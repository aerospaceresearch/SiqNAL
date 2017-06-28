from PyQt4 import QtGui

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftshift
import sys

from Modules import SignalData

from Screens import waitscreen


def PlotSpectrogram(freq_vector, dummy_vector, data, cmap, dbf=60):

    eps = 1e-3
    data_max = abs(data).max()

    data_log = 20.0 * np.log10(abs(data) / data_max + eps)
    display_data = (np.flipud(64.0 * (data_log + dbf) / dbf))

    fig = plt.figure(figsize=(16, 5))

    plt.imshow(display_data.T, extent=freq_vector + dummy_vector,
               aspect='auto', interpolation="nearest", cmap=cmap)
    plt.colorbar()
    plt.xlabel('Frequency (Hz)')
    plt.tight_layout()


def ShortTimeSpectrogram(signal, N, fs, fc):

    len_signal = len(signal)
    len_padding = (len_signal + N - 1) // N

    signal = np.append(signal, np.zeros(-len_signal + len_padding * N))
    signal = signal.reshape((N // 2, len_padding * 2), order='F')
    signal = np.concatenate((signal, signal), axis=0)
    signal = signal.reshape((N * len_padding * 2, 1), order='F')
    signal = signal[np.r_[N // 2:len(signal), np.ones(N // 2) * (
        len(signal) - 1)].astype(int)].reshape((N, len_padding * 2), order='F')

    signal_spectrogram = signal * np.hanning(N)[:, None]
    signal_spectrogram = fftshift(fft(
        signal_spectrogram, len(signal_spectrogram), axis=0), axes=0)

    return signal_spectrogram


def SpectrogramPlot(SignalInfo, cmapstr, WaitWindow):

    value = SignalInfo.getvalues()
    signal = value[2]
    nfft = 32768

    if("gray" in cmapstr):
        cmap = plt.cm.gray
    elif("magma" in cmapstr):
        cmap = plt.cm.magma
    elif("inferno" in cmapstr):
        cmap = plt.cm.inferno
    elif("viridis" in cmapstr):
        cmap = plt.cm.viridis
    else:
        cmap = plt.cm.plasma

    if(value[1] == ".dat"):
        factor = 2
    else:
        factor = 1

    fs = value[3]
    fc = value[4]
    chunksize = int(fs)
    len_signal = len(signal)
    chunknumber = int(len_signal // (factor * chunksize))

    WaitWindow.show()

    for i in range(0, chunknumber):

        startslice = i * factor * chunksize
        endslice = startslice + factor * chunksize

        if(value[1] == ".wav"):
            factor = 1
            startslice = start * factor * int(value[3])
            endslice = end * factor * int(value[3])
            signal_chunk = signal[startslice:endslice, :]
            signal_chunk = signal_chunk.flatten()
            signal_chunk = signal_chunk - 127.5
        elif(value[1] == ".dat"):
            factor = 2
            startslice = start * factor * int(value[3])
            endslice = end * factor * int(value[3])
            signal_chunk = signal[startslice:endslice]
            signal_chunk = signal_chunk - 127.5
        else:
            factor = 1
            startslice = start * factor * int(value[3])
            endslice = end * factor * int(value[3])
            signal_chunk_iq = signal[startslice:endslice]

    if(value[1] != ".txt"):
        signal_chunk_iq = np.empty(
            signal_chunk.shape[0] // 2, dtype=np.complex128)
        signal_chunk_iq.real = signal_chunk[::2]
        signal_chunk_iq.imag = signal_chunk[1::2]

        if (i == 0):
            spectrogram_data = ShortTimeSpectrogram(
                signal_chunk_iq, nfft, fs, fc)

        else:
            spectrogram_data = spectrogram_data + \
                ShortTimeSpectrogram(signal_chunk_iq, nfft, fs, fc)

        if(i == chunknumber - 1):
            len_dummy = len(signal_chunk_iq)

        del signal_chunk_iq, signal_chunk
        WaitWindow.updateprogress(i, chunknumber)

    spectrogram_data = spectrogram_data / chunknumber
    dummy_vector = [0.0, len_dummy / (fs)]
    freq_vector = [-(fs / 2) + fc, (fs / 2) + fc]

    WaitWindow.close()

    eps = 1e-3
    dbf = 60
    data_max = abs(spectrogram_data).max()

    data_log = 20.0 * np.log10(abs(spectrogram_data) / data_max + eps)
    display_data = (np.flipud(64.0 * (data_log + dbf) / dbf))

    plt.imshow(display_data.T, extent=freq_vector + dummy_vector,
               origin='lower', interpolation='nearest', aspect='auto', cmap=cmap)
    plt.colorbar()
    plt.xlabel('Frequency (Hz)')
    plt.tight_layout()
    plt.yticks([])
    plt.show()
