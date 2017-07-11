import numpy as np
from scipy.fftpack import fft, fftshift


def CalcFourier(signal, fs, fc, nfft=0):

    step = 1 / fs
    pole = fs
    if nfft == 0:
        nfft = len(signal)
    # One way I want to implement this
    transform = 20 * \
        np.log10(np.absolute(fftshift(fft(signal, n=nfft)) / len(signal)))

    # Other way I implemented keeping the log thing away
    #transform = (np.absolute(fftshift(fft(signal,n=nfft))))

    #N = transform.shape[0]

    frequency = np.arange((-1 * pole) / 2 + fc, pole / 2 + fc, fs / nfft)

    return frequency, transform
