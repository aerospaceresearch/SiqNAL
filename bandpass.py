import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import cmath
from os import path
import scipy.io.wavfile
from scipy.fftpack import fft,fftshift
from scipy import signal
from scipy.signal import butter, lfilter, firwin, fftconvolve
import fourier

def bandpass_filter(data,ntap,fstop,fs,window='hanning'):
	h = firwin(ntap,float(fstop),nyq=float(fs)/2,window=window)
	h = np.append(h,np.zeros(1024-len(h)))

	filtered_data = fftconvolve(data, h)

	return filtered_data

def LoadData(filename):

	try:

		rate,signal=scipy.io.wavfile.read(filename,mmap=True)
		signal=signal[44:,:]
		return signal

	except:

		return None

if __name__ == '__main__':

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

			final=bandpass_filter(signal_chunk_iq,513,0.5*1e6,2e6,'hanning')
			plt.rcParams["figure.figsize"] = (16,12)
			fig=plt.figure()

			frequency,transform=fourier.CalcFourier(signal_chunk_iq,fs,fc)
			ax = fig.add_subplot(211)
			plt.gca().xaxis.grid(True)
			plt.gca().yaxis.grid(True)
			ax.set_xlabel('Frequency(MHz)')
			ax.set_ylabel('|X(f)|')
			plt.plot(frequency,transform)

			frequency1,transform1=fourier.CalcFourier(final,fs,fc)
			ax = fig.add_subplot(212)
			plt.gca().xaxis.grid(True)
			plt.gca().yaxis.grid(True)
			ax.set_xlabel('Frequency(MHz)')
			ax.set_ylabel('|X(f)|')
			plt.plot(frequency1,transform1)

			plt.show()