"""
    **Author :** *Jay Krishna*

    This module computes the length normalized fourier transform of the signal.

"""
import numpy as np
from scipy.fftpack import fft, fftshift


def CalcFourier(signal, fs, fc):
    """
        This function calculates the fourier transform of a signal. The fourier transform's
        zero frequency is shifted to the centre of the spectrum. Further the fourier transform
        is length normalized.

        Parameters
        -------------------------
            signal : ndarray
                Numpy complex array of shifted signal.
            fs : float
                Sampling frequency of the signal.
            fc : float
                Centre frequency of the signal.

        Returns
        -----------------------
            frequency : ndarray
                Numpy array of values of frequencies present in the signal.
            transform : ndarray
                Numpy array of computed fourier transform.

    """
    step = 1 / fs
    pole = fs

    transform = 20 * np.log10(np.absolute(fftshift(fft(signal)) / len(signal)))
    N = transform.shape[0]
    frequency = np.arange((-1 * pole) / 2 + fc, pole / 2 + fc, fs / N)
    return frequency, transform
