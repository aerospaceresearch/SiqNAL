import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import cmath
from os import path
import scipy.io.wavfile
from scipy.fftpack import fft,fftshift,ifft
from scipy import signal
from scipy.signal import csd,periodogram
import fourier

def psd(signal,fc,fs,window='boxcar', nfft=None, detrend='constant',return_onesided=False, scaling='density', axis=-1):

	if window is None:
		window = 'boxcar'

	if nfft is None:
		nperseg = signal.shape[axis]
	elif nfft == signal.shape[axis]:
		nperseg = nfft
	elif nfft > signal.shape[axis]:
		nperseg = signal.shape[axis]
	elif nfft < signal.shape[axis]:
		s = [np.s_[:]]*len(signal.shape)
		s[axis] = np.s_[:nfft]
		signal = signal[s]
		nperseg = nfft
		nfft = None

	noverlap=0

	frequency,pxx=csd(signal,signal,fs, window, nperseg,noverlap,nfft,'constant', return_onesided,scaling,axis)
	frequency=frequency+fc

	return pxx,frequency

def LoadData(filename):

	try:

		rate,signal=scipy.io.wavfile.read(filename,mmap=True)
		signal=signal[44:,:]
		return signal

	except:

		return None


if __name__=="__main__":

	data_directory=path.join(os.getcwd(),'data')
	filename=path.join(data_directory,'station1_yagi_SDRSharp_20170312_060959Z_137650kHz_IQ.wav')

	signal=LoadData(filename)

	if(type(signal)==None):

		print("Requested file not found !!!!!!")

	else:

		fs=2*1e6
		fc=137.65*1e6

		chunksize=2000000
		last=1
		
		for i in range(0,last):

			start=i*chunksize
			end=start+chunksize

			signal_chunk=signal[start:end,:]
			signal_chunk=signal_chunk.flatten()
			signal_chunk=signal_chunk-127.5

			signal_chunk_iq = np.empty(signal_chunk.shape[0]//2, dtype=np.complex128)
			signal_chunk_iq.real = signal_chunk[::2]
			signal_chunk_iq.imag = signal_chunk[1::2]

			pxx,frequency=psd(signal_chunk_iq,fc,fs,scaling='spectrum')
			plt.rcParams["figure.figsize"] = (16,6)
			fig=plt.figure()

			ax = fig.add_subplot(111)
			plt.gca().xaxis.grid(True)
			plt.gca().yaxis.grid(True)
			ax.set_xlabel('Frequency(MHz)')
			ax.set_ylabel('PSD')
			plt.plot(frequency,pxx)

			plt.show()
