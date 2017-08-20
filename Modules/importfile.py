import json
import numpy as np
import os
from os.path import splitext

from Modules import SignalData


def loadfile(filename):
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
