import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fftpack import fft, ifft

from Modules import bandpass
from Modules import importfile
from Modules import read_dat
from Modules import read_wav
from Modules import SignalData
from Modules import freqbands

def find_segs(samples, threshold, min_dur, merge_dur,fs,n):
    start = -1
    end = -1
    segments = []
    points = []

    for idx, x in enumerate(samples):
        if start < 0 and x < threshold:
            pass
        elif start < 0 and x >= threshold:
            start = idx
            end = idx
        elif start >= 0 and x >= threshold:
            end = idx
        elif start >= 0 and x < threshold:
            dur = end - start + 1

            if(dur > min_dur):
                if(len(segments) == 0):
                    segments.append([start, end, dur])
                    points.append([int(start*n), int(end*n)])
                else:
                    start_prev = segments[-1][0]
                    end_prev = segments[-1][1]
                    dur_prev = segments[-1][2]

                    if(start - end_prev <= merge_dur):
                        segments[-1][1] = end
                        segments[-1][2] = end - start_prev + 1
                    else:
                        segments.append([start, end, dur])
                        points.append([int(start*n), int(end*n)])

            start = -1
            end = -1

    if(start >= 0):

        dur = end - start + 1

        if(dur > min_dur):
            if(len(segments) == 0):
                segments.append([start, end, dur])
                points.append([int(start * n), int(end * n)])
            else:
                start_prev = segments[-1][0]
                end_prev = segments[-1][1]
                dur_prev = segments[-1][2]

                if(start - end_prev <= merge_dur):
                    segments[-1][1] = end
                    segments[-1][2] = end - start_prev + 1
                else:
                    segments.append([start, end, dur])
                    points.append([int(start * n), int(end * n)])

    return points

def calc_average(signal_filtered, n):

    average = []
    average_all=[]
    for i in range(0, len(signal_filtered), n):
        average.append(np.mean(signal_filtered[i:i + n]))

    # for i in range(len(average)):
    #     for j in range(n):
    #         average_all.append(average[i])

    # return average_all,average

    return average



# def test_cor():

# 	needle = np.loadtxt('needle.txt').view(complex)
# 	needle=needle[:8192]
# 	needle=needle[::-1]
# 	hay=np.loadtxt('hay.txt').view(complex)
# 	print("Start")
# 	needle_mn=np.mean(needle.real)+1j*np.mean(needle.imag)
# 	hay_mn=np.mean(hay.real)+1j*np.mean(hay.imag)
# 	needle_new=(needle- needle_mn)/(np.sqrt(np.sum((needle- needle_mn)**2)))
# 	hay_new=(hay- hay_mn)/(np.sqrt(np.sum((hay- hay_mn)**2)))
# 	print(hay_new.shape)
# 	fs=2e6
# 	chunksize=2*int(fs)

# 	start=0
# 	end=chunksize
# 	points=[]
# 	point_max=0
# 	while start <= hay_new.shape[0]-2*int(fs):
# 		if(end > hay_new.shape[0]):
# 			end=hay_new.shape[0]
# 		print("{} {}".format(start,end))
# 		autocor=signal.fftconvolve(hay_new[start:end],needle_new,mode="full")
# 		autocor_abs=np.absolute(autocor)
# 		average_all,average=calc_average(autocor_abs,3*8192)
# 		point=find_segs(average,0.2,40,5,int(fs),3*8192)
# 		plt.subplot(211)
# 		plt.plot(autocor_abs)
# 		plt.plot(average_all)

# 		if(len(point) > 0):
# 			initial=point[0][0]
# 			final=point[0][1]
# 			point_max=initial+np.argmax(autocor_abs[initial:final])
# 			final_point=start+(point_max)
# 			if(not final_point in points):
# 				points.append(final_point)
# 			print("Points {} {} {}".format(start,point_max,final_point))
# 			plt.axvline(point_max,color='red')

# 		plt.subplot(212)
# 		plt.plot(average)
# 		plt.show()
# 		start=start+int(fs)//2
# 		end=start+chunksize

# 	print("printing points")
# 	print(points)

# def test_cor():

# 	needle = np.loadtxt('needle.txt').view(complex)
# 	needle=needle[:8192]
# 	needle=needle[::-1]
# 	hay=np.loadtxt('hay.txt').view(complex)
# 	print("Start")
# 	# needle_mn=np.mean(needle.real)+1j*np.mean(needle.imag)
# 	# hay_mn=np.mean(hay.real)+1j*np.mean(hay.imag)
# 	# needle_new=(needle- needle_mn)/(np.sqrt(np.sum((needle- needle_mn)**2)))
# 	# hay_new=(hay- hay_mn)/(np.sqrt(np.sum((hay- hay_mn)**2)))
# 	# print(hay_new.shape)
# 	fs=2e6
# 	chunksize=2*int(fs)

# 	start=0
# 	end=chunksize
# 	points=[]
# 	point_max=0
# 	while start <= hay.shape[0]-2*int(fs):
# 		if(end > hay.shape[0]):
# 			end=hay.shape[0]
# 		print("{} {}".format(start,end))
# 		autocor=signal.fftconvolve(hay[start:end],needle,mode="full")
# 		deno=np.sqrt(np.sum((hay[start:end])**2)*np.sum((needle)**2))
# 		autocor_abs=np.absolute(autocor/deno)
# 		average_all,average=calc_average(autocor_abs,3*8192)
# 		point=find_segs(average,0.06,40,5,int(fs),3*8192)
# 		plt.subplot(211)
# 		plt.plot(autocor_abs)
# 		plt.plot(average_all)

