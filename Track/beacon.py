"""
    **Author :** *Jay Krishna*
    
    This module detects the presence of signal sent by beacon. Dynamic thresholding is applied based upon leading & lagging cells.

    Approach
    ----------------------------
     
    * Signal is broken down in chunks of one second each.
    * At each point of smaller signal threshold is calculated based upon average of lagging & leading reference cells after removing guard cells from both sides.
    * Point where APRS signal is suppossed to start is found & checked against peak induced by random noise.

    Reference
    ------------------------------
    
    `Barkat, Mourad & Varshney, P.K (1987). On adaptive cell-averaging CFAR (Constant False-Alarm Rate) radar signal detection. Final Technical Report, Jun. 1984 - Dec. 1986 Syracuse Univ., NY. Dept. of Electrical and Computer Engineering <https://goo.gl/15t64a>`_

"""

import numpy as np
from scipy import signal
import math

from Modules import SignalData


def merge(peak, signal):
    """

        Parameters
        -----------------------
            peak : list
                Points of presence of beacon.
            signal : ndarray
                Numpy array of signal.
        
        Returns
        -------------------------
            final_peak : list
                Points of presence of beacon after merging nearby peaks.
                
    """

    final_peak = []
    start = 0

    for end in range(1, peak.shape[0]):
        if(peak[end] - peak[end - 1] < 200):
            pass
        else:
            point = peak[start] + np.argmax(signal[peak[start]:peak[end - 1]])
            final_peak.append(point)
            start = end

    if(start == 0):
        point = peak[start] + np.argmax(signal[peak[start]:peak[end - 1]])
        final_peak.append(point)

    if(peak[start] > final_peak[-1]):
        point = peak[start] + np.argmax(signal[peak[start]:peak[end - 1]])
        final_peak.append(point)

    return final_peak


def radar_detect(radar, signal):
    """

        Parameters
        -----------------------
            radar : ndarray
                Threshold values calculated at each point.
            signal : ndarray
                Numpy array of signal.
        
        Returns
        -------------------------
            peak : list
                Points of presence of beacon.
                
    """

    peak = []
    for i in range(signal.shape[0]):

        if(signal[i] > radar[i]):
            peak.append(i)

    peak = np.array(peak, dtype=int)

    if(peak.shape[0] > 1):
        peak = merge(peak, signal)

    return peak


def cfar(signal, refLength=1000, guardLength=100, p=0.01):
    """
        Parameters
        -----------------------
            signal : ndarray
                Numpy complex array of signal.
            refLength : int
                Length of reference cells
            guardLength : int
                Length of guard cells
            p : float
                Accepted probability of false alarm.

        Returns
        -----------------------
            point : int
                Starting point of aprs signal if present.

    """

    N = 2 * refLength
    alpha = (math.pow(p, -1 / N) - 1) * N

    cfarWin = np.ones(((refLength + guardLength) * 2 + 1, 1))
    cfarWin[refLength + 1:refLength + 1 + 2 * guardLength] = 0
    cfarWin = cfarWin / sum(cfarWin)
    signal = np.reshape(signal, (signal.shape[0], 1))
    noiseLevel = signal.fftconvolve(signal, cfarWin, 'same')
    cfarThreshold = noiseLevel * alpha

    cfarThreshold[:refLength] = cfarThreshold[:refLength] * 3
    cfarThreshold[cfarThreshold.shape[0] -
                  refLength:] = cfarThreshold[cfarThreshold.shape[0] - refLength:] * 3

    peak = radar_detect(cfarThreshold, signal)

    del noiseLevel, cfarWin, signal

    return peak


def check(SignaIInfo, signal):
    """

        Parameters
        -----------------------
            SignalInfo : object
                Instance of class SignalData having meta-data of file and signal.
            signal : ndarray
                Numpy complex array of signal.

        Returns
        ------------------------------
            points : list
                List of starting index of aprs signal.

    """

    value = SignaIInfo.getvalues()

    fs = value[3]
    chunksize = int(fs)
    chunknumber = int((signal.shape[0]) // chunksize)

    points = []

    for i in range(chunknumber):
        start = i * chunksize
        end = start + chunksize

        hay = np.absolute(signal[start:end])
        point = cfar(hay)

        for peak in point:
            final_point = start + peak
            points.append(final_point)

    return points
