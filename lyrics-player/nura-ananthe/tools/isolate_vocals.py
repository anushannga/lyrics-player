"""Local MDX vocal analysis of three hooks; no audio is uploaded."""
import json,hashlib
from pathlib import Path
import av,numpy as np,onnxruntime as ort
from scipy.signal import stft,istft,resample_poly,windows
from scipy.io import wavfile
R=Path(__file__).resolve().parents[1]
model=Path.home()/'.cache/audio-models/Kim_Vocal_2.onnx'
expected='ce74ef3b6a6024ce44211a07be9cf8bc6d87728cc852a68ab34eb8e58cde9c8b'
assert hashlib.sha256(model.read_bytes()).hexdigest()==expected
options=ort.SessionOptions();options.intra_op_num_threads=4;options.inter_op_num_threads=1
session=ort.InferenceSession(str(model),sess_options=options,providers=['CPUExecutionProvider'])
input_name=session.get_inputs()[0].name
source=next((Path.home()/'Downloads').glob('Cozzy - Nura Ananthe*mp3'))
container=av.open(str(source));resampler=av.AudioResampler(format='fltp',layout='stereo',rate=44100);chunks=[]
for frame in container.decode(audio=0):
 for out in resampler.resample(frame):chunks.append(out.to_ndarray())
for out in resampler.resample(None):chunks.append(out.to_ndarray())
x=np.concatenate(chunks,axis=1).astype(np.float32);container.close()
N=7680;H=1024;T=256;F=3072;chunk=H*(T-1);trim=N//2;step=chunk-2*trim;win=windows.hann(N,sym=False).astype(np.float32)
regions=[('song',0,150.517551)];report=[]
for name,start,end in regions:
 signal=x[:,round(start*44100):round(end*44100)];length=signal.shape[1];pad=(-length)%step
 padded=np.pad(signal,((0,0),(trim,trim+pad)));parts=[]
 for i,offset in enumerate(range(0,length+pad,step)):
  audio=padded[:,offset:offset+chunk]
  _,_,z=stft(audio,window=win,nperseg=N,noverlap=N-H,nfft=N,boundary='even',padded=False,axis=-1)
  z=(z*win.sum()).astype(np.complex64)
  assert z.shape==(2,N//2+1,T),z.shape
  spec=np.stack([z[0].real,z[0].imag,z[1].real,z[1].imag])[None,:,:F,:].astype(np.float32)
  spec[:,:,0:3,:]=0
  predicted=session.run(None,{input_name:spec})[0][0]
  result=np.zeros((2,N//2+1,T),dtype=np.complex64)
  result[0,:F]=predicted[0]+1j*predicted[1];result[1,:F]=predicted[2]+1j*predicted[3]
  _,wave=istft(result/win.sum(),window=win,nperseg=N,noverlap=N-H,nfft=N,input_onesided=True,boundary=True,time_axis=-1,freq_axis=-2)
  assert wave.shape[-1]==chunk,wave.shape
  parts.append(wave[:,trim:-trim])
  print(name,'vocal chunk',i+1,flush=True)
 vocals=np.concatenate(parts,axis=1)[:,:length]*1.009
 mono=resample_poly(vocals.mean(axis=0),160,441).astype(np.float32)
 dest=R/'analysis';dest.mkdir(exist_ok=True);wavfile.write(dest/(name+'-vocals.wav'),16000,mono)
 hop=160;envelope=np.array([np.sqrt(np.mean(mono[i:i+400]**2)) for i in range(0,len(mono)-400,hop)])
 peak=float(np.percentile(envelope,97));threshold=peak*.14
 active=envelope>threshold
 # Join very short interruptions in a single held note, without moving onsets.
 for i in range(1,len(active)-12):
  if active[i-1] and not active[i] and active[i:i+12].any():
   j=i+int(np.argmax(active[i:i+12]));active[i:j]=True
 starts=np.flatnonzero(active&~np.r_[False,active[:-1]]);ends=np.flatnonzero(active&~np.r_[active[1:],False])
 runs=[{'start':round(start+float(a)*.01,3),'end':round(start+float(b+1)*.01,3)} for a,b in zip(starts,ends) if b-a>=8]
 report.append({'section':name,'window':[start,end],'rms_threshold':threshold,'voice_regions':runs,'file':str((dest/(name+'-vocals.wav')).relative_to(R))})
 (R/'vocal_regions.json').write_text(json.dumps(report,indent=2))
 print(name,'voice regions:',runs,flush=True)
