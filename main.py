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
from Modules import freqbands


def singlefile():

    SignalInfo = selectfile.select()

    if SignalInfo.filetype == ".dat":
        SignalInfo.filedata = read_dat.loaddata(SignalInfo.filename)
    else:
        SignalInfo.filedata = read_wav.loaddata(SignalInfo.filename)

    filename = 'satellite_db.json'
    bands = freqbands.getbands(SignalInfo, filename)

    signal = SignalInfo.filedata
    # twice, because of i and q in one chunk
    chunksize = int(1024 * 2 * 2 * 2 * 2 * 2 * 2 * 2)
    len_signal = len(signal)
    chunknumber = int(len_signal // chunksize)

    for band in bands:
        FLow = band[1]
        FHigh = band[2]

        filter_array = bandpass.filter_box(SignalInfo, FLow, FHigh, chunksize)
        signal_filtered = np.zeros(chunknumber * chunksize, dtype=np.float)

        waterfall = []
        waterfall_filtered = []
        # signal_filtered = []

        for i in range(0, chunknumber):
            print(i)
            startslice = i * chunksize
            endslice = startslice + chunksize

            signal_chunk = signal[startslice:endslice]
            signal_chunk_iq = np.empty(
                signal_chunk.shape[0] // 2, dtype=np.complex128)

            signal_chunk_iq.real = signal_chunk[::2] - 127.5
            signal_chunk_iq.imag = signal_chunk[1::2] - 127.5

            ''' fft start + shifting '''
            signalFFT = fourier.CalcFourier(
                signal_chunk_iq)

            ''' fft shifted signal power '''
            frequency, transform = fourier.CalcFourierPower(
                signalFFT / len(signalFFT), SignalInfo.Fsample, SignalInfo.Fcentre)

            waterfall.append(transform)

            # Box filter
            new_signalFFT = signalFFT * filter_array
            new_signalFFT1 = new_signalFFT

            ''' fft shifted signal power '''
            frequency, transform = fourier.CalcFourierPower(
                new_signalFFT / len(new_signalFFT), SignalInfo.Fsample, SignalInfo.Fcentre)

            waterfall_filtered.append(transform)

            signal_back = (fourier.CalcIFourier(new_signalFFT1))

            start_index = i * chunksize
            end_index = start_index + chunksize
            signal_filtered[start_index:end_index -
                            1:2] = signal_back.real + 127.5
            signal_filtered[start_index +
                            1:end_index:2] = signal_back.imag + 127.5

            # for j in range(len(signal_back)):
            #     signal_filtered.append(int(signal_back.real[j] + 127.5))
            #     signal_filtered.append(int(signal_back.imag[j] + 127.5))

        n = 30
        plt.imshow(waterfall[::n], origin='lower', aspect='auto')
        plt.colorbar()
        plt.show()
        plt.imshow(waterfall_filtered[::n], origin='lower', aspect='auto')
        plt.colorbar()
        plt.show()

        # plt.plot(signal[:200000])
        # plt.plot(signal_filtered[:200000])
        # plt.show()

        del waterfall, waterfall_filtered, signal_filtered


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
