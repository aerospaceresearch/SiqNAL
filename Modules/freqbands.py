import json
from Modules import SignalData


def getbands(SignalInfo, filename):
    bands = []
    flow = SignalInfo.Fcentre - SignalInfo.Fsample / 2
    fhigh = SignalInfo.Fcentre + SignalInfo.Fsample / 2

    with open(filename) as json_data:
        data = json.load(json_data)

        for freq in data["Bands"]:
            lower = float(freq["Lower"]) * 1e6
            upper = float(freq["Upper"]) * 1e6

            if(lower > flow and upper < fhigh):
                bands.append((lower, upper))

    print(bands)
    return bands
