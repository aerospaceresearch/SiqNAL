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
import numpy as np
import matplotlib.pyplot as plt
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


def filter(signal, SignalInfo, Flow, Fhigh, chunksize):
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

    value = SignalInfo.getvalues()

    fs = value[3]
    fc = value[4]

    chunksize = int(chunksize // 2)
    multiplier, width = calc_parameter(Flow, Fhigh, fc, fs)
    t_power = np.arange(chunksize)

    signal_chunk_iq_new = signal * \
        (np.exp(1j * 2 * np.pi * t_power * (multiplier)))

    final = (butter_bandpass_filter(signal_chunk_iq_new, width, fs)
             ) * (np.exp(1j * 2 * np.pi * t_power * (-1 * multiplier)))

    return final


def filter_box(SignalInfo, Flow, Fhigh, chunksize):

    value = SignalInfo.getvalues()

    fs = value[3]
    fc = value[4]

    length = int(chunksize // 2)

    filter_array = np.ones(length, dtype=np.complex128) + 1j
    np.savetxt('filter1.csv', filter_array)
    freq = np.arange(fc - fs / 2, fc + fs / 2, fs / length)

    nlow = int((Flow - (fc - fs / 2)) // (fs / length))
    nhigh = int((Fhigh - (fc - fs / 2)) // (fs / length))
    if abs(Flow - freq[nlow]) > abs(Flow - freq[nlow + 1]):
        nlow = nlow + 1
    if abs(Fhigh - freq[nhigh]) > abs(Fhigh - freq[nhigh + 1]):
        nhigh = nhigh + 1

    filter_array[:nlow] = 0 + 0j
    filter_array[nhigh:] = 0 + 0j

    return filter_array
