import numpy as np
import math

from Modules import SignalData


def stat_check(values, threshold, chunknumber):
    is_present = False
    stat = []

    for i in range(1, 17, 2):
        measure = round(sum(values > (threshold / i)) / chunknumber, 2)
        stat.append(measure)

    print(stat)
    if(stat[0] >= 0.5 and stat[1] >= 0.7 and stat[2] >= 0.8 and stat[3] >= 0.9 and stat[4] >= 0.95):
        is_present = True

    return is_present


def check(SignaIInfo, signal):

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
