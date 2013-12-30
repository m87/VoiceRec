#!/usr/bin/env python
# -*- coding: utf -*-

from __future__ import division
from pylab import *
from numpy import *
from scipy import *
import scipy.io.wavfile as wavfile

f = (wavfile.read("train/005_M.wav")[1])
t = range(0,len(f))
subplot(211)
plot(t,f,'*')

signal1 = fft(f)      
signal1 = abs(signal1)        # moduĹ 



subplot(212)
freqs = range(0,len(signal1))              # <-- ZACZNIJ TUTAJ. UĹźyj linspace
plot(freqs, signal1, '-*')


show()


