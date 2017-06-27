from PyQt4 import QtGui

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftshift
import sys

from Modules import SignalData

from Screens import waitscreen

def waterfallspect(data, fc, fs, fft_size, overlap_fac):

    hop_size = np.int32(np.floor(fft_size * (1 - overlap_fac)))
    pad_end_size = fft_size

    total_segments = np.int32(np.ceil(len(data) / np.float32(hop_size)))
    t_max = len(data) / np.float32(fs)

    window = np.hanning(fft_size)
    inner_pad = np.zeros(fft_size)

    proc = np.concatenate((data, np.zeros(pad_end_size)))
    result = np.empty((total_segments, fft_size),
                      dtype=np.float32)

    for i in range(total_segments):
        current_hop = hop_size * i
        segment = proc[current_hop:current_hop +
                       fft_size]
        windowed = segment * window
        padded = np.append(windowed, inner_pad)
        spectrum = fftshift(fft(windowed)) / fft_size
        result[i, :] = np.absolute(spectrum[:])

    result = (20 * np.log10(result))

    return result

def SpectrogramPlot(SignalInfo,cmapstr,WaitWindow):

	value=SignalInfo.getvalues()
	signal=value[2]
	nfft=32768

	if("gray" in cmapstr):
		cmap=plt.cm.gray
	elif("magma" in cmapstr):
		cmap=plt.cm.magma
	elif("inferno" in cmapstr):
		cmap=plt.cm.inferno
	elif("viridis" in cmapstr):
		cmap=plt.cm.viridis
	else:
		cmap=plt.cm.plasma

	if(value[1]==".wav"):
		factor=1
	else:
		factor=2

	fs=value[3]
	fc=value[4]
	chunksize=int(fs)
	len_signal=len(signal)
	chunknumber=int(len_signal//(factor*chunksize))

	#WaitWindow=WaitScreenReq()
	WaitWindow.show()
	#WaitWindow.updateprogress(i,chunknumber)

	for i in range(0, chunknumber):

		WaitWindow.updateprogress(i,chunknumber)
		
		start = i * factor*chunksize
		end = start + factor*chunksize

		if(value[1]==".wav"):
			signal_chunk = signal[start:end, :]
			signal_chunk = signal_chunk.flatten()
		else:
			signal_chunk = signal[start:end]

		signal_chunk = signal_chunk - 127.5

		signal_chunk_iq = np.empty(signal_chunk.shape[0] // 2, dtype=np.complex128)
		signal_chunk_iq.real = signal_chunk[::2]
		signal_chunk_iq.imag = signal_chunk[1::2]

		if(i == 0):
			waterfall_data = waterfallspect(signal_chunk_iq, fc, fs, nfft, 0.5)
		else:
			waterfall_data = waterfall_data + waterfallspect(signal_chunk_iq, fc, fs, nfft, 0.5)

		del signal_chunk_iq, signal_chunk


	WaitWindow.close()
	dummy_vector = [0.0, 10]
	freq_vector = [-(fs / 2) + fc, (fs / 2) + fc]
	waterfall_data = waterfall_data / chunknumber

	img = plt.imshow(waterfall_data, extent=freq_vector + dummy_vector,origin='lower', interpolation='nearest', aspect='auto', cmap=cmap)
	plt.colorbar()
	plt.yticks([])
	plt.show()