#!/usr/bin/env python3
"""Play Sandawaka Mathaka against the Mac audio clock and send Arduino cues."""
import argparse
import glob
import hashlib
import json
import select
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_MP3 = Path.home()/'Downloads/Sandawaka Mathaka.mp3'

def load_cues(path, count):
    data=json.loads(path.read_text())
    cues=data['cues']
    previous=-1
    for cue in cues:
        t=cue['time']; line=cue['line']
        if not isinstance(t,(int,float)) or not 0<=t<float('inf') or t<previous:
            raise ValueError('Cue times must be finite, nonnegative and ordered')
        if not isinstance(line,int) or not -1<=line<count:
            raise ValueError('Invalid lyric index')
        previous=t
    if not cues: raise ValueError('No timing cues')
    return data

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mp3',nargs='?',type=Path,default=DEFAULT_MP3)
    p.add_argument('--port')
    p.add_argument('--test',action='store_true',help='Display every lyric without audio')
    p.add_argument('--tap',action='store_true',help='Record real lyric starts with Enter')
    p.add_argument('--dry',action='store_true',help='Validate and list timings without opening audio or USB')
    p.add_argument('--offset',type=float,default=0,help='Positive = lyrics later, negative = earlier')
    p.add_argument('--times',type=Path,default=ROOT/'timings.json')
    a=p.parse_args()
    report=json.loads((ROOT/'render_report.json').read_text())
    count=len(report['lines'])
    if a.dry:
        data=load_cues(a.times,count)
        print('Timing status:',data.get('status','unspecified'))
        for c in data['cues']:print(f"{c['time']+a.offset:8.3f}s  {'CLEAR' if c['line']<0 else 'L'+str(c['line'])}")
        return
    if not a.test and not a.mp3.is_file():p.error('MP3 not found: '+str(a.mp3))
    if not a.test and not a.tap:
        if not a.times.exists():
            p.error(f'No measured timing file. Run with --tap to record the {count} lyric starts.')
        data=load_cues(a.times,count)
        if data.get('lyrics_id') != report['id']:
            p.error('Lyrics changed. Run --tap to record timings for this lyric sequence.')
        digest=hashlib.sha256(a.mp3.read_bytes()).hexdigest()
        if data.get('audio_sha256') and data['audio_sha256']!=digest:
            p.error('Timing file belongs to a different MP3')
        print('Timing status:',data.get('status','unspecified'),flush=True)
    import serial
    ports=glob.glob('/dev/cu.usbmodem*')
    if not a.port and len(ports)!=1:p.error('Specify --port; expected exactly one Arduino USB port')
    with serial.Serial(a.port or ports[0],9600,timeout=0.2,write_timeout=1,exclusive=True) as board:
        time.sleep(2)
        board.reset_input_buffer()
        def command(text, expected):
            board.write((text+'\n').encode('ascii'));board.flush()
            deadline=time.monotonic()+3
            while time.monotonic()<deadline:
                response=board.readline().decode('ascii',errors='replace').strip()
                if response==expected or (expected is None and response):return response
            raise RuntimeError('Arduino did not acknowledge '+text)
        command('?',f"LYRICS {report['id']} {count}")
        timing_response=command('D',None)
        if not timing_response.startswith('DRAW_MS '):
            raise RuntimeError('Upload the smooth-transition firmware before playing')
        transition_lead=max(0.08,min(0.8,int(timing_response.split()[1])/1000+0.012))
        print(f'LCD transition: {transition_lead*1000:.0f}ms (automatically compensated)',flush=True)
        if a.test:
            for n in range(count):
                start=time.monotonic();command('L'+str(n),'OK L'+str(n))
                print(f'Line {n+1:02}: ACK in {(time.monotonic()-start)*1000:.0f}ms',flush=True)
                time.sleep(0.9)
            command('L0','OK L0');return
        command('C','OK C')
        clock=ROOT/'tools/audio_clock'
        source=ROOT/'tools/audio_clock.m'
        if not clock.exists() or clock.stat().st_mtime<source.stat().st_mtime:
            subprocess.run(['clang','-fobjc-arc','-framework','Foundation','-framework','AVFoundation',str(source),'-o',str(clock)],check=True)
        proc=subprocess.Popen([str(clock),str(a.mp3)],stdout=subprocess.PIPE,text=True,bufsize=1)
        recorded=[]; index=0; now=0
        unicode_lines=(ROOT/'lyrics_unicode.txt').read_text().splitlines()
        if a.tap:
            print(f'Press Enter at the START of each new lyric ({count} presses). Ctrl+C cancels without replacing saved timings.',flush=True)
            print('NEXT: '+unicode_lines[0],flush=True)
        try:
            for raw in proc.stdout:
                kind,value=raw.strip().split()
                if kind=='END':break
                if kind!='TIME':continue
                now=float(value)
                if a.tap:
                    if index<count and select.select([sys.stdin],[],[],0)[0]:
                        if not sys.stdin.readline():raise RuntimeError('Tap mode needs an interactive terminal')
                        command('L'+str(index),'OK L'+str(index))
                        recorded.append({'time':round(now,3),'line':index})
                        print(f'{index+1:02}/{count}  {now:.3f}s',flush=True);index+=1
                        if index<count:print('NEXT: '+unicode_lines[index],flush=True)
                        if index==count:
                            saved={'status':'manually tapped lyric starts','lyrics_id':report['id'],'audio_sha256':hashlib.sha256(a.mp3.read_bytes()).hexdigest(),'cues':recorded}
                            if a.times.exists():
                                backup=a.times.with_name(a.times.stem+'-backup-'+time.strftime('%Y%m%d-%H%M%S')+'.json')
                                backup.write_bytes(a.times.read_bytes())
                            a.times.write_text(json.dumps(saved,ensure_ascii=False,indent=2)+'\n')
                            print('Saved '+str(a.times),flush=True)
                else:
                    cues=data['cues']
                    # Begin each dissolve early enough to finish at the sung cue.
                    # Consume stale events in one step if the computer was briefly busy.
                    due=None
                    while index<len(cues):
                        lead=0.080 if cues[index]['line']<0 else transition_lead
                        if now<max(0,cues[index]['time']+a.offset-lead):break
                        due=cues[index];index+=1
                    if due is not None:
                        n=due['line'];text='C' if n<0 else 'L'+str(n)
                        draw_started=time.monotonic()
                        command(text,'OK '+text)
                        if n>=0:
                            measured=time.monotonic()-draw_started
                            transition_lead=max(0.08,min(0.8,measured))
                        print(f'{now:7.3f}s  {text}',flush=True)
            if proc.wait()!=0:raise RuntimeError('Audio player failed')
            if a.tap and index<count:raise RuntimeError(f'Only {index}/{count} starts recorded; timing file was not replaced')
            command('C','OK C')
        finally:
            if proc.poll() is None:
                proc.terminate();proc.wait()

if __name__=='__main__':
    try:main()
    except KeyboardInterrupt:print('\nStopped.');sys.exit(130)
    except (ValueError,RuntimeError,OSError) as e:print(str(e),file=sys.stderr);sys.exit(1)
