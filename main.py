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
from Modules import aprs
from Modules import beacon
from Modules import apt


def analysis(SignalInfo):

    filename = 'satellite_db.json'
    bands = freqbands.getbands(SignalInfo, filename)
    print(bands)
    chunksize = int(1024 * 2 * 2 * 2 * 2 * 2 * 2 * 2)
    # waterfall.plot_waterfall(SignalInfo, chunksize, 30)

    peaks = []
    is_peaks_all = False
    fc = SignalInfo.Fcentre
    fs = SignalInfo.Fsample

    for band in bands:

        name = band[0]
        FLow = band[1]
        FHigh = band[2]
        description = band[3]
        # print(band, FLow, FHigh)

        if(fc - fs / 2 < FLow and fc + fs / 2 > FHigh):

            signal_filtered = bandpass.filter_box(
                SignalInfo, FLow, FHigh, chunksize)

            if("APT" in description):
                # print("NOAA")
                is_present = apt.check(SignalInfo, signal_filtered)
                peaks = "NOAA Present"
                # print(is_present==True)
                if(is_present == True):
                    is_peaks_all = True
                    # Data kept in json format
                    data = ({"Peaks": True}, {"Band Name": name}, {"FLow": FLow}, {
                        "FHigh": FHigh}, {"Description": description})
                else:
                    data = ({"Peaks": False}, {"Band Name": name}, {"FLow": FLow}, {
                        "FHigh": FHigh}, {"Description": description})

            elif("beacon" in description):
                # For Beacon like funcube
                points = beacon.check(SignalInfo, signal_filtered)
                if(len(points) > 0):
                    is_peaks_all = True
                    # Data kept in json format
                    data = ({"Peaks": True}, {"Band Name": name}, {"FLow": FLow}, {
                            "FHigh": FHigh}, {"Description": description}, {"Points": points})
                    peaks.append({SignalInfo.filename: data})
                else:
                    data = ({"Peaks": False}, {"Band Name": name}, {"FLow": FLow}, {
                            "FHigh": FHigh}, {"Description": description}, {"Points": []})
                    peaks.append({SignalInfo.filename: data})

            else:
                # For APRS
                points = aprs.check(SignalInfo, signal_filtered)
                if(len(points) > 0):
                    is_peaks_all = True
                    # Data kept in json format
                    data = ({"Peaks": True}, {"Band Name": name}, {"FLow": FLow}, {
                            "FHigh": FHigh}, {"Description": description}, {"Points": points})
                    peaks.append({SignalInfo.filename: data})
                else:
                    data = ({"Peaks": False}, {"Band Name": name}, {"FLow": FLow}, {
                            "FHigh": FHigh}, {"Description": description}, {"Points": []})
                    peaks.append({SignalInfo.filename: data})

            del signal_filtered

    return peaks, is_peaks_all


def singlefile():

    SignalInfo = selectfile.select()

    if SignalInfo.filetype == ".dat":
        SignalInfo.filedata = read_dat.loaddata(SignalInfo.filename)
    else:
        SignalInfo.filedata = read_wav.loaddata(SignalInfo.filename)

    peaks, is_peaks = analysis(SignalInfo)
    print(peaks)


def folderwatch():
    foldername = selectfolder.select()

    #laststamp = -1
    while True:
        contents = os.listdir(foldername)
        process = []
        for content in contents:
            if(content.endswith('.dat') or content.endswith('.wav')):
                duplicate = 0
                for content1 in contents:
                    if content + ".png" == content1:
                        # we assume that as soon as the waterfall graph image is there, it was already processed
                        duplicate = 1

                if duplicate == 0:
                    process.append(join(foldername, content))

        for file in process:
            SignalInfo = importfile.loadfile(file)

            if SignalInfo.filetype == ".dat":
                SignalInfo.filedata = read_dat.loaddata(SignalInfo.filename)
            else:
                SignalInfo.filedata = read_wav.loaddata(SignalInfo.filename)

            peaks, is_peaks = analysis(SignalInfo)

            if(not is_peaks):
                print("Deleted " + str(SignalInfo.filename))
                del SignalInfo.filedata
                os.remove(SignalInfo.filename)
                os.remove(SignalInfo.filename.split(".")[0] + ".json")

        print(time.time(), "waiting for new file...")
        time.sleep(10)


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
