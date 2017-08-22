"""
    **Author :** *Jay Krishna*
    
    This module detects the presence of signal sent following Automatic Packet Reporting System(APRS). Instead of having
    constant threshold, dynamic thresholding is applied based upon leading & lagging cells.

    Approach
    ----------------------------
     
    * Signal is broken down in chunks of one second each.
    * At each point of smaller signal threshold is calculated based upon difference of lagging & leading reference cells after removing guard cells from both sides.
    * Point where APRS signal is suppossed to start is found & checked against peak induced by random noise.

    Reference
    ------------------------------
    
    `Barkat, Mourad & Varshney, P.K (1987). On adaptive cell-averaging CFAR (Constant False-Alarm Rate) radar signal detection. Final Technical Report, Jun. 1984 - Dec. 1986 Syracuse Univ., NY. Dept. of Electrical and Computer Engineering <https://goo.gl/15t64a>`_

"""


import numpy as np
from scipy import signal
import math

from Modules import SignalData


def radar_detect(diff, refLength, threshold_min=1.2, threshold_ratio=10, threshold_max=1.5):
    """
        
        Based upon the values calculated start of APRS signal is detected while taking care of false results
        due to spikes induced by noise.

        Parameters
        -----------------------
            diff : ndarray
                Values calculated at each point
            refLength : int
                Length of reference cells
            threshold_min : float
                Minimum level of threshold
            threshold_ratio : float
                Minimum ratio of detected point and mean of signal chunk
            threshold_max : float
                Maximum value of local maxima to ensure false detection due to random spikes.
        
        Returns
        -------------------------
            point : int
                Starting point of aprs signal if present.
                
    """
    point = -1
    mn = -1
    min_point = np.argmin(diff)
    check_period = diff.shape[0] // 4

    if(abs(diff[min_point]) > threshold_min):
        mn = np.mean(np.absolute(
            diff[min_point - 2 * refLength:min_point - refLength]))
        if(abs(diff[min_point]) / mn > threshold_ratio):
            check_point = min(min_point + check_period, diff.shape[0])
            max_point = min_point + np.argmax(diff[min_point:check_point])
            max_value = diff[max_point]
            if(max_value < threshold_max):
                point = min_point

    return point


def cfar(signal, refLength=10000, guardLength=10, p=0.001):
    """
        Calculates threshold value for each point using leading & lagging cells
        while discarding leading & lagging guard cells. 

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

    signal = np.reshape(signal, (signal.shape[0], 1))

    cfarWin = np.ones(((refLength + guardLength) * 2 + 1, 1))
    cfarWin[refLength:refLength + 1 + 2 * guardLength] = 0
    cfarWin[0:refLength] = -1
    cfarWin = cfarWin / sum(np.absolute(cfarWin))

    noiseLevel = signal.fftconvolve(signal, cfarWin, 'same')
    cfarThreshold = noiseLevel * alpha
    cfarThreshold[:refLength] = 0
    cfarThreshold[cfarThreshold.shape[0] - refLength:] = 0

    point = radar_detect(cfarThreshold, refLength)

    del cfarThreshold, cfarWin, signal

    return point


def check(SignaIInfo, signal):
    """
        Breaks the signal into smaller chunks and send them
        sequentially for APRS signal detection.

        Parameters
        -----------------------
            SignalInfo : object
                Instance of class SignalData having meta-data of file and signal.
            signal : ndarray
                Numpy complex array of filtered signal.

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

        if(point > 0):
            final_point = start + point
            points.append(final_point)

    return points
