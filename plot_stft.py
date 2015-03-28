import numpy
from matplotlib import pyplot as plt
from scipy.io import wavfile
import stft

audio_file = raw_input("Enter the audio file path : ")
rate, data = wavfile.read(audio_file)

win = stft.stft.cosine(256) #Windowing function
stft_data = stft.stft.process( data, window=win )

#stft_data = stft.stft.spectrogram(data,window=win,framelength=2048)

plt.specgram(stft_data)
#plt.plot( stft_data )
plt.show()
