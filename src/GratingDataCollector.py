from openpyxl import load_workbook
from openpyxl import Workbook
import os
import csv
import matplotlib.pyplot as plt


import numpy as np
from scipy import optimize as sci
from scipy import stats as stat


import re

class WhiteLight_Data_Reader():

    def natural_key(self,string_):
        return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


    def single_file(self,directory,output_filename):

        output_directory = '../Results/'
        collected = Workbook()
        results_file = os.path.join(output_directory, output_filename + '.npy')

        if not os.path.exists(output_directory):
            os.mkdir(output_directory)

        files = [f for f in os.listdir(directory) if '.csv' in f]
        files = sorted(files, key=self.natural_key)

        refletance_array = list()
        for file in files:
            print(file)
            reflectance = np.genfromtxt(os.path.join(directory,file),delimiter=',')
            refletance_array.append(reflectance)
        np.save(results_file, np.asarray(refletance_array))


        # output_filename = os.path.join(output_directory,'Sorted.csv')
        # print(files)
        # with open(output_filename,'w') as output_file:
        #     writer = csv.writer(output_file)
        #     for file in files:
        #         with open(os.path.join(directory, file)) as input_file:
        #             reader = csv.reader(input_file,delimiter=',')
        #             for row in reader:
        #                 time = file.split('.')[0]
        #                 row.insert(0, time)
        #                 writer.writerow(row)

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def grating_fit(wavelength, scaling_factor,fano_parameter,resonance_linewidth,resonance_wavelength,vertical_shift):
    numerator = np.square(fano_parameter*resonance_linewidth+ wavelength- resonance_wavelength)
    demonimator = np.square(resonance_linewidth) + np.square(wavelength-resonance_wavelength)
    quotient = numerator/demonimator
    result = scaling_factor * quotient + vertical_shift
    return result


if __name__ == '__main__':
    sorted_file = '/Users/st659/Documents/SiN Grating Local/MannoseConA_270317/Output/Sorted.csv'


    fit_initial = [float(6), 10, 4, 852, 0.63235924622541]
    spectrum = np.linspace(498.6174,1103.161,3648)

    fig = plt.figure()
    ax3 = fig.add_subplot(111)
    with open(sorted_file, 'r') as input_file:
        reader = csv.reader(input_file, delimiter=',')

        wavelength = list()
        time = list()
        time_peak = list()
        peaks = list()
        for row in reader:
            data = row[1:]

            peak = detect_peaks.detect_peaks(data, mph=5.7, mpd = 1000)
            if peak and peak >2000:
                peaks.append(peak[0])
                time_peak.append(row[0])
            peak_data = data[2110:2300]
            x = spectrum[2110:2300]

            peak_data = [float(data) for data in peak_data]

            try:
                a = sci.curve_fit(grating_fit,x, peak_data, p0 =fit_initial)
                ax3.plot(peak_data)
                print(row[0])
                time.append(row[0])
                wavelength.append(a[0][3])
            except RuntimeError:
                print("Fit Failed")


            #if int(row[0]) > 100 and int(row[0])< 104 :
                #ax3.plot(peak_data)
            #if int(row[0]) > 2100 and int(row[0])< 2110:
                #ax3.plot(peak_data)

            #if int(row[0]) > 2200:
                #break

    plt.style.use(['seaborn-white', 'seaborn-notebook'])
    wavelength_mean = list()
    wavelength_std = list()
    time_mean = list()
    for values, times in zip(chunker(wavelength, 50), chunker(time, 50)):
        wavelength_mean.append(np.mean(values, axis=0))
        wavelength_std.append(stat.sem(values, axis=0))
        time_mean.append(float(times[0])/60)

    figure = plt.figure()
    ax = figure.add_subplot(111)

    ax.set_xlabel('Time (min)')
    ax.set_ylabel('Peak Wavelength (nm)')

    print(len(time_mean))
    print(wavelength_mean)
    print(wavelength_std)
    ax.set_ylim(851.0,852.4)
    ax.errorbar(time_mean, wavelength_mean, wavelength_std, fmt='o')
    ax.errorbar((4410.0/60, 4410.0/60), (851.0, 852.4),(0,0), fmt='--', color='k')
    ax.text(4490.0/60, 851.63, 'AMP +')
    ax.text(4490.0/60, 851.57, 'Sulfo SMCC')
    ax.errorbar((7800.0/60, 7800.0/60), (851.0, 852.4),(0,0), fmt='--', color='k')
    ax.text(7890.0/60, 851.8, 'ConA')
    ax.errorbar((11000.0/60, 11000.0/60), (851.0, 852.4),(0,0), fmt='--', color='k')
    ax.text(11090.0/60, 851.8, 'D-Mannose')

    plt.show()