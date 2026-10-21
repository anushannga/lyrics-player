#!/usr/bin/env python3
"""Stream the supplied ISI bitmaps against the actual Mac audio playback clock."""
import argparse,binascii,glob,hashlib,json,struct,subprocess,sys,time
from pathlib import Path
import serial
ROOT=Path(__file__).resolve().parent
MP3=Path.home()/'Downloads/Sellakkaraya - Kaizer Kaiz Ft. Lil Neo.mp3'

def compress(raw):
    out=bytearray();i=0
    while i<len(raw):
        if raw[i]==0 and (i+1==len(raw) or raw[i+1]==0):
            end=i+1
            while end<len(raw) and raw[end]==0 and end-i<128:end+=1
            out.append(0x80|(end-i-1));i=end
        else:
            start=i;i+=1
            while i<len(raw) and i-start<128:
                if raw[i]==0 and i+1<len(raw) and raw[i+1]==0:break
                i+=1
            out.append(i-start-1);out.extend(raw[start:i])
    return bytes(out)

class LCD:
    def __init__(self,port):
        self.s=serial.Serial(port,115200,timeout=0.2,write_timeout=2,exclusive=True)
        time.sleep(2);self.s.reset_input_buffer();self.seq=0;self.previous=bytes(1024)
        self.s.write(b'?');self.expect('STREAMLCD 1')
    def expect(self,text):
        deadline=time.monotonic()+4
        while time.monotonic()<deadline:
            response=self.s.readline().decode('ascii',errors='replace').strip()
            if response==text:return
            if response.startswith('ERR'):raise RuntimeError('LCD: '+response)
        raise RuntimeError('LCD did not acknowledge '+text)
    def check_layout(self):
        from PIL import Image,ImageDraw
        from tools.pixel_format import native
        image=Image.new('1',(128,64));draw=ImageDraw.Draw(image)
        for xy in [(0,0),(7,0),(8,1),(13,17),(127,63)]:draw.point(xy,fill=1)
        draw.rectangle((20,25,50,43),outline=1)
        expected=binascii.crc_hqx(native(image),0xffff)
        self.s.write(b'T');self.expect('TEST '+str(expected))
        self.clear();print('ST7920 pixel layout verified against U8g2 on the board.',flush=True)
    def frame(self,raw):
        assert len(raw)==1024
        self.seq=(self.seq+1)&65535
        body=compress(raw)
        packet=b'F'+struct.pack('<HH',self.seq,len(body))+body+struct.pack('<H',binascii.crc_hqx(raw,0xffff))
        for attempt in range(2):
            try:
                self.s.write(packet);self.s.flush();self.expect('OK '+str(self.seq));return
            except RuntimeError:
                if attempt:raise
                time.sleep(1.1);self.s.reset_input_buffer()
    def show(self,raw,smooth=True,steps=2):
        start=time.monotonic()
        if raw==self.previous:return 0
        if smooth:
            bayer=((0,8,2,10),(12,4,14,6),(3,11,1,9),(15,7,13,5))
            for phase in range(1,steps):
                threshold=16*phase/steps
                masks=[sum((1<<(7-x)) for x in range(8) if bayer[y][x%4]<threshold) for y in range(4)]
                intermediate=bytes((a&~masks[(i//16)%4])|(b&masks[(i//16)%4]) for i,(a,b) in enumerate(zip(self.previous,raw)))
                self.frame(intermediate)
        self.frame(raw);self.previous=raw
        return time.monotonic()-start
    def clear(self):
        start=time.monotonic();self.s.write(b'C');self.s.flush();self.expect('OK C');self.previous=bytes(1024)
        return time.monotonic()-start
    def close(self):self.s.close()

def main():
    global MP3
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port');parser.add_argument('--test',action='store_true')
    parser.add_argument('--verify',action='store_true',help='Verify every unique frame over USB without audio')
    parser.add_argument('--dry',action='store_true');parser.add_argument('--offset',type=float,default=0)
    parser.add_argument('--start',type=float,default=0,help='Start audio at this song position')
    parser.add_argument('--stop',type=float,help='Stop a preview at this song position')
    parser.add_argument('--loop',action='store_true',help='Repeat the full song and lyrics until Ctrl+C')
    parser.add_argument('--mp3',type=Path,default=MP3,help='Local audio file matching the saved timing hash')
    args=parser.parse_args()
    MP3=args.mp3.expanduser()
    if args.loop and (args.start or args.stop is not None or args.test or args.verify):parser.error('--loop repeats the full song; use without preview or test options')
    if not 0<=args.start<296.10:parser.error('--start must be within the song')
    if args.stop is not None and not args.start<args.stop<=296.10:parser.error('--stop must be after --start and within the song')
    settings=json.loads((ROOT/'player_settings.json').read_text())
    fade_frames=settings['fade_frames']
    if any(not isinstance(fade_frames.get(s),int) or not 1<=fade_frames[s]<=16 for s in ('rap','melodic')):raise ValueError('Fade frames must be between 1 and 16')
    manifest=json.loads((ROOT/'manifest.json').read_text());blob=(ROOT/'frames.bin').read_bytes()
    if manifest.get('pixel_format')!='st7920-horizontal-msb':raise RuntimeError('Rebuild frames for the ST7920 pixel layout')
    frames=[blob[i:i+1024] for i in range(0,len(blob),1024)]
    assert len(frames)==manifest['bitmap_count'] and all(len(x)==1024 for x in frames)
    if not (args.test or args.verify):
        timing=json.loads((ROOT/'timings.json').read_text());cues=timing['cues']
        if timing['lyrics_id']!=manifest['id']:raise RuntimeError('Timing belongs to different lyrics')
        if timing['audio_sha256']!=hashlib.sha256(MP3.read_bytes()).hexdigest():raise RuntimeError('Timing belongs to another MP3')
        assert all(a['time']<b['time'] for a,b in zip(cues,cues[1:]))
        if args.dry:
            print(f"{manifest['line_count']} lyrics / {len(manifest['pages'])} pages / {len(cues)} timed events")
            for cue in cues:print(f"{cue['time']:8.3f}s  page {cue['page']+1}")
            return
    ports=glob.glob('/dev/cu.usbmodem*')+glob.glob('/dev/cu.usbserial*')
    if not args.port and len(ports)!=1:raise RuntimeError('Specify --port: expected exactly one connected Arduino')
    lcd=LCD(args.port or ports[0]);proc=None;log=[]
    try:
        if args.verify:
            lcd.check_layout()
            durations=[]
            for i,frame in enumerate(frames):
                dt=lcd.show(frame,smooth=False);durations.append(dt)
                print(f"Frame {i+1}/{len(frames)} CRC+ACK {dt*1000:.0f}ms",flush=True)
            lcd.show(frames[0]);print('All unique frames verified.',flush=True);return
        if args.test:
            for i,page in enumerate(manifest['pages'][:8]):
                dt=lcd.show(frames[page['bitmap']]);print(f'Page {i+1}: {dt*1000:.0f}ms',flush=True);time.sleep(0.7)
            return
        while True:
            lcd.clear();leads={s:fade_frames[s]*0.08 for s in fade_frames};clear_lead=0.08;index=0;preview=args.start>0 or args.stop is not None;stopped_early=False
            clock=ROOT/'tools/audio_clock';source=ROOT/'tools/audio_clock.m'
            if not clock.exists() or clock.stat().st_mtime<source.stat().st_mtime:
                subprocess.run(['clang','-fobjc-arc','-framework','Foundation','-framework','AVFoundation',str(source),'-o',str(clock)],check=True)
            print('Playing Sellakkaraya — automatic ISI lyrics',flush=True)
            proc=subprocess.Popen([str(clock),str(MP3),str(args.start)],stdout=subprocess.PIPE,text=True,bufsize=1)
            for row in proc.stdout:
                kind,value=row.strip().split()
                if kind=='END':break
                if kind!='TIME':continue
                now=float(value);due=None
                if args.stop is not None and now>=args.stop:
                    stopped_early=True;proc.terminate();proc.wait();break
                while index<len(cues):
                    cue=cues[index];ahead=clear_lead if cue['page']<0 else leads[cue.get('style','rap')]
                    if now<max(0,cue['time']+args.offset-ahead):break
                    due=cue;index+=1
                if due is not None:
                    if due['page']<0:dt=lcd.clear();clear_lead=dt
                    else:
                        page=manifest['pages'][due['page']]
                        style=due.get('style','rap')
                        dt=lcd.show(frames[page['bitmap']],steps=fade_frames[style])
                        if dt:leads[style]=max(0.05,min(1.5,dt))
                    log.append({'audio_time':now,'target':due['time'],'page':due['page'],'transfer_seconds':dt})
                    print(f"{now:7.3f}s  {'CLEAR' if due['page']<0 else 'page '+str(due['page']+1)}  {dt*1000:.0f}ms",flush=True)
            if proc.wait()!=0 and not stopped_early:raise RuntimeError('Audio playback failed')
            lcd.clear()
            (ROOT/('last_preview.json' if preview else 'last_playback.json')).write_text(json.dumps({'complete':index==len(cues),'preview':preview,'lyrics_id':manifest['id'],'events':log},indent=2)+'\n')
            print('Preview complete.' if preview else 'Playback complete.',flush=True)
            if not args.loop:break
            print("Restarting song and lyrics...",flush=True)
    finally:
        if proc and proc.poll() is None:proc.terminate();proc.wait()
        lcd.close()

if __name__=='__main__':
    try:main()
    except KeyboardInterrupt:print('\nStopped.');sys.exit(130)
    except (ValueError,RuntimeError,OSError,AssertionError) as error:print(str(error),file=sys.stderr);sys.exit(1)
