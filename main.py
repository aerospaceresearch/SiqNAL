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
    print(chunknumber)
    #waterfall = []
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
        # waterfall.append(transform)
        if(i == 0):
            row = transform.shape[0]
            waterfall = np.zeros([chunknumber, row], dtype=np.float32)
        waterfall[chunknumber - i - 1] = transform

    n = 30
    #waterfall = np.flip(waterfall, axis=0)
    time_vector = [0.0, int(len_signal // int(2 * SignalInfo.Fsample))]
    freq_vector = [-(SignalInfo.Fsample / 2) + SignalInfo.Fcentre,
                   (SignalInfo.Fsample / 2) + SignalInfo.Fcentre]
    plt.imshow(waterfall[::n], extent=freq_vector +
               time_vector, origin='lower', aspect='auto')
    plt.gca().invert_yaxis()
    plt.colorbar()
    plt.show()
    del waterfall

    for band in bands:
        FLow = band[1]
        FHigh = band[2]

        filter_array = bandpass.filter_box(SignalInfo, FLow, FHigh, chunksize)
        signal_filtered = np.zeros(
            chunknumber * (chunksize // 2), dtype=np.float)

        #waterfall = []
        #waterfall_filtered = []
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
            # frequency, transform = fourier.CalcFourierPower(
            #     signalFFT / len(signalFFT), SignalInfo.Fsample, SignalInfo.Fcentre)

            # waterfall.append(transform)

            # Box filter
            new_signalFFT = signalFFT * filter_array
            new_signalFFT1 = new_signalFFT

            ''' fft shifted signal power '''
            frequency, transform = fourier.CalcFourierPower(
                new_signalFFT / len(new_signalFFT), SignalInfo.Fsample, SignalInfo.Fcentre)

            # waterfall_filtered.append(transform)
            if(i == 0):
                row = transform.shape[0]
                waterfall_filtered = np.zeros(
                    [chunknumber, row], dtype=np.float32)
            waterfall_filtered[chunknumber - i - 1] = transform

            signal_back = (fourier.CalcIFourier(new_signalFFT1))

            # Instead of stoaring IQ values stoared absolute values directly
            start_index = i * (chunksize // 2)
            end_index = start_index + (chunksize // 2)
            signal_filtered[start_index:end_index] = np.absolute(signal_back)

            signal_filtered[start_index:end_index -
                            1:2] = signal_back.real + 127.5
            signal_filtered[start_index +
                            1:end_index:2] = signal_back.imag + 127.5

        n = 30
        #waterfall_filtered = np.flip(waterfall_filtered, axis=0)
        time_vector = [0.0, int(len_signal // int(2 * SignalInfo.Fsample))]
        freq_vector = [-(SignalInfo.Fsample / 2) + SignalInfo.Fcentre,
                       (SignalInfo.Fsample / 2) + SignalInfo.Fcentre]
        plt.imshow(waterfall_filtered[::n], extent=freq_vector +
                   time_vector, origin='lower', aspect='auto')
        plt.gca().invert_yaxis()
        plt.colorbar()
        plt.show()

        # time domain plot of the filtered signal
        '''  below portion is for selecting best threshold you can uncomment & plot signal with threshold lines to see which is best '''
        # m = 1000

        #signal_plot=((signal_filtered[::m] - 127.5)**2 + (signal_filtered[1::m] - 127.5)**2)**0.5
        # signal_plot=np.flipud(signal_filtered)

        # signal_plot=signal_filtered[::m]
        mn = np.mean(signal_filtered)
        # md=np.median(signal_filtered)
        st = np.std(signal_filtered)
        # th1=mn+3*st
        # th2=md+3*st
        th3 = mn + 2.5 * st
        # th4=md+2.5*st
        # th5=mn+2*st
        # th6=md+2*st

        # print("{} {} {} {} {} {}".format(th1,th2,th3,th4,th5,th6))
        # plt.plot(signal_plot)
        # plt.axhline(y=th1,color='black')
        # plt.axhline(y=th2,color='r')
        # plt.axhline(y=th3,color='m')
        # plt.axhline(y=th4,color='orange')
        # plt.axhline(y=th5,color='darkblue')
        # plt.axhline(y=th6,color='green')
        # plt.show()

        # Till here

        # Getting segments where there is signal
        start, end, dur, seg = silent_segs(signal_filtered, th3,
                                           float(SignalInfo.Fsample * 0.5))

        # np.savetxt('end.csv', end, fmt='%.0f')
        # np.savetxt('start.csv', start, fmt='%.0f')
        # np.savetxt('dur.csv', dur, fmt='%.0f')
        # np.savetxt('seg.csv', seg, fmt='%.0f')

        # plt.plot(signal[:100000])
        # plt.plot(signal_filtered[:100000])
        # plt.show()

        del signal_filtered  # waterfall_filtered, signal_filtered


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


def silent_segs(samples, threshold, min_dur):
    start = -1
    end = -1
    silent_segments = []
    starts = []
    ends = []
    durs = []
    for idx, x in enumerate(samples):
        if start < 0 and x < threshold:
            pass
        elif start < 0 and x >= threshold:
            start = idx
            end = idx
        elif start >= 0 and x >= threshold:
            end = idx
        elif start >= 0 and x < threshold:
            dur = end - start + 1
            starts.append(start)
            ends.append(end)
            durs.append(dur)

            if(dur > 500):
                if(len(silent_segments) == 0):
                    silent_segments.append([start, end, dur])
                else:
                    start_prev = silent_segments[-1][0]
                    end_prev = silent_segments[-1][1]
                    dur_prev = silent_segments[-1][2]

                    if(start - end_prev <= 0.0015 * dur_prev):
                        silent_segments[-1][1] = end
                        silent_segments[-1][2] = end - start_prev + 1
                    elif(start - end_prev <= 30):
                        silent_segments[-1][1] = end
                        silent_segments[-1][2] = end - start_prev + 1
                    else:
                        silent_segments.append([start, end, dur])

            start = -1
            end = -1

    if(start >= 0):

        dur = end - start + 1
        starts.append(start)
        ends.append(end)
        durs.append(dur)

        if(dur > 500):
            if(len(silent_segments) == 0):
                silent_segments.append((start, end, dur))
            else:
                start_prev = silent_segments[-1][0]
                end_prev = silent_segments[-1][1]
                dur_prev = silent_segments[-1][2]

                if(start - end_prev <= 0.0015 * dur_prev):
                    silent_segments[-1][1] = end
                    silent_segments[-1][2] = end - start_prev + 1
                if(start - end_prev <= 30):
                    silent_segments[-1][1] = end
                    silent_segments[-1][2] = end - start_prev + 1
                else:
                    silent_segments.append([start, end, dur])

    return starts, ends, durs, silent_segments


def main():
    option = input("Do you want to launch single signal analysis [y/n] ? ")
    if option == "y" or option == "Y":
        singlefile()
    else:
        folderwatch()


if __name__ == "__main__":
    main()
