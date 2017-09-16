import max7219

import alsaaudio as aa
import wave
from struct import unpack
import numpy as np


spectrum = [1,1,1,3,3,3,2,2]
levels = [0,0,0,0,0,0,0,0]
power  = []
weighting = [2,8,8,16,16,32,32,64]


def songSource(name):
    return wave.open('/media/pi/My Passport/Musik/wav-files/'+name,'r')


# Audio setup

#wavfile = wave.open('/home/pi/Music/opus_ericprydz.wav','r')
#wavfile = wave.open('/home/pi/Music/sunset_over_manaan_attlas.wav','r')
wavfile = wave.open('/home/pi/Music/strobe_deadmau5.wav','r')


sample_rate = wavfile.getframerate()
no_channels = wavfile.getnchannels()
chunk = 4096

output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
output.setchannels(no_channels)
output.setrate(sample_rate)
output.setformat(aa.PCM_FORMAT_S16_LE)
output.setperiodsize(chunk)
def piff(val):
    return int(2*chunk*val/sample_rate)

def getLevels(data, chunk, sample_rate):
    global levels

    data = unpack("%dh"%(len(data)/2),data)
    data = np.array(data,dtype='h')

    fourier = np.fft.rfft(data)
 
    fourier = np.delete(fourier, len(fourier)-1)
    
    power = np.abs(fourier)
   
    
    levels[0] = int(np.mean(power[piff(0)    : piff(156) :1]))
    levels[1] = int(np.mean(power[piff(156)  : piff(312) :1]))
    levels[2] = int(np.mean(power[piff(312)  : piff(624) :1]))
    levels[3] = int(np.mean(power[piff(624)  : piff(1248) :1]))
    levels[4] = int(np.mean(power[piff(1248) : piff(2496) :1]))
    levels[5] = int(np.mean(power[piff(2496) : piff(4992) :1]))
    levels[6] = int(np.mean(power[piff(4992) : piff(9984) :1]))
    levels[7] = int(np.mean(power[piff(9984): piff(19968) :1]))


    levels = np.divide(np.multiply(levels, weighting),2000000)      #set high                               

    levels = levels.clip(0,8)
   
    return levels


audioData = wavfile.readframes(chunk)
max7219.initMax7219()
while audioData!='':
    output.write(audioData)
    levels=getLevels(audioData, chunk, sample_rate)
    #print(levels, "levels")

    patternArray = max7219.freqToPattern(levels)
    max7219.pattern(patternArray)
    audioData = wavfile.readframes(chunk)
  

    
    

