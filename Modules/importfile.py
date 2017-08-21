"""
    **Author :** *Jay Krishna*

    This module reads the json file associated with a signal file for
    server version of this project.

"""
import json
import numpy as np
import os
from os.path import splitext

from Modules import SignalData

def loadfile(filename):
    """
        This function read the json file associated with the signal file and extract 
        centre frequency and sampling frequency of the signal file.
        
        Parameters
        -----------------------
            filename : string
                Absolute path of signal file whose associated json file need to be read.

        Returns
        ------------------------------
            SignalInfo : object
                Instance of class SignalData having meta-data of file and signal.

    """

    SignalMeta = SignalData.Signal()
    _, file_extension = os.path.splitext(filename)
    if file_extension == ".dat":
        json_filename = filename.replace(".dat", ".json")
    else:
        json_filename = filename.replace(".wav", ".json")
    with open(json_filename) as json_data:
        data = json.load(json_data)

        fs = float(data["samplingRate"])
        fc = float(data["centerFrequency"])

    SignalMeta.setvalues(filename=filename, filetype=file_extension,
                         filedata=None, Fsample=fs, Fcentre=fc)

    return SignalMeta
