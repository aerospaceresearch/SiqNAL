"""
    **Author :** *Jay Krishna*

    This module reads the json database of satellites & correspondingly
    populates list object for construction of bandpass filter and signal detection.

"""

import json
import os
from Modules import SignalData


def getbands(SignalInfo, filename):
    """
        This function go through the json database of satellites, read the meta data
        about them usch as name and transmission method used by them. It also
        reads about their transponder data particularly Downlink frequency
        along with width of frequency band used by them which is further corrected
        for doppler shift and stored. 

        Parameters
        -----------------------
            SignalInfo : object
                Instance of class SignalData having meta-data of file and signal.
            filename: str
                Absolute path to json satellite database.

        Returns
        ------------------------------
            bands : list
                List object containing meta data about each satellite.

    """
    bands = []
    flow = SignalInfo.Fcentre - SignalInfo.Fsample / 2
    fhigh = SignalInfo.Fcentre + SignalInfo.Fsample / 2

    file = os.path.join(os.getcwd(), filename)

    with open(file) as json_data:
        data = json.load(json_data)

        for sat in data["satellite"]:
            name = sat["name"]

            for transponder in sat["transponders"]:
                downlink = float(transponder["downlink"]) * 1e6
                width = float(transponder["downlinkWidth"]) * 1e6 / 2
                description = str(transponder["description"])
                doppler = 0.01 * 1e6

                lower = downlink - width - doppler
                upper = downlink + width + doppler

                if(lower > flow and upper < fhigh):
                    bands.append((name, lower, upper, description))

    return bands