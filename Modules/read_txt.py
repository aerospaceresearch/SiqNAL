import numpy as np


def loaddata(filename):

    try:

        signal = np.memmap(filename, dtype='complex128', mode='r')
        return signal

    except:

        return None
