import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from os import path
import scipy.io.wavfile
from scipy.fftpack import fft,fftshift
from scipy import signal

def PlotSpectrogram(freq_vector, dummy_vector,data, dbf = 60) :

	eps = 1e-3
	data_max = abs(data).max()

	data_log = 20.0 * np.log10( abs( data ) / data_max + eps )
	display_data=(np.flipud( 64.0*(data_log + dbf)/dbf ))

	fig=plt.figure(figsize=(16,5))
	plt.imshow( display_data.T, extent= freq_vector + dummy_vector ,aspect='auto', interpolation="nearest")
	plt.xlabel('Frequency (Hz)')
	plt.tight_layout()

def ShortTimeSpectrogram(signal, N, fs, fc):

	len_signal = len(signal);
	len_padding = (len_signal + N - 1) // N

	signal = np.append(signal,np.zeros(-len_signal+len_padding*N))
	signal = signal.reshape((N//2,len_padding*2), order='F')
	signal = np.concatenate((signal,signal),axis=0)
	signal = signal.reshape((N*len_padding*2,1),order='F')
	signal = signal[np.r_[N//2:len(signal),np.ones(N//2)*(len(signal)-1)].astype(int)].reshape((N,len_padding*2),order='F')


	signal_spectrogram = signal * np.hanning(N)[:,None];
	signal_spectrogram = np.fft.fftshift( np.fft.fft( signal_spectrogram ,len(signal_spectrogram),axis=0), axes=0 )

	return signal_spectrogram

def GenerateSpectrogram(signal,fs,fc):

	chunksize=2000000
	fft_points=1024

	len_signal=signal.shape[0]
	last = int(len_signal//chunksize)

	for i in range(0,last):

		start=i*chunksize
		end=start+chunksize

		signal_chunk=signal[start:end,:]
		signal_chunk=signal_chunk.flatten()
		signal_chunk=signal_chunk-127.5

		signal_chunk_iq = np.empty(signal_chunk.shape[0]//2, dtype=np.complex128)
		signal_chunk_iq.real = signal_chunk[::2]
		signal_chunk_iq.imag = signal_chunk[1::2]

		signal_chunk_spectrogram_data = ShortTimeSpectrogram(signal_chunk_iq,fft_points,fs,fc)

		if (i == 0):

			dimension=signal_chunk_spectrogram_data.shape
			spectrogram_data=np.zeros(dimension,dtype=np.complex128)
			len_dummy=len(signal_chunk_iq)

		spectrogram_data += signal_chunk_spectrogram_data
		
		del signal_chunk_iq , signal_chunk , signal_chunk_spectrogram_data

	dummy_vector = [0.0, len_dummy / (fs)]
	freq_vector = [-(fs/2) + fc, (fs/2) + fc]
	PlotSpectrogram(freq_vector, dummy_vector,spectrogram_data)

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

		GenerateSpectrogram(signal,fs,fc)

		plt.yticks([])
		plt.show()