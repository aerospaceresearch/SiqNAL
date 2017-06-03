import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import cmath
from os import path
import scipy.io.wavfile
from scipy.fftpack import fft,fftshift
from scipy import signal
from scipy.signal import fftconvolve
import fourier
from scipy.signal.signaltools import get_window

def firwin_custom(numtaps, cutoff, width=None, window='hamming', pass_zero=True,scale=True, nyq=1.0):

	cutoff = np.atleast_1d(cutoff) / float(nyq)

	# Check for invalid input.
	if cutoff.ndim > 1:
	    raise ValueError("The cutoff argument must be at most "
	                     "one-dimensional.")
	if cutoff.size == 0:
	    raise ValueError("At least one cutoff frequency must be given.")
	if cutoff.min() <= 0 or cutoff.max() >= 1:
	    raise ValueError("Invalid cutoff frequency: frequencies must be "
	                     "greater than 0 and less than nyq.")
	if np.any(np.diff(cutoff) <= 0):
	    raise ValueError("Invalid cutoff frequencies: the frequencies "
	                     "must be strictly increasing.")

	if width is not None:
	    # A width was given.  Find the beta parameter of the Kaiser window
	    # and set `window`.  This overrides the value of `window` passed in.
	    atten = kaiser_atten(numtaps, float(width) / nyq)
	    beta = kaiser_beta(atten)
	    window = ('kaiser', beta)

	pass_nyquist = bool(cutoff.size & 1) ^ pass_zero
	if pass_nyquist and numtaps % 2 == 0:
	    raise ValueError("A filter with an even number of coefficients must "
	                     "have zero response at the Nyquist rate.")

	# Insert 0 and/or 1 at the ends of cutoff so that the length of cutoff
	# is even, and each pair in cutoff corresponds to passband.
	cutoff = np.hstack(([0.0] * pass_zero, cutoff, [1.0] * pass_nyquist))

	# `bands` is a 2D array; each row gives the left and right edges of
	# a passband.
	bands = cutoff.reshape(-1, 2)

	# Build up the coefficients.
	alpha = 0.5 * (numtaps - 1)
	m = np.arange(0, numtaps) - alpha
	h = 0
	for left, right in bands:
	    h += right * np.sinc(right * m)#*np.exp(1j*2*np.pi*1)
	    h -= left * np.sinc(left * m)#*np.exp(1j*2*np.pi*1)

	# Get and apply the window function.
	#from .signaltools import get_window
	win = get_window(window, numtaps, fftbins=False)
	h *= win

	# Now handle scaling if desired.
	if scale:
	    # Get the first passband.
	    left, right = bands[0]
	    if left == 0:
	        scale_frequency = 0.0
	    elif right == 1:
	        scale_frequency = 1.0
	    else:
	        scale_frequency = 0.5 * (left + right)
	    c = np.cos(np.pi * m * scale_frequency)
	    s = np.sum(h * c)
	    h /= s

	return h

def firwin_bandpass_filter(data, lowcut, highcut, fs,fc,num):
	nyq = 0.5 * fs
	centre=(highcut+lowcut)/2-fc
	print(centre)
	width=np.ceil((highcut-lowcut)/2)

	h = firwin_custom(num,width,nyq=nyq,window='hanning')
	h = np.append(h,np.zeros(1024-len(h)))

	t=np.arange(len(h))
	h=h*(np.exp(1j*2*np.pi*t*(centre/fs)))

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

		final=firwin_bandpass_filter(signal_chunk_iq,138.15*1e6,138.65*1e6,fs,fc,num=513)

		plt.rcParams["figure.figsize"] = (16,6)
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