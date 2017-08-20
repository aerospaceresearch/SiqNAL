"""
    Reference: www.researchgate.net/publication/252378206_On_adaptive_cell-averaging_CFAR_Constant_False-Alarm_Rate_radar_signal_detection
"""


import numpy as np
from scipy import signal
import math

from Modules import SignalData


def merge(peak, autocor):
    final_peak = []
    start = 0

    for end in range(1, peak.shape[0]):
        if(peak[end] - peak[end - 1] < 200):
            pass
        else:
            point = peak[start] + np.argmax(autocor[peak[start]:peak[end - 1]])
            final_peak.append(point)
            start = end

    if(start == 0):
        point = peak[start] + np.argmax(autocor[peak[start]:peak[end - 1]])
        final_peak.append(point)

    if(peak[start] > final_peak[-1]):
        point = peak[start] + np.argmax(autocor[peak[start]:peak[end - 1]])
        final_peak.append(point)

    return final_peak


def radar_detect(radar, autocor):

    peak = []
    for i in range(autocor.shape[0]):

        if(autocor[i] > radar[i]):
            peak.append(i)

    peak = np.array(peak, dtype=int)

    if(peak.shape[0] > 1):
        peak = merge(peak, autocor)

    return peak


def cfar(autocor, refLength=1000, guardLength=100, p=0.01):

    N = 2 * refLength
    alpha = (math.pow(p, -1 / N) - 1) * N

    cfarWin = np.ones(((refLength + guardLength) * 2 + 1, 1))
    cfarWin[refLength + 1:refLength + 1 + 2 * guardLength] = 0
    cfarWin = cfarWin / sum(cfarWin)
    autocor = np.reshape(autocor, (autocor.shape[0], 1))
    noiseLevel = signal.fftconvolve(autocor, cfarWin, 'same')
    cfarThreshold = noiseLevel * alpha

    cfarThreshold[:refLength] = cfarThreshold[:refLength] * 3
    cfarThreshold[cfarThreshold.shape[0] -
                  refLength:] = cfarThreshold[cfarThreshold.shape[0] - refLength:] * 3

    peak = radar_detect(cfarThreshold, autocor)

    del noiseLevel, cfarWin, autocor

    return peak


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

        for peak in point:
            final_point = start + peak
            points.append(final_point)

    return points
