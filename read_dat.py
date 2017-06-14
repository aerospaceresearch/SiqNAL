import numpy as np


def loaddata(filename):

    try:

        signal = np.memmap(filename, dtype='uint8', mode='r', offset=44)
        return signal

    except:

        return None
