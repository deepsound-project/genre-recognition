import librosa
from librosa import display
import matplotlib.pyplot as plt
import numpy as np
import cPickle as pickle

# Load pickle

#data = pickle.load(open( "/Users/Andrew/Development/music-genre-recognition/data/data.pkl", "rb" ))
data = pickle.load(open( "/Users/Andrew/Development/music-genre-recognition/data/data.pkl", "rb" ))
data2 = pickle.load(open( "/Users/Andrew/Development/music-genre-recognition/data/ix1.pkl", "rb" ))
#print "1,", data['x'][0]
#print "2,", data['x'][len(data)-1]

print data['x'][0][0]
for i in range(len(data)):
	t1 = data['x'][i][0]
	t2 = data2['x'][i][0]
	if t1.all() == t2.all():
		print 'true'
	else:
		print 'false'
#print data['y'][0]
#print data['y'][100]
# Load sound file
#y, sr = librosa.load("/Users/Andrew/Downloads/fma/132567.mp3")


#stft = np.abs(librosa.stft(data['x'][1292], n_fft=2048,  hop_length=2048//2))
#mel = librosa.feature.melspectrogram(sr=1, S=stft**2) #data['x'][0]
#print mel.T
#log_mel = librosa.logamplitude(mel)
#print log_mel, log_mel.size

# Let's make and display a mel-scaled power (energy-squared) spectrogram
#S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)

# Convert to log scale (dB). We'll use the peak power as reference.
#log_S = librosa.logamplitude(S, ref_power=np.max)
'''
# Make a new figure
plt.figure(figsize=(12,4))

# Display the spectrogram on a mel scale
# sample rate and hop length parameters are used to render the time axis


librosa.display.specshow(data['x'][0].T, x_axis='time', y_axis='mel')
#librosa.display.specshow(data['x'][2].T, x_axis='time', y_axis='mel')
#librosa.display.specshow(data['x'][len(data)-1].T, x_axis='time', y_axis='mel')

# Put a descriptive title on the plot
plt.title('mel power spectrogram')

# draw a color bar
plt.colorbar(format='%+02.0f dB')

# Make the figure layout compact
#plt.tight_layout()
plt.show()
'''
'''
librosa.display.specshow(data['x'][0].T, x_axis='time', y_axis='mel')

plt.title('mel power spectrogram')

# draw a color bar
plt.colorbar(format='%+02.0f dB')

# Make the figure layout compact
plt.tight_layout()
plt.show()
'''
