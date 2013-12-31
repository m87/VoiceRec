#!/usr/bin/env python
# -*- coding: utf -*-

from __future__ import division
from numpy import *
from scipy import *
import scipy.io.wavfile as wavfile
import scipy.fftpack as fftpack
import os as os
import wave
import struct
from matplotlib import pyplot as pt
def loadFiles(path):
    """reads wave files from path and returns dictionary with fields:
        - "name" - name of file
        - "nameGender" - a gender taken from file name
        - "signal" - numpy array with sound signal readed from file
        - "sampleRate" - sample rate of the file
 
        and dictionary that contains numbers of male and female voices
    """
 
    files = [ f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) and os.path.splitext(f)[1] == ".wav" ]
 
    samples = []
    maleCount = 0
    femaleCount = 0
    for f in files:
        p = path + '/' + f
 
        with open(p, "rb") as wavFile:
            wavFile.read(24)
            
            rate = wavFile.read(4)
            rate = struct.unpack('<i',rate)[0]
            
            wavFile.read(6)
            
            bps = wavFile.read(2)
            bps = struct.unpack('<h',bps)[0]
 
            wavFile.read(8)
            
            sig = []
            sampleSize = bps/8
            b = wavFile.read(int(sampleSize))
            while b != "":
                b = struct.unpack('<h', b)
                sig.append(b[0])
                b = wavFile.read(int(sampleSize))
            
            
        samples.append({'name': f, 'nameGender': f[-5:-4], 'signal': sig, 'sampleRate': rate})
        
        if f[-5:-4] == "M":
            maleCount += 1
        else:
            femaleCount += 1
    
    counters = {"maleCount":maleCount, "femaleCount":femaleCount}
    return samples, counters

samples, counters = loadFiles("train")
correct=0
for sam in samples:
    wf= sam['signal']

    w = sam['sampleRate']           # czÄstotliwoĹÄ prĂłbkowania [Hz]
    T=1
 
    n = w*T        # liczba prĂłbek

    t = linspace(0,T,n,endpoint=False)
    f = wf[0:n:1]
    pt.subplot(211)
    pt.plot(t,f,'*')

    signal1 = fft(f)      
    signal1 = (abs(signal1))        # moduĹ 
    
    freqs = linspace(0,w,n)
    
    pt.subplot(212)
    #pt.plot(freqs[0:len(freqs)/w*600], signal1[0:len(freqs)/w*600], '-*')
    #pt.plot(freqs[0:len(freqs)/w*600], signal1[0:len(freqs)/w*600], '-*')
    sumaLow=0
    sumaHigh=0
    shrimM =0.0
    shrimK =0.0
    for f in signal1[len(freqs)/w*80:len(freqs)/w*180]:
        if(f>995000.0):
            sumaLow=sumaLow+1
    for f in signal1[len(freqs)/w*150:len(freqs)/w*250]:
        if(f>995000.0):
            sumaHigh=sumaHigh+1
    
    for f in range(int(len(freqs)/w*80),int(len(freqs)/w*180)-1):
        shrimM = shrimM + abs(20*log(signal1[f+1]/signal1[f]))
    shrimM = 1/(len(freqs)/w*80+len(freqs)/w*180-1)*shrimM

    for f in range(int(len(freqs)/w*150),int(len(freqs)/w*250)-1):
        shrimK = shrimK + abs(20*log(signal1[f+1]/signal1[f]))
    shrimK = 1/(len(freqs)/w*150+len(freqs)/w*250-1)*shrimK

    
    if(sumaLow > sumaHigh and shrimM >1.5):
        pt.plot(freqs[len(freqs)/w*80:len(freqs)/w*180], signal1[len(freqs)/w*80:len(freqs)/w*180], '-*')
        if(sam["nameGender"]=="M"):
            correct = correct + 1
    else:
        pt.plot(freqs[len(freqs)/w*180:len(freqs)/w*300], signal1[len(freqs)/w*180:len(freqs)/w*300], '-*')
        if(sam["nameGender"]=="K"):
            correct = correct + 1
   
    #pt.show()
    
print correct/(counters["femaleCount"]+counters["maleCount"]) 
    
    


