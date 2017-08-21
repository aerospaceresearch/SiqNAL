"""
    **Author :** *Jay Krishna*

    This module saves the waterfall diagram of the entire signal by concatenating waterfall diagram of each second.

    Approach
    ---------------------------
    * Signal is broken down into slices of size specified.
    * For each signal slice

        * Rectangular window is chosen based of size according to overlaping factor.
        * Fast Fourier Transform is calculated whose zero frequency spectrum is shifted to the centre and length normalized.
        * Each fft is stacked over previous one.

"""

import numpy as np
import matplotlib.pyplot as plt

from Modules import SignalData
from Modules import fourier


def plot_waterfall(SignalInfo, chunksize, number):
    """
        Parameters
        ---------------------------
        SignalInfo : object
            Instance of class SignalData.
        chunksize : int
            Size of one signal chunk processed each time, preferred 
            power of two for faster FFT computation.
        number : int
            Number of rows to be interleaved to help reduce memory consumption.

    """

    signal = SignalInfo.filedata
    len_signal = len(signal)
    chunknumber = int(len_signal // chunksize)

    for i in range(0, chunknumber):

        startslice = i * chunksize
        endslice = startslice + chunksize

        signal_chunk = signal[startslice:endslice]
        signal_chunk_iq = np.empty(
            signal_chunk.shape[0] // 2, dtype=np.complex64)

        signal_chunk_iq.real = signal_chunk[::2] - 127.5
        signal_chunk_iq.imag = signal_chunk[1::2] - 127.5

        ''' fft start + shifting '''
        signalFFT = fourier.CalcFourier(
            signal_chunk_iq)

        ''' fft shifted signal power '''
        frequency, transform = fourier.CalcFourierPower(
            signalFFT / len(signalFFT), SignalInfo.Fsample, SignalInfo.Fcentre)

        if(i == 0):
            row = transform.shape[0]
            waterfall = np.zeros([chunknumber, row], dtype=np.float32)
        waterfall[chunknumber - i - 1] = transform

        del signal_chunk, signal_chunk_iq, signalFFT, frequency, transform

    waterfall = np.flip(waterfall, axis=0)
    time_vector = [0.0, int(len_signal // int(2 * SignalInfo.Fsample))]
    freq_vector = [-(SignalInfo.Fsample / 2) + SignalInfo.Fcentre,
                   (SignalInfo.Fsample / 2) + SignalInfo.Fcentre]
    plt.imshow(waterfall[::number], extent=freq_vector +
               time_vector, origin='lower', aspect='auto')
    # plt.gca().invert_yaxis()
    plt.colorbar()
    plt.savefig(SignalInfo.filename + ".png", dpi=1600)
    plt.clf()
    # plt.show()

    del time_vector, freq_vector, waterfall