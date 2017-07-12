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
from Modules import spectrogram
from Modules import power


def singlefile():

    SignalInfo = selectfile.select()

    if SignalInfo.filetype == ".dat":
        SignalInfo.filedata = read_dat.loaddata(SignalInfo.filename)
    else:
        SignalInfo.filedata = read_wav.loaddata(SignalInfo.filename)

    signal = SignalInfo.filedata
    # twice, because of i and q in one chunk
    #chunksize = int(SignalInfo.Fsample) * 2
    chunksize = int(1024 * 64)
    len_signal = len(signal)
    chunknumber = int(len_signal // chunksize)

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

        ''' fft start '''

        frequency, transform = fourier.CalcFourier(
            signal_chunk_iq, SignalInfo.Fsample, SignalInfo.Fcentre)

        plt.plot(frequency, transform)
        plt.axvline(x=SignalInfo.Fcentre, color='r', linestyle='-')
        plt.show()

    #     if i == 0:
    #         row_dimension = transform.shape[0]
    #         waterfall_data = np.zeros(
    #             [chunknumber, row_dimension], dtype=np.float32)
    #         waterfall_data[i] = transform
    #     else:
    #         waterfall_data[i] = transform

    # #waterfall_data=np.flip(waterfall_data,0)
    # time_vector = [0.0, chunknumber]
    # freq_vector = [-(SignalInfo.Fsample / 2) + SignalInfo.Fcentre,
    #                (SignalInfo.Fsample / 2) + SignalInfo.Fcentre]
    # # print(waterfall_data.shape)
    # img = plt.imshow(waterfall_data, extent=freq_vector + time_vector,
    #                  origin='lower', aspect='auto')
    # plt.colorbar()
    # plt.show()

    # Approach 2
    #spectrogram.SpectrogramPlot(SignalInfo, 'plt.cm.inferno')


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
