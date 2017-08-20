"""
    Reference: www.researchgate.net/publication/252378206_On_adaptive_cell-averaging_CFAR_Constant_False-Alarm_Rate_radar_signal_detection
"""


import numpy as np
from scipy import signal
import math

from Modules import SignalData


def radar_detect(diff, refLength, threshold_min=1.2, threshold_ratio=10, threshold_max=1.5):
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


def cfar(autocor, refLength=10000, guardLength=10, p=0.001):

    N = 2 * refLength
    alpha = (math.pow(p, -1 / N) - 1) * N

    autocor = np.reshape(autocor, (autocor.shape[0], 1))

    cfarWin = np.ones(((refLength + guardLength) * 2 + 1, 1))
    cfarWin[refLength:refLength + 1 + 2 * guardLength] = 0
    cfarWin[0:refLength] = -1
    cfarWin = cfarWin / sum(np.absolute(cfarWin))

    noiseLevel = signal.fftconvolve(autocor, cfarWin, 'same')
    cfarThreshold = noiseLevel * alpha
    cfarThreshold[:refLength] = 0
    cfarThreshold[cfarThreshold.shape[0] - refLength:] = 0

    point = radar_detect(cfarThreshold, refLength)

    del cfarThreshold, cfarWin, autocor

    return point


def check(SignaIInfo, signal):

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
