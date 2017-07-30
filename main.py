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
    waterfall = np.flip(waterfall, axis=0)
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

            # Box filter
            new_signalFFT = signalFFT * filter_array
            new_signalFFT1 = new_signalFFT

            ''' fft shifted signal power '''
            frequency, transform = fourier.CalcFourierPower(
                new_signalFFT / len(new_signalFFT), SignalInfo.Fsample, SignalInfo.Fcentre)

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

            # signal_filtered[start_index:end_index -
            #                 1:2] = signal_back.real + 127.5
            # signal_filtered[start_index +
            #                 1:end_index:2] = signal_back.imag + 127.5

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
        # m = 1000
        #signal_plot=((signal_filtered[::m] - 127.5)**2 + (signal_filtered[1::m] - 127.5)**2)**0.5

        n = 10 * 1000
        all_average = calc_average(signal_filtered, n)
        mn = np.mean(signal_filtered)
        std = np.std(signal_filtered)
        threshold = (mn + (mn + std)) / 2
        times, points = find_segs(
            all_average, threshold, 50, 20, float(SignalInfo.Fsample), n, signal_filtered)

        for k in range(len(points)):
            point = points[k][0]
            new_point = re_check(signal_filtered, point, threshold, n)
            # points[k][0] = new_point
            # times[k][0] = new_point / int(SignalInfo.Fsample)

        # Times => start time,end time (in seconds)
        # Points => start point,end point (in I/Q file)
        # np.savetxt('times.csv', times, fmt='%.5f')
        # np.savetxt('points.csv', points, fmt='%.0f')

        # for k in range(len(points)):
        #     point = points[k][0]
        #     diff = int(10*1000 / 2)
        #     test1 = int(point - diff)
        #     test2 = int(point + diff)
        #     print("{} {} {} {} {}".format(k, point, diff, test1, test2))
        #     small_signal = signal_filtered[test1:test2]
        #     # if(k==0):
        #     #     np.savetxt("first.txt",small_signal)
        #     plt.plot(small_signal)
        #     display = 'Signal Detected, Point= ' + str(point)
        #     plt.axvline(diff, color='r', label=display)
        #     plt.axhline(threshold, color='orange', label='Threshold')
        #     plt.legend()
        #     plt.show()

        del signal_filtered, waterfall_filtered


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


def find_segs(samples, threshold, min_dur, merge_dur, fs, n, signal_filtered):
    start = -1
    end = -1
    segments = []
    times = []
    points = []

    for idx, x in enumerate(samples):
        if start < 0 and x < threshold:
            pass
        elif start < 0 and x >= threshold and x > 1.2:
            start = idx
            end = idx
        elif start >= 0 and x >= threshold:
            end = idx
        elif start >= 0 and x < threshold:
            dur = end - start + 1

            if(dur > min_dur):
                if(len(segments) == 0):
                    segments.append([start, end, dur])
                    times.append([start * n / fs, end * n / fs])
                    points.append([int(start * n), int(end * n)])
                else:
                    start_prev = segments[-1][0]
                    end_prev = segments[-1][1]
                    dur_prev = segments[-1][2]

                    if(start - end_prev <= merge_dur):
                        segments[-1][1] = end
                        segments[-1][2] = end - start_prev + 1
                    else:
                        segments.append([start, end, dur])
                        times.append([start * n / fs, end * n / fs])
                        points.append([int(start * n), int(end * n)])

            start = -1
            end = -1

    if(start >= 0):

        dur = end - start + 1

        if(dur > min_dur):
            if(len(segments) == 0):
                segments.append([start, end, dur])
                times.append([start * n / fs, end * n / fs])
                points.append([int(start * n), int(end * n)])
            else:
                start_prev = segments[-1][0]
                end_prev = segments[-1][1]
                dur_prev = segments[-1][2]

                if(start - end_prev <= merge_dur):
                    segments[-1][1] = end
                    segments[-1][2] = end - start_prev + 1
                else:
                    segments.append([start, end, dur])
                    times.append([start * n / fs, end * n / fs])
                    points.append([int(start * n), int(end * n)])

    return times, points


def calc_average(signal_filtered, n):

    average = []
    for i in range(0, len(signal_filtered), n):
        average.append(np.mean(signal_filtered[i:i + n]))

    return average


# def re_check(signal, th, point):
#     print(point)
#     n = 50

#     if(signal[point] < th):
#         i = 0
#         print("1")
#         while(True):
#             start = point + i * n
#             end = start + n
#             if(np.mean(signal[start:end]) >= th):
#                 point = start
#                 break
#             else:
#                 i = i + 1
#     else:
#         i = 0
#         print("2")
#         while(True):
#             end = point - i * n
#             start = end - n
#             if(np.mean(signal[start:end]) <= th):
#                 point = end
#                 break
#             else:
#                 i = i + 1

#     return point

def re_check(signal, point, threshold, m):
    n = m
    point = int(point)
    print(point)
    option=0
    while(n >= 1):
        average_r = np.mean(signal[point:point + n])
        average_l = np.mean(signal[point - n:point])
        if(average_l >= threshold):
            option=1
            point = int((point + (point - n)) / 2)
        elif (average_r <= threshold):# or average_l < threshold):
            option=2
            point = int((point + (point + n)) / 2)
        elif(average_l < threshold and average_r >=threshold):
            option=3
            average_temp=np.mean(signal[point:point + n//4])
            if(average_temp <= 0.6*threshold):
                option=4
                point=int((point+(point+n//2))/2)
            elif(np.mean(average_temp) < threshold):
                option=5
                point=int((point+(point+n//4))/2)
        #print("{} {} {} {} {} {}".format(average_l, average_r, threshold, n, point,option))
        n = n // 2
    return point


def main():
    option = input("Do you want to launch single signal analysis [y/n] ? ")
    if option == "y" or option == "Y":
        singlefile()
    else:
        folderwatch()


if __name__ == "__main__":
    main()
