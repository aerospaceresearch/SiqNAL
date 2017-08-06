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
from Modules import waterfall
from Modules import detect
from Modules import selectfolder


def analysis(SignalInfo):
    is_peaks_all = False
    filename = 'satellite_db.json'
    bands = freqbands.getbands(SignalInfo, filename)

    chunksize = int(1024 * 2 * 2 * 2 * 2 * 2 * 2 * 2)
    waterfall.plot_waterfall(SignalInfo, chunksize, 30)

    is_peaks_all = False
    for band in bands:

        FLow = band[1]
        FHigh = band[2]
        print(band, FLow, FHigh)

        signal_filtered = bandpass.filter_box(
            SignalInfo, FLow, FHigh, chunksize)

        print(len(signal_filtered), len(SignalInfo.filedata)/2)

        signal_filtered = np.absolute(signal_filtered)

        n = 10 * 1000
        all_average = detect.calc_average(signal_filtered, n)
        threshold = detect.calc_threshold(signal_filtered)
        times, points = detect.find_segs(
            all_average, threshold, 50, 20, float(SignalInfo.Fsample), n, signal_filtered)

        if(len(points) > 0):
            #is_peaks = True

            # if ONE band has peaks, we keep the file.
            # later, we will also distinguish on which bands it was
            is_peaks_all = True

        for k in range(len(points)):
            point = points[k][0]
            new_point = detect.re_check(signal_filtered, point, threshold, n)
            points[k][0] = new_point
            times[k][0] = new_point / int(SignalInfo.Fsample)

        print(band, len(points), is_peaks_all)

        for k in range(len(points)):
            point = points[k][0]
            diff = 5000
            test1 = int(point - diff)
            test2 = int(point + diff)
            print("{} {} {} {} {}".format(k, point, diff, test1, test2))
            small_signal = signal_filtered[test1:test2]
            plt.plot(small_signal)
            display = 'Signal Detected, Point= ' + str(point)
            plt.axvline(diff, color='r', label=display)
            plt.axhline(threshold, color='orange', label='Threshold')
            plt.legend()
            plt.show()

        del signal_filtered

    return is_peaks_all


def singlefile():

    SignalInfo = selectfile.select()

    if SignalInfo.filetype == ".dat":
        SignalInfo.filedata = read_dat.loaddata(SignalInfo.filename)
    else:
        SignalInfo.filedata = read_wav.loaddata(SignalInfo.filename)

    is_peaks = analysis(SignalInfo)
    print(is_peaks)


def folderwatch():
    foldername = selectfolder.select()

    laststamp = -1
    while True:
        contents = os.listdir(foldername)
        process = []
        for content in contents:
            if(content.endswith('.dat') or content.endswith('.wav')):
                if (laststamp == -1):
                    process.append(join(foldername, content))
                else:
                    if(getmtime(join(foldername, content)) > laststamp):
                        process.append(join(foldername, content))

        laststamp = time.time()

        for file in process:
            SignalInfo = importfile.loadfile(file)

            if SignalInfo.filetype == ".dat":
                SignalInfo.filedata = read_dat.loaddata(SignalInfo.filename)
            else:
                SignalInfo.filedata = read_wav.loaddata(SignalInfo.filename)

            is_peaks = analysis(SignalInfo)

            if(not is_peaks):
                print("Deleted " + str(SignalInfo.filename))
                del SignalInfo.filedata
                os.remove(SignalInfo.filename)
                os.remove(SignalInfo.filename.split(".")[0] + ".json")


def main():
    option = str(
        input("Do you want to launch single signal analysis (y/n) [n]? ") or "n")
    if option == "y" or option == "Y":
        singlefile()
    elif option == "n" or option == "N":
        folderwatch()
    else:
        pass


if __name__ == "__main__":
    main()
