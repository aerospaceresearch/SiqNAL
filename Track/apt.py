"""
    **Author :** *Jay Krishna*
    
    This module detects the presence of signal sent following Automatic Picture Transmission(APT). Since signal under APT is sent twice every
    second when under contact hence it significantly affects the statistical parameters of the signal hence statistical method is developed for detection.

    Approach
    ----------------------------
     
    * Signal is broken down in chunks of one second each.
    * For each smaller signal statistical values(mean, standard deviation and median) was calculated along with mean of whole signal file. 
    * Presence of signal is confirmed by evaluating the statistical distribution of signal relative to threshold. 

"""

import numpy as np
import math

from Modules import SignalData


def stat_check(values, threshold, chunknumber):
    """
        Based upon the threshold views the statistical distribution of
        points in signal file and concludes the presence of APT signal.

        Parameters
        -----------------------
            values : list
                Calculated statistical values of each small signals.
            threshold : float
                Calculated threshold for signal file.
            chunknumber : int
                Size of each smaller signal

        Returns
        ------------------------------
            is_present : bool
                Showing presence of APT signal.

    """

    is_present = False
    stat = []

    for i in range(1, 17, 2):
        measure = round(sum(values > (threshold / i)) / chunknumber, 2)
        stat.append(measure)

    if(stat[0] >= 0.5 and stat[1] >= 0.7 and stat[2] >= 0.8 and stat[3] >= 0.9 and stat[4] >= 0.95):
        is_present = True

    return is_present


def check(SignaIInfo, signal):
    """

        Breaks the signal into smaller chunks and calculates statistical parameters
        for each chunk. Also calculates mean of whole signal file.

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

    values = []
    total = 0

    for i in range(chunknumber):
        start = i * chunksize
        end = start + chunksize

        hay = np.absolute(signal[start:end])

        mean = np.mean(hay)
        std = np.std(hay)
        median = np.median(hay)
        total = total + sum(hay)

        value = (((mean) / std) * median)**2
        values.append(value)

    threshold = 10 * (total / (chunknumber * chunksize))

    is_present = stat_check(values, threshold, chunknumber)

    return is_present