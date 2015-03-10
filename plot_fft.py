import numpy
from matplotlib import pyplot as plt
from scipy.io import wavfile

audio_file = input("Enter the audio file path : ")
rate, data = wavfile.read(audio_file)

fft_data = numpy.fft.fft(data)
ifft_data = numpy.fft.ifft(fft_data)

plt.plot(fft_data, label="Fast Fourier Transform")
plt.show()

plt.plot(ifft_data, label="Inverse Fast Fourier Transform")
plt.show()

