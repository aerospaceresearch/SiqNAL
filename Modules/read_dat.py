"""
    **Author :** *Jay Krishna*

    This module read (.dat) file from physical storage as a memory-
    mapped file.

"""

import numpy as np


def loaddata(filename):
    """
        This function opens a (.dat) format file specified by it's absolute 
        path and returns a memory-mapped file object.

        Parameters
        --------------------------
            filename : string
                Absolute path to (.dat) format file to be read.

        Returns
        --------------------------
            signal : file object
                Memory mapped file object of specified (.dat) file.
    """

    signal = np.memmap(filename, dtype='uint8', mode='r')
    return signal
