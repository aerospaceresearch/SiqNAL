from PyQt4 import QtGui

import os
from os import path
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter, lfilter

from Modules import fourier
from Modules import SignalData


def calc_parameter(flow, fhigh, fc, fs=2 * 1e6):

    centre = ((flow + fhigh) / 2) - fc
    width = np.ceil((fhigh - flow) / 2)
    factor = -1 * centre / fs

    return factor, width


def butter_bandpass_filter(data, width, fs, order=7):
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
    shape = data.shape
    offset = data.nbytes * i

    file = np.memmap(filename, dtype="complex128",
                     mode="r+", shape=shape, offset=offset)
    file[:] = data

    del file


def filter(SignalInfo, Flow, Fhigh, filename, WaitWindow):

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
