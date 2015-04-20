import numpy
from scipy.io import wavfile
import matplotlib.pyplot as plt
import sys

if( len(sys.argv) < 2 ):
    print "Usage : python2.7 plot_specgram.py [FILENAME]"
    exit()
audio_file = sys.argv[1]
#audio_file = raw_input("Enter file name : ")
rate, data = wavfile.read( audio_file )

sampling_freq = int(raw_input("Enter sampling freq : "))
frame_size = float(raw_input("Enter frame size : "))
overlap = float(raw_input("Enter overlap : "))



fs = int(frame_size * sampling_freq)
os = int(overlap * sampling_freq)
win = numpy.hamming( fs ) #window function
(spec, freqs, t, im) = plt.specgram( numpy.array(data), NFFT=fs, Fs=sampling_freq, window=numpy.hamming(fs), noverlap=os )
plt.show()
