import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import cmath
from os import path
import scipy.io.wavfile
from scipy.fftpack import fft, fftshift
from scipy import signal
from scipy.signal import fftconvolve
import fourier
import pylab
from scipy.signal.signaltools import get_window


def waterfallspect(data, fs, fft_size, overlap_fac):
    # data = a numpy array containing the signal to be processed
    # fs = a scalar which is the sampling frequency of the data

    hop_size = np.int32(np.floor(fft_size * (1 - overlap_fac)))
    # the last segment can overlap the end of the data array by no more than one window size
    pad_end_size = fft_size
    # print(np.float32(hop_size))

    total_segments = np.int32(np.ceil(len(data) / np.float32(hop_size)))
    t_max = len(data) / np.float32(fs)

    window = np.hanning(fft_size)  # our half cosine window
    # the zeros which will be used to double each segment size
    inner_pad = np.zeros(fft_size)

    proc = np.concatenate((data, np.zeros(pad_end_size))
                          )              # the data to process
    result = np.empty((total_segments, 2 * fft_size),
                      dtype=np.float32)    # space to hold the result

    for i in range(total_segments):                      # for each segment
        # figure out the current segment offset
        current_hop = hop_size * i
        segment = proc[current_hop:current_hop +
                       fft_size]  # get the current segment
        # multiply by the half cosine function
        windowed = segment * window
        # add 0s to double the length of the data
        padded = np.append(windowed, inner_pad)
        # take the Fourier Transform and scale by the number of samples
        spectrum = fftshift(fft(padded)) / fft_size
        # autopower = np.abs(spectrum * np.conj(spectrum))  # find the autopower spectrum
        # result[i, :] = autopower[:fft_size]               # append to the results array
        result[i, :] = abs(spectrum[:])

    result = 20 * np.log10(result)          # scale to db
    # result = np.clip(result, -40, 200)    # clip values
    img = plt.imshow(result, origin='lower',
                     interpolation='nearest', aspect='auto')
    plt.show()


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

    chunksize = 3 * 2000000

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

        waterfallspect(signal_chunk_iq, fs, 10 * 4096, 0.5)
