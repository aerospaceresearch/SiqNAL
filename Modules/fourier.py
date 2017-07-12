import numpy as np
from scipy.fftpack import fft, fftshift


def CalcFourier(signal, fs, fc):

    step = 1 / fs
    pole = fs
    # One way I want to implement this
    # transform = 20 * \
    #     np.log10(np.absolute(fftshift(fft(signal)/ len(signal))))

    p = fftshift(fft(signal) / len(signal))
    value = np.absolute(p)
    maximum = value.max()
    transform = 20 * np.log10(value / maximum)

    N = transform.shape[0]

    frequency = np.arange((-1 * pole) / 2 + fc, pole / 2 + fc, fs / N)

    return frequency, transform
