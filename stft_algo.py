'''To implement STFT and plot the resulting data'''
import numpy
from scipy.io import wavfile
import matplotlib.pyplot as plt

audio_file = raw_input("Enter file name : ")
rate, data = wavfile.read( audio_file )

sampling_freq = 4000
frame_size = 0.050
overlap = 0.020

stft_data = []
fs = int(frame_size * sampling_freq)
os = int(overlap * sampling_freq)
win = numpy.hamming( fs ) #window function
for i in range(0,len(data)-fs, os): #0 to last but one frame, step with overlap length
    fft_data = numpy.fft.fft(win*data[i:i+fs]) #multiply the frame with window function and take fft of it
    stft_data.append(fft_data) 

plt.plot(numpy.array(stft_data))
#plt.specgram(numpy.array(stft_data))
plt.show()

