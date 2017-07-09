import numpy as np

from Modules import read_dat
from Modules import read_wav
from Modules import selectfile
from Modules import SignalData

def main():

	SignalInfo=selectfile.select()
	print(SignalInfo.getvalues())

	if SignalInfo.filetype == ".dat":
		SignalInfo.filedata=read_dat.loaddata(SignalInfo.filename)
	else:
		SignalInfo.filedata=read_wav.loaddata(SignalInfo.filename)

	signal=SignalInfo.filedata
	chunksize = int(SignalInfo.Fsample)
	len_signal = len(signal)
	chunknumber = int(len_signal // chunksize)

	for i in range(0, chunknumber):

		startslice = i * chunksize
		endslice = startslice + chunksize

		signal_chunk = signal[startslice:endslice]
		signal_chunk_iq = np.empty(signal_chunk.shape[0]//2, dtype=np.complex128)
		signal_chunk_iq.real = signal_chunk[::2]
		signal_chunk_iq.imag = signal_chunk[1::2]

if __name__ == "__main__" :
	main()