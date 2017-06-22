import numpy as np
import matplotlib.pyplot as plt
import fourier
import bandpass_butter
import bandpass_firwin
import spectrogram
import read_dat
import read_wav
import selectfile
import bandpass_butter

if __name__ == "__main__":

    filename, file_extension = selectfile.select()

    if file_extension != ".wav" and file_extension != ".dat":
        print("Invalid Input !!!")
        quit()

    else:

        fs = 2 * 1e6
        fc = 137.65 * 1e6
        chunksize = 2000000
        last = 1

        if(file_extension == ".dat"):
            signal = read_dat.loaddata(filename)
            factor = 2
        else:
            signal = read_wav.loaddata(filename)
            factor = 1

        for i in range(0, last):

            start = i * factor * chunksize
            end = start + factor * chunksize

            if(file_extension == ".wav"):
                signal_chunk = signal[start:end, :]
                signal_chunk = signal_chunk.flatten()

            else:
                signal_chunk = signal[start:end]

            signal_chunk = signal_chunk - 127.5

            signal_chunk_iq = np.empty(
                signal_chunk.shape[0] // 2, dtype=np.complex128)
            signal_chunk_iq.real = signal_chunk[::2]
            signal_chunk_iq.imag = signal_chunk[1::2]

            plt.rcParams["figure.figsize"] = (16, 6)
            fig = plt.figure()

            frequency, transform = fourier.CalcFourier(signal_chunk_iq, fs, fc)
            ax = fig.add_subplot(111)
            plt.gca().xaxis.grid(True)
            plt.gca().yaxis.grid(True)
            ax.set_xlabel('Frequency(MHz)')
            ax.set_ylabel('|X(f)|')
            plt.plot(frequency, transform)
            plt.show()
