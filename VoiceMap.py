import librosa
import librosa.display
import os
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import scipy
from scipy.signal import butter, sosfiltfilt
from scipy.signal import sosfiltfilt
import scipy.signal as signal
from scipy.io.wavfile import write

audio_path = 'BogDan_crop.wav'
signal, freq = librosa.load(audio_path)

plt.figure(figsize = (12,12))
D = librosa.amplitude_to_db(librosa.stft(signal), ref = np.max)
plt.subplot(4,1,1)
librosa.display.specshow(D, y_axis = 'linear')
plt.colorbar(format = '%+2.0f dB')
plt.title('Спектограмма энергии частоты')

pd.Series(signal).plot(figsize=(5,5), lw=1, title = "Sound")
