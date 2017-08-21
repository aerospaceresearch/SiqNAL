"""
    **Author :** *Jay Krishna*

    This module computes the fourier transform, fourier transform power & inverse
    fourier transform of the signal.

"""
import numpy as np
from scipy.fftpack import fft, fftshift, ifft
import matplotlib.pyplot as plt


def CalcFourier(signal):
    """
        This function calculates the fourier transform of a signal. The fourier transform's
        zero frequency is shifted to the centre of the spectrum.

        Parameters
        -------------------------
            signal : ndarray
                Numpy complex array of signal.

        Returns
        -----------------------
            transform : ndarray
                Numpy array of computed fourier transform.

    """

    transform = fftshift(fft(signal))

    return transform


def CalcFourierPower(signal, fs, fc):
    """
        This function calculates the power of fourier transform of a signal in each frequency bin.

        Parameters
        -------------------------
            signal : ndarray
                Numpy complex array of signal.
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

    value = np.absolute(signal)
    transform = 20 * np.log10(value)

    N = transform.shape[0]

    frequency = np.arange((-1 * pole) / 2 + fc, pole / 2 + fc, fs / N)

    return frequency, transform


def CalcIFourier(signal):
    """
        This function calculates the inverse fourier transform of a signal. The fourier transform's
        zero frequency is shifted to the left of the spectrum.

        Parameters
        -------------------------
            signal : ndarray
                Numpy complex array of signal.

        Returns
        -----------------------
            isignal : ndarray
                Numpy array of computed inverse fourier transform.

    """

    isignal = ifft(fftshift(signal))

    return isignal
