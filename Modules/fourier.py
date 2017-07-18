import numpy as np
from scipy.fftpack import fft, fftshift, ifft, ifftshift
import matplotlib.pyplot as plt


def CalcFourier(signal):
    # just the plain fft  shift, so we can use the output for ther filtering as well ;)

    p = fftshift(fft(signal))

    return p


def CalcFourierPower(signalFFT, fs, fc):
    step = 1 / fs
    pole = fs
    # One way I want to implement this
    # transform = 20 * \
    #     np.log10(np.absolute(fftshift(fft(signal)/ len(signal))))

    value = np.absolute(signalFFT)
    #maximum = value.max()
    #transform = 20 * np.log10(value / maximum)
    # @jay, please don't use this on a chunk level!
    # it is normalizing it wrongly only on a part level, but not for the full waterfall.
    # and my limited knowledge says, it is not making it dBm
    transform = 20 * np.log10(value)

    N = transform.shape[0]

    # why generating this all the loops? that won't change.
    frequency = np.arange((-1 * pole) / 2 + fc, pole / 2 + fc, fs / N)

    return frequency, transform


def CalcIFourier(P):

    signal = ifft(ifftshift(P))

    return signal
