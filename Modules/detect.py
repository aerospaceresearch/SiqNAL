import numpy as np


def find_segs(samples, threshold, min_dur, merge_dur, fs, n, signal_filtered):
    start = -1
    end = -1
    segments = []
    times = []
    points = []

    for idx, x in enumerate(samples):
        if start < 0 and x < threshold:
            pass
        elif start < 0 and x >= threshold and x > 1.2:
            start = idx
            end = idx
        elif start >= 0 and x >= threshold:
            end = idx
        elif start >= 0 and x < threshold:
            dur = end - start + 1

            if(dur > min_dur):
                if(len(segments) == 0):
                    segments.append([start, end, dur])
                    times.append([start * n / fs, end * n / fs])
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
                        times.append([start * n / fs, end * n / fs])
                        points.append([int(start * n), int(end * n)])

            start = -1
            end = -1

    if(start >= 0):

        dur = end - start + 1

        if(dur > min_dur):
            if(len(segments) == 0):
                segments.append([start, end, dur])
                times.append([start * n / fs, end * n / fs])
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
                    times.append([start * n / fs, end * n / fs])
                    points.append([int(start * n), int(end * n)])

    return times, points


def calc_average(signal_filtered, n):

    average = []
    for i in range(0, len(signal_filtered), n):
        average.append(np.mean(signal_filtered[i:i + n]))

    return average


def re_check(signal, point, threshold, m):
    n = m
    point = int(point)
    option = 0
    while(n >= 1):
        average_r = np.mean(signal[point:point + n])
        average_l = np.mean(signal[point - n:point])
        if(average_l >= threshold):
            option = 1
            point = int((point + (point - n)) / 2)
        elif (average_r <= threshold):  # or average_l < threshold):
            option = 2
            point = int((point + (point + n)) / 2)
        elif(average_l < threshold and average_r >= threshold):
            option = 3
            average_temp = np.mean(signal[point:point + (n // 4) + 1])
            if(average_temp <= 0.6 * threshold):
                option = 4
                point = int((point + (point + n // 2)) / 2)
            elif(np.mean(average_temp) < threshold):
                option = 5
                point = int((point + (point + n // 4)) / 2)
        n = n // 2
    return point


def calc_threshold(signal):

    mn = np.mean(signal)
    std = np.std(signal)
    threshold = (mn + (mn + std)) / 2

    return threshold
