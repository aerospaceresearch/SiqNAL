from Modules import SignalData

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import csd


def psd(signal, fs, fc, window='boxcar', nfft=None, detrend='constant', return_onesided=False, scaling='density', axis=-1):

    if window is None:
        window = 'boxcar'

    if nfft is None:
        nperseg = signal.shape[axis]
    elif nfft == signal.shape[axis]:
        nperseg = nfft
    elif nfft > signal.shape[axis]:
        nperseg = signal.shape[axis]
    elif nfft < signal.shape[axis]:
        s = [np.s_[:]] * len(signal.shape)
        s[axis] = np.s_[:nfft]
        signal = signal[s]
        nperseg = nfft
        nfft = None

    noverlap = 0

    frequency, pxx = csd(signal, signal, fs, window, nperseg,
                         noverlap, nfft, 'constant', return_onesided, scaling, axis)
    frequency = frequency + fc

    return pxx, frequency


def SignalPowerPlot(SignalInfo, start, end):

    value = SignalInfo.getvalues()
    signal = value[2]

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

    pxx, frequency = psd(
        signal_chunk_iq, value[3], value[4], scaling='spectrum')

    plt.rcParams["figure.figsize"] = (16, 6)
    fig = plt.figure()

    ax = fig.add_subplot(111)
    plt.gca().xaxis.grid(True)
    plt.gca().yaxis.grid(True)
    ax.set_title("Power Spectral Density of Signal")
    ax.set_xlabel('Frequency(Hz)')
    ax.set_ylabel('PSD')
    plt.plot(frequency, pxx)
    plt.show()
