import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import cmath
from os import path
import scipy.io.wavfile
from scipy.fftpack import fft, fftshift  # ,fftconvolve
from scipy import signal
from scipy.signal import butter, lfilter, firwin, fftconvolve
import fourier


def butter_bandpass_filter(data, lowcut, highcut, fs, fc, order=15):
    nyq = 0.5 * fs
    low = (lowcut - fc) / nyq
    high = (highcut - fc) / nyq

    if(abs(low) < 0.05):
        b, a = butter(order, high, btype='low')

    else:
        b, a = butter(order, [low, high], btype='band')

    y = lfilter(b, a, data)
    return y


def LoadData(filename):

    try:

        rate, signal = scipy.io.wavfile.read(filename, mmap=True)
        signal = signal[44:, :]
        return signal

    except:

        return None


if __name__ == '__main__':

    data_directory = path.join(os.getcwd(), 'data')
    filename = path.join(
        data_directory, 'station1_yagi_SDRSharp_20170312_060959Z_137650kHz_IQ.wav')

    signal = LoadData(filename)

    if(type(signal) == None):

        print("Requested file not found !!!!!!")

    else:

        fs = 2 * 1e6
        fc = 137.65 * 1e6

    chunksize = 2000000

    last = 1

    for i in range(0, last):

        start = i * chunksize
        end = start + chunksize

        signal_chunk = signal[start:end, :]
        signal_chunk = signal_chunk.flatten()
        signal_chunk = signal_chunk - 127.5

        signal_chunk_iq = np.empty(
            signal_chunk.shape[0] // 2, dtype=np.complex128)
        signal_chunk_iq.real = signal_chunk[::2]
        signal_chunk_iq.imag = signal_chunk[1::2]

        final = butter_bandpass_filter(
            signal_chunk_iq, 138.15 * 1e6, 138.55 * 1e6, fs, fc)

        plt.rcParams["figure.figsize"] = (16, 6)
        fig = plt.figure()

        frequency, transform = fourier.CalcFourier(signal_chunk_iq, fs, fc)
        ax = fig.add_subplot(211)
        plt.gca().xaxis.grid(True)
        plt.gca().yaxis.grid(True)
        ax.set_xlabel('Frequency(MHz)')
        ax.set_ylabel('|X(f)|')
        plt.plot(frequency, transform)

        frequency1, transform1 = fourier.CalcFourier(final, fs, fc)
        ax = fig.add_subplot(212)
        plt.gca().xaxis.grid(True)
        plt.gca().yaxis.grid(True)
        ax.set_xlabel('Frequency(MHz)')
        ax.set_ylabel('|X(f)|')
        plt.plot(frequency1, transform1)

        plt.show()
