import numpy as np

from Modules import read_dat
from Modules import read_wav
from Modules import selectfile
from Modules import SignalData

def main():

	filename,file_extension=selectfile.select()

	if file_extension == ".dat":
		signal=read_dat.loaddata(filename)
	else:
		signal=read_wav.loaddata(filename)

	fs = float(input("Enter Fsampling in MHz :"))
	fc = float(input("Enter FCentre in MHz :"))

	SignalInfo = SignalData.Signal(filename=filename, filetype=file_extension,
                                      filedata=signal, Fsample=fs * 1e6, Fcentre=fc * 1e6)

	chunksize = int(fs*1e6)
	len_signal = len(signal)
	chunknumber = int(len_signal // chunksize)
	print(chunknumber)
	for i in range(0, chunknumber):
		print(i)
		startslice = i * chunksize
		endslice = startslice + chunksize

		signal_chunk = signal[startslice:endslice]
		signal_chunk_iq = np.empty(signal_chunk.shape[0]//2, dtype=np.complex128)
		signal_chunk_iq.real = signal_chunk[::2]
		signal_chunk_iq.imag = signal_chunk[1::2]

if __name__ == "__main__" :
	main()