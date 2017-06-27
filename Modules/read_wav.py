import numpy as np
import scipy.io.wavfile


def loaddata(filename):

    try:

        rate, signal = scipy.io.wavfile.read(filename, mmap=True)
        signal = signal[44:, :]
        return signal

    except:

        return None