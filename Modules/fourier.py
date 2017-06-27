import numpy as np
from scipy.fftpack import fft, fftshift


def CalcFourier(signal, fs, fc):

    step = 1 / fs
    pole = fs

    transform = 20 * np.log10(np.absolute(fftshift(fft(signal))/len(signal)))
    N = transform.shape[0]
    frequency = np.arange((-1 * pole) / 2 + fc, pole / 2 + fc, fs / N)
    return frequency, transform