# 		if(len(point) > 0):
# 			initial=point[0][0]
# 			final=point[0][1]
# 			point_max=initial+np.argmax(autocor_abs[initial:final])
# 			final_point=start+(point_max)
# 			if(not final_point in points):
# 				points.append(final_point)
# 			print("Points {} {} {}".format(start,point_max,final_point))
# 			plt.axvline(point_max,color='red')

# 		plt.subplot(212)
# 		plt.plot(average)
# 		plt.show()
# 		start=start+int(fs)//2
# 		end=start+chunksize

# 	print("printing points")
# 	print(points)


def test_cor():

	needle = np.loadtxt('needle.txt').view(complex)
	needle=needle[:8192]
	needle=needle[::-1]
	hay=np.loadtxt('hay.txt').view(complex)
	print("Start")
	needle_mn=np.mean(needle.real)+1j*np.mean(needle.imag)
	#hay_mn=np.mean(hay.real)+1j*np.mean(hay.imag)
	needle_new=(needle- needle_mn)/(np.sqrt(np.sum((needle- needle_mn)**2)))
	#hay_new=(hay- hay_mn)/(np.sqrt(np.sum((hay- hay_mn)**2)))
	#print(hay_new.shape)
	fs=2e6
	chunksize=2*int(fs)

	start=0
	end=chunksize
	points=[]
	point_max=0
	while start <= hay.shape[0]-2*int(fs):
		if(end > hay.shape[0]):
			end=hay.shape[0]
		print("{} {}".format(start,end))

		hay2=hay[start:end]
		#print(hay[:5])
		hay_mn=np.mean(hay2.real)+1j*np.mean(hay2.imag)
		hay_new=(hay2- hay_mn)/(np.sqrt(np.sum((hay2- hay_mn)**2)))

		autocor=signal.fftconvolve(hay_new,needle_new,mode="full")
		autocor_abs=np.absolute(autocor)
		average_all,average=calc_average(autocor_abs,3*8192)
		point=find_segs(average,0.4,30,5,int(fs),3*8192)
		plt.subplot(211)
		plt.plot(autocor_abs)
		#print(autocor_abs[:5])
		plt.plot(average_all)

		if(len(point) > 0):
			initial=point[0][0]
			final=point[0][1]
			point_max=initial+np.argmax(autocor_abs[initial:final])
			final_point=start+(point_max)
			if(not final_point in points):
				points.append(final_point)
			print("Points {} {} {}".format(start,point_max,final_point))
			plt.axvline(point_max,color='red')

		plt.subplot(212)
		plt.plot(average)
		plt.show()
		start=start+int(fs)//2
		end=start+chunksize

	print("printing points")
	print(points)

def analysis(SignalInfo):
	is_peaks_all = False
	filename = 'satellite_db (copy).json'
	bands = freqbands.getbands(SignalInfo, filename)

	chunksize = int(1024 * 2 * 2 * 2 * 2 * 2 * 2 * 2)

	is_peaks_all = False
	for band in bands:

		FLow = band[1]
		FHigh = band[2]
		print(band, FLow, FHigh)

		signal_filtered = bandpass.filter_box(
		SignalInfo, FLow, FHigh, chunksize)

		return signal_filtered


def test_cor_double():

	file2="/home/matrix/Desktop/SiqNAL/test/d6cd51d0002395bea758bda96d641518876bb922e8159b23b2704e9e_f145825000_d0_t1496600686.dat"

	SignalInfo2 = importfile.loadfile(file2)

	if SignalInfo2.filetype == ".dat":
		SignalInfo2.filedata = read_dat.loaddata(SignalInfo2.filename)
	else:
		SignalInfo2.filedata = read_wav.loaddata(SignalInfo2.filename)


	hay=analysis(SignalInfo2)
	hay=np.reshape(hay,(hay.shape[0],1))
	print(hay.shape)
	needle = np.loadtxt('needle.txt').view(complex)
	needle=needle[:8192]
	needle=needle[::-1]
	print("Start")
	needle_mn=np.mean(needle.real)+1j*np.mean(needle.imag)
	needle_new=(needle- needle_mn)/(np.sqrt(np.sum((needle- needle_mn)**2)))
	fs=2e6
	chunksize=2*int(fs)

	start=0
	end=chunksize
	points=[]
	point_max=0
	while start <= hay.shape[0]-2*int(fs):
		if(end > hay.shape[0]):
			end=hay.shape[0]
		print("{} {}".format(start,end))

		hay2=hay[start:end]
		#print(hay[:5])
		hay_mn=np.mean(hay2.real)+1j*np.mean(hay2.imag)
		hay_new=(hay2- hay_mn)/(np.sqrt(np.sum((hay2- hay_mn)**2)))

		autocor=signal.fftconvolve(hay_new,needle_new,mode="full")
		autocor_abs=np.absolute(autocor)
		average=calc_average(autocor_abs,3*8192)
		point=find_segs(average,0.4,30,5,int(fs),3*8192)

		if(len(point) > 0):
			initial=point[0][0]
			final=point[0][1]
			point_max=initial+np.argmax(autocor_abs[initial:final])
			final_point=start+(point_max)
			if(not final_point in points):
				points.append(final_point)
			print("Points {} {} {}".format(start,point_max,final_point))

		start=start+int(fs)//2
		end=start+chunksize

	print("printing points")
	print(points)
	np.savetxt("Corr.csv",points)

if __name__=="__main__":
	test_cor_double()
	#test_cor()