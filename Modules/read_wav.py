"""
    **Author :** *Jay Krishna*

    This module read (.wav) file from physical storage as a memory-
    mapped file.

"""

import numpy as np
import scipy.io.wavfile


def loaddata(filename):
    """
        This function opens a (.wav) format file specified by it's absolute 
        path and returns a memory-mapped file object.

        Parameters
        --------------------------
            filename : string
                Absolute path to (.wav) format file to be read.

        Returns
        --------------------------
            signal : file object
                Memory mapped file object of specified (.wav) file.
    """

    try:

        rate, signal = scipy.io.wavfile.read(filename, mmap=True)
        signal = signal[44:, :]
        return signal

    except:

        return None
