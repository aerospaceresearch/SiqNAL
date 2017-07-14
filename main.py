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
    print(chunknumber)
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
        signalFFT = signalFFT / len(signalFFT)

        FLow = float(144.7 * 1e6)
        FHigh = float(144.8 * 1e6)
        new_signaI = bandpass.filter(
            signal_chunk_iq, SignalInfo, FLow, FHigh, chunksize)

        new_signalFFT = fourier.CalcFourier(
            new_signaI)
        new_signalFFT = new_signalFFT / len(new_signalFFT)

        ''' fft shifted signal power '''
        frequency, transform = fourier.CalcFourierPower(
            new_signalFFT, SignalInfo.Fsample, SignalInfo.Fcentre)

        if i == 0:
            row_dimension = transform.shape[0]
            # Pre-allocation will make it faster
            waterfall_data = np.zeros(
                [chunknumber, row_dimension], dtype=np.float32)

        waterfall_data[i] = transform

        ''' filtering the signalFFT shifted signal by multiplying it with filter window (box,...) '''
        # next task, when other code is clean ;)

    n = 20
    time_vector = [0.0, int(len_signal // int(2 * SignalInfo.Fsample))]
    freq_vector = [-(SignalInfo.Fsample / 2) + SignalInfo.Fcentre,
                   (SignalInfo.Fsample / 2) + SignalInfo.Fcentre]
    waterfall_data = np.flip(waterfall_data, 0)
    new_waterfall_data = waterfall_data[::n]
    plt.imshow(new_waterfall_data, extent=freq_vector +
               time_vector, origin='lower', aspect='auto')
    plt.colorbar()
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
