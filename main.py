import numpy as np
import os
import time
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join, getmtime
from scipy.fftpack import fft, fftshift

from Modules import read_dat
from Modules import read_wav
from Modules import selectfile
from Modules import SignalData
from Modules import importfile
from Modules import fourier
from Modules import bandpass


def singlefile():

    SignalInfo = selectfile.select()

    if SignalInfo.filetype == ".dat":
        SignalInfo.filedata = read_dat.loaddata(SignalInfo.filename)
    else:
        SignalInfo.filedata = read_wav.loaddata(SignalInfo.filename)

    signal = SignalInfo.filedata
    # twice, because of i and q in one chunk
    chunksize = int(1024 * 2 * 2 * 2 * 2 * 2 * 2 * 2)
    len_signal = len(signal)
    chunknumber = int(len_signal // chunksize)
    FLow = float((145.9 - 0.1) * 1e6)
    FHigh = float((145.9 + 0.1) * 1e6)

    filter_array = bandpass.filter_box(SignalInfo, FLow, FHigh, chunksize)
    plt.plot(filter_array.real)
    plt.plot(filter_array.imag)
    plt.show()

    waterfall = []
    waterfall_filtered = []
    signal_filtered = []

    for i in range(0, chunknumber):
        print(i)
        startslice = i * chunksize
        endslice = startslice + chunksize

        signal_chunk = signal[startslice:endslice]
        signal_chunk_iq = np.empty(
            signal_chunk.shape[0] // 2, dtype=np.complex128)
        # it is recorded as uint8 but sint8 is better
        signal_chunk_iq.real = signal_chunk[::2] - 127.5
        signal_chunk_iq.imag = signal_chunk[1::2] - 127.5

        ''' fft start + shifting '''
        signalFFT = fourier.CalcFourier(
            signal_chunk_iq)

        ''' fft shifted signal power '''
        frequency, transform = fourier.CalcFourierPower(
            signalFFT / len(signalFFT), SignalInfo.Fsample, SignalInfo.Fcentre)

        waterfall.append(transform)


        ########################
        # from here:
        # from here, each bandpass musst do this
        ''' filtering the signalFFT shifted signal by multiplying it with filter window (box,...) '''
        # next task, when other code is clean ;)

        # Box filter
        new_signalFFT = signalFFT * filter_array
        new_signalFFT1 = new_signalFFT
        #print(filter_array)

        ''' fft shifted signal power '''
        frequency, transform = fourier.CalcFourierPower(
            new_signalFFT / len(new_signalFFT), SignalInfo.Fsample, SignalInfo.Fcentre)

        waterfall_filtered.append(transform)

        # going back to time series with filtered signal
        signal_back = (fourier.CalcIFourier(new_signalFFT1))
        # the following is shitty, but the fasted to check the filter.
        for i in range(len(signal_back)):
            # going int again, because of memory and comparison reasons
            signal_filtered.append(int(signal_back.real[i] + 127.5))
            signal_filtered.append(int(signal_back.imag[i] + 127.5))

        # to here
        # this is where each bandpass loop should end....


    # waterfall[::n] i guess you can caclulate the number of n until memory is full
    plt.imshow(waterfall[::2], origin='lower', aspect='auto')
    plt.colorbar()
    plt.show()
    plt.imshow(waterfall_filtered[::2], origin='lower', aspect='auto')
    plt.colorbar()
    plt.show()

    plt.plot(signal[:200000])
    plt.plot(signal_filtered[:200000])
    plt.show()


def folderwatch():
    name = "/home/matrix/Desktop/aero/data"
    laststamp = -1
    while True:
        contents = os.listdir(name)
        process = []
        for content in contents:
            if(content.endswith('.dat') or content.endswith('.wav')):
                if (laststamp == -1):
                    process.append(join(name, content))
                else:
                    if(getmtime(join(name, content)) > laststamp):
                        process.append(join(name, content))

        laststamp = time.time()

        for file in process:
            SignalInfo = importfile.loadfile(file)

            if SignalInfo.filetype == ".dat":
                SignalInfo.filedata = read_dat.loaddata(SignalInfo.filename)
            else:
                SignalInfo.filedata = read_wav.loaddata(SignalInfo.filename)

            signal = SignalInfo.filedata
            chunksize = int(SignalInfo.Fsample)
            len_signal = len(signal)
            chunknumber = int(len_signal // chunksize)

            for i in range(0, chunknumber):

                startslice = i * chunksize
                endslice = startslice + chunksize

                signal_chunk = signal[startslice:endslice]
                signal_chunk_iq = np.empty(
                    signal_chunk.shape[0] // 2, dtype=np.complex128)
                signal_chunk_iq.real = signal_chunk[::2]
                signal_chunk_iq.imag = signal_chunk[1::2]

        # time.sleep(3)


def main():
    option = input("Do you want to launch single signal analysis [y/n] ? ")
    if option == "y" or option == "Y":
        singlefile()
    else:
        folderwatch()


if __name__ == "__main__":
    main()
