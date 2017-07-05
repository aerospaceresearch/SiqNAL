"""
    **Author :** *Jay Krishna*

    This module plots the waterfall diagram of the entire signal by concatenating waterfall diagram of each second.

    Approach
    ---------------------------
    * Signal is broken down into slices of 1 second
    * For each 1 second signal slice

        * Rectangular window is chosen based of size according to overlaping factor.
        * Each smaller section is windowed with hanning window function.
        * After windowing fft is calculated whose zero frequency spectrum is shifted to the centre and length normalized.
        * Each fft is superimposed over each other.

    * Each waterfall data is appended to an array. 



"""
from PyQt4 import QtGui

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftshift
import sys

from Modules import SignalData

from Screens import waitscreen


def waterfallspect(data, fc, fs, fft_size, overlap_fac=0.0):
    """
        This function computes waterfall of small segments of signal (i.e 1 second).
        Based upon overlap factor size of each slide is calculated & number of segments 
        are calculated. Each smaller segment is windowed using hanning window, length 
        normalized fft is calculated & superimposed.

        Parameters
        ----------------------
        data : ndarray
            Numpy complex array of signal.
        fc : float
            Centre frequency of the signal.
        fs : float
            Sampling frequency of the signal.
        fft_size : int
            Length of fft.
        overlap_fac : float
            Overlapin factor in fraction, optional. Default is 0.

        Returns
        -------------------------
        result : ndarray
            Numpy array of calculated waterfall values of signal segment.
    """

    hop_size = np.int32(np.floor(fft_size * (1 - overlap_fac)))

    total_segments = np.int32(np.ceil(len(data) // np.float32(hop_size)))
    t_max = len(data) / np.float32(fs)

    window = np.hanning(fft_size)

    for i in range(total_segments):
        current_hop = hop_size * i
        segment = data[current_hop:current_hop +
                       fft_size]
        windowed = segment * window
        spectrum = fftshift(fft(windowed)) / fft_size
        if (i==0):
        	result=np.absolute(spectrum)
        else:
        	result=result+ np.absolute(spectrum)

    result = (20 * np.log10(result))
    return result


def SpectrogramPlot(SignalInfo, cmapstr, WaitWindow):
    """
        Driver function for ploting of waterfall. Signal is sliced into signal of 
        one second and waterfall data is recorded in similar order. 

        Parameters
        ---------------------------
        SignalInfo : object
            Instance of class SignalData.
        cmapstr : string
            Matplotlib colormap to be used for the waterfall.
        WaitWindow : object
            Instance of WaitScreen.
    """

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
        WaitWindow.updateprogress(i, chunknumber)

        startslice = i * factor * chunksize
        endslice = startslice + factor * chunksize

        if(value[1] == ".wav"):
            signal_chunk = signal[startslice:endslice, :]
            signal_chunk = signal_chunk.flatten()
            signal_chunk = signal_chunk - 127.5
        elif(value[1] == ".dat"):
            signal_chunk = signal[startslice:endslice]
            signal_chunk = signal_chunk - 127.5
        else:
            signal_chunk_iq = signal[startslice:endslice]

        if(value[1] != ".txt"):
            signal_chunk_iq = np.empty(
                signal_chunk.shape[0] // 2, dtype=np.complex128)
            signal_chunk_iq.real = signal_chunk[::2]
            signal_chunk_iq.imag = signal_chunk[1::2]
        if(i == 0):
            waterfall_data_one_second = waterfallspect(signal_chunk_iq, fc, fs, nfft)
            rows=waterfall_data_one_second.shape[0]
            waterfall_data=np.zeros((chunknumber,rows),dtype=np.float32)
            waterfall_data[i] = waterfall_data_one_second
        else:
            waterfall_data[i] = waterfallspect(signal_chunk_iq, fc, fs, nfft)
        try:
            del signal_chunk_iq, signal_chunk
        except:
            pass

    WaitWindow.close()
    dummy_vector = [0.0, chunknumber]
    freq_vector = [-(fs / 2) + fc, (fs / 2) + fc]
    img = plt.imshow(waterfall_data, extent=freq_vector + dummy_vector,origin='lower', interpolation='nearest', aspect='auto', cmap=cmap)
    plt.title("Waterfall Diagram")
    plt.xlabel("Frequency")
    plt.ylabel("Time")
    plt.colorbar()
    plt.show()
