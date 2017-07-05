"""
    **Author :** *Jay Krishna*

    This module implements linear phase finite impule response (FIR) butterworth bandpass filter
    using Frequency shift theorem and symmetricity of the filter. The computed signal after 
    applying bandpass filter is then stoared as (.txt) file.

    Approach
    ----------------------------
    #. First of all the centre frequency of signal is shifted from current centre frequency(fc) to mean of lower and higher frequency cutoff.
    #. A linear phase finite impule response (FIR) butterworth bandpass filter is constructed of width half of passband width.
    #. After filtering the signal is again shifted back to the previous centre frequency.

    Note
    ------------------------------
    #. Frequency Shift Theorem
        The frequency shift theorem states that, if

        .. math:: x(t) = X( \omega )

        then,

        .. math:: x(t) e^{(j \omega_o t)} = X( \omega - \omega_o)

        where,

        .. math:: \omega_o = 2 \pi F_o / F_{sample}

        :math:`F_o` is in it's equivalent baseband counterpart.

    #. Width of the filter
        Linear Phase filters are symmetric around the centre frequency of the signal. Since the centre frequency of the new signal is average of \
        lower and higher frequency cutoffs. Hence, the width of the filter is kept half of the passband width.
"""
from PyQt4 import QtGui

import os
from os import path
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter, lfilter

from Modules import fourier
from Modules import SignalData


def calc_parameter(flow, fhigh, fc, fs):
    """
        This function calculates the width of the filter and the multiplying
        factor for the shifting of the signal to the required centre frequency.

        Parameters
        ----------------------------
            flow : float
                Lower cutoff frequency for bandpass filter.
            fhigh : float
                Higher cutoff frequency for bandpass filter.
            fc : float
                Center frequency of the signal.
            fs : float
                Sampling frequency of the signal.

        Returns
        ------------------------------
            multiplier : float
                Shifting coefficient for the frequency shift. 
            width : float
                Width of the filter to be constructed.
    """

    centre = ((flow + fhigh) / 2) - fc
    width = np.ceil((fhigh - flow) / 2)
    multiplier = -1 * centre / fs

    return multiplier, width


def butter_bandpass_filter(data, width, fs):
    """
        This function constructs as well as applies the specified 
        linear phase finite impule response (FIR) butterworth 
        bandpass filter to the given shifted signal. The order of 
        the filter is automatically selected based upon the value of 
        *(Width of the filter / Nyquist Smapling frequency)*.

        Parameters
        ----------------------------
            data : ndarray
                Numpy complex array of shifted signal.
            width : float
                Width of the filter to be constructed.
            fs : float
                Sampling frequency of the signal.

        Returns
        ------------------------------
            y : ndarray
                Numpy complex array of filtered and shifted signal.

    """
    nyq = 0.5 * fs
    val = width / nyq

    if val < 0.002:
        val = 0.002
    if val >= 0.25:
        order = 21
    if val >= 0.025 and val < 0.25:
        order = 11

    b, a = butter(order, val, btype='low')
    y = lfilter(b, a, data)

    return y


def createfile(filename):
    """
        This function creates a (.txt) file with specified name in the
        current working directory which is used to store the filtered
        signal from the bandpass filter. If file with same name already
        exists first it is deleted.

        Parameters
        ---------------------------------
            filename : string
                Name of the file which will be created to store filtered
                signal.
        Returns
        ----------------------------------
            filepath : file object
                Absolute path to the (.txt) file created.
    """
    data_directory = os.getcwd()
    filepath = path.join(data_directory, filename)

    try:
        os.remove(filename)
    except:
        pass

    filepointer = open(filepath, 'w+')
    filepointer.close()

    return filepath


def WriteData(filename, data, i):
    """
        This function stores the filtered signal in memory-mapped (.txt) 
        format file. 

        Parameters
        ------------------------------
            filename : string
                Absolute path to the (.txt) file.
            data : ndarray
                Numpy complex array of filtered signal.
            i : int
                Iteration value used for calculation of offset.
    """
    shape = data.shape
    offset = data.nbytes * i

    file = np.memmap(filename, dtype="complex128",
                     mode="r+", shape=shape, offset=offset)
    file[:] = data

    del file


def filter(SignalInfo, Flow, Fhigh, filename, WaitWindow):
    """
        Driver function of bandpass filtering. Signal is read at the rate of
        per second, shifted to the desired centre frequency, linear phase
        finite impulse response (FIR) butterworth bandpass filter is applied, 
        signal is reshifted back and written to a (.txt) file.

        Parameters
        -----------------------
            SignalInfo : object
                Instance of class SignalData having meta-data of file and signal.
            Flow : float
                Lower cutoff frequency for bandpass filter.
            Fhigh : float
                Higher cutoff frequency for bandpass filter.
            filename : string
                Name of the (.txt) file used for storing filtered signal.
            WaitWindow : object
                Instance of WaitScreen

    """

    filename = createfile(filename)
    value = SignalInfo.getvalues()
    signal = value[2]

    if(value[1] == ".wav"):
        factor = 1
    else:
        factor = 2

    fs = value[3]
    fc = value[4]
    chunksize = int(fs)
    len_signal = len(signal)
    chunknumber = int(len_signal // (factor * chunksize))

    multiplier, width = calc_parameter(Flow, Fhigh, fc, fs)
    t_power = np.arange(chunksize)

    WaitWindow.show()

    for i in range(0, chunknumber):

        WaitWindow.updateprogress(i, chunknumber)

        start = i * factor * chunksize
        end = start + factor * chunksize

        if(value[1] == ".wav"):
            signal_chunk = signal[start:end, :]
            signal_chunk = signal_chunk.flatten()
        else:
            signal_chunk = signal[start:end]

            signal_chunk = signal_chunk - 127.5

        signal_chunk_iq = np.empty(
        signal_chunk.shape[0] // 2, dtype=np.complex128)
        signal_chunk_iq.real = signal_chunk[::2]
        signal_chunk_iq.imag = signal_chunk[1::2]

        signal_chunk_iq_new = signal_chunk_iq * \
        (np.exp(1j * 2 * np.pi * t_power * (multiplier)))

        final = (butter_bandpass_filter(signal_chunk_iq_new, width, fs)
        ) * (np.exp(1j * 2 * np.pi * t_power * (-1 * multiplier)))

        WriteData(filename, final, i)

        del final, signal_chunk_iq, signal_chunk
