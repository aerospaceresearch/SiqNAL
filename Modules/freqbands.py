import json
import os
from Modules import SignalData


def getbands(SignalInfo, filename):
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
                doppler = 0.01 * 1e6

                lower = downlink - width - doppler
                upper = downlink + width + doppler

                if(lower > flow and upper < fhigh):
                    bands.append((name, lower, upper))

    print(bands)
    return bands
