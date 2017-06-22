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
import matplotlib as mlp
from scipy.signal.signaltools import get_window
from matplotlib.colors import LinearSegmentedColormap


def waterfallspect(data, fc, fs, fft_size, overlap_fac):

    hop_size = np.int32(np.floor(fft_size * (1 - overlap_fac)))
    pad_end_size = fft_size

    total_segments = np.int32(np.ceil(len(data) / np.float32(hop_size)))
    t_max = len(data) / np.float32(fs)

    window = np.hanning(fft_size)
    inner_pad = np.zeros(fft_size)

    proc = np.concatenate((data, np.zeros(pad_end_size)))
    result = np.empty((total_segments, fft_size),
                      dtype=np.float32)

    for i in range(total_segments):
        current_hop = hop_size * i
        segment = proc[current_hop:current_hop +
                       fft_size]
        windowed = segment * window
        padded = np.append(windowed, inner_pad)
        spectrum = fftshift(fft(windowed)) / fft_size
        result[i, :] = np.absolute(spectrum[:])

    result = (20 * np.log10(result))

    return result


def LoadData(filename):

    try:

        rate, signal = scipy.io.wavfile.read(filename, mmap=True)
        signal = signal[44:, :]
        #signal = np.memmap(filename, dtype='uint8', mode='r',offset=44)
        return signal

    except:

        return None


if __name__ == '__main__':

    filename = "/home/matrix/Desktop/siqnal/data/station1_yagi_SDRSharp_20170312_060959Z_137650kHz_IQ.wav"

    signal = LoadData(filename)

    if(type(signal) == None):

        print("Requested file not found !!!!!!")

    else:

        fs = 2 * 1e6
        fc = 137.65 * 1e6
        # fc=145.825*1e6

    chunksize = 2000000
    len_signal = len(signal)
    last = int(len_signal // (chunksize))

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

        if(i == 0):
            waterfall_data = waterfallspect(
                signal_chunk_iq, fc, fs, 8 * 4096, 0.5)
        else:
            waterfall_data = waterfall_data + \
                waterfallspect(signal_chunk_iq, fc, fs, 8 * 4096, 0.5)

    dummy_vector = [0.0, 10]
    freq_vector = [-(fs / 2) + fc, (fs / 2) + fc]
    waterfall_data = waterfall_data / last
    img = plt.imshow(waterfall_data, extent=freq_vector + dummy_vector,
                     origin='lower', interpolation='nearest', aspect='auto', cmap=plt.cm.magma)
    plt.colorbar()
    plt.yticks([])
    plt.show()
