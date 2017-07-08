"""
    **Author :** *Jay Krishna*

    This module read (.txt) file from physical storage as a memory-
    mapped file.

"""

import numpy as np


def loaddata(filename):
    """
        This function opens a (.txt) format file specified by it's absolute 
        path and returns a memory-mapped file object.

        Parameters
        --------------------------
            filename : string
                Absolute path to (.txt) format file to be read.

        Returns
        --------------------------
            signal : file object
                Memory mapped file object of specified (.txt) file.
    """

    try:

        signal = np.memmap(filename, dtype='complex128', mode='r')
        return signal

    except:

        return None