from src.GratingDataCollector import WhiteLight_Data_Reader
from src.EC_Lab_CVReader import CVReader
import matplotlib.pyplot as plt
import os
import numpy as np
from src.GratingDataCollector import grating_fit
import scipy as sci
import scipy.stats as stats
import re


def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


def single_file(data_directory,results_directory, results_filename):


    files = [f for f in os.listdir(data_directory) if '.csv' in f]
    files = sorted(files, key=natural_key)

    output_filename = os.path.join(results_directory,results_filename)
    for file in files:
        reflectance.append()


def linear_fit(m,x,c):
    return m*x + c
def subtract_linear_background(wavelength, reflectance):
    slope, intercept, r, p, s = stats.linregress([wavelength[0], wavelength[-1]], [reflectance[0], reflectance[-1]])
    line_fit = np.apply_along_axis(linear_fit, 0, wavelength, slope, intercept)
    return np.subtract(reflectance, line_fit)

def fit_fano_shape(file_name,wavelength_range ,background_reflectance, reflectance_plot):
    print(file_name)
    grating_reflectance = np.genfromtxt(file_name, unpack=True, delimiter=',')
    print(len(grating_reflectance))

    normalised_reflectance = np.divide(grating_reflectance, background_reflectance)
    min_wavelength = np.argmax(wavelength_range > 820)
    max_wavelength = np.argmin(wavelength_range < 900)

    wavelengths_fit = wavelength_range[min_wavelength:max_wavelength]

    reflectance_fit = subtract_linear_background(wavelengths_fit, normalised_reflectance[min_wavelength:max_wavelength])
    #reflectance_fit = normalised_reflectance[min_wavelength:max_wavelength]
    reflectance_plot.plot(wavelengths_fit, reflectance_fit)
    # reflectance_plot.set_ylim([0, 1])
    # reflectance_plot.set_xlim([750, 900])

    peak_reflectance_arg = np.argmax(reflectance_fit)
    print(peak_reflectance_arg)
    data_point_range = 200
    min_peak_reflectance = peak_reflectance_arg - int(data_point_range / 2)
    max_peak_reflectance = peak_reflectance_arg + int(data_point_range / 2)

    print(wavelengths_fit[peak_reflectance_arg])
    resonance_wavelength = 0
    try:
        popt, pcov = sci.optimize.curve_fit(grating_fit,
                                            wavelengths_fit[min_peak_reflectance:max_peak_reflectance],
                                            reflectance_fit[min_peak_reflectance:max_peak_reflectance],
                                            maxfev=15000,
                                            p0=[1, 1, 1, wavelengths_fit[peak_reflectance_arg], 1])
        print(popt)
        resonance_wavelength = popt[-2]
    except RuntimeError:
        print('Fit Failed')
    except TypeError:
        print('Type Error Failure')


    return resonance_wavelength





if __name__ == "__main__":
    results_filename = './Results/Sensitivity_Resonance.npy'

    photonics_directory = '../Data/Salt_Sensitivity/Photonics'
    electro_buffer_directory = '../Data/Salt_Sensitivity/Electrochemistry/Converted/Buffer'
    electro_salt_directory = '../Data/Salt_Sensitivity/Electrochemistry/Converted/Buffer + Salt'

    electro_buffer_files = os.listdir(electro_buffer_directory)
    electro_salt_files = os.listdir(electro_salt_directory)

    file_names = os.listdir(photonics_directory)
    wave = np.linspace(498.6174, 1103.161, 3648)
    background = np.genfromtxt(os.path.join(photonics_directory, 'ref.csv'), unpack=True, delimiter=',')
    file_names.remove('ref.csv')
    file_names.remove('.DS_Store')

    fig, (cv_plot, resonance_plot) = plt.subplots(1, 2)
    sorted_files = sorted(file_names, key=natural_key)

    for file in electro_buffer_files[2:12]:

        cv_reader = CVReader(os.path.join(electro_buffer_directory, file), set_cycle=2)
        if cv_reader.scan_rate == 250:
            print(file)
            split_current = np.array_split(cv_reader.current, len(cv_reader.voltage) / 5)
            split_voltage = np.array_split(cv_reader.voltage, len(cv_reader.voltage) / 5)
            mean_current = [np.mean(current) for current in split_current]
            voltage = [voltage[0] for voltage in split_voltage]
            cv_plot.plot(voltage, mean_current, 'b')

    for file in electro_salt_files[:8]:
        cv_reader = CVReader(os.path.join(electro_salt_directory, file), set_cycle=2)
        if cv_reader.scan_rate == 250:
            print(file)
            split_current = np.array_split(cv_reader.current, len(cv_reader.voltage) / 5)
            split_voltage = np.array_split(cv_reader.voltage, len(cv_reader.voltage) / 5)
            mean_current = [np.mean(current) for current in split_current]
            voltage = [voltage[0] for voltage in split_voltage]
            cv_plot.plot(voltage, mean_current, 'r')


    try:
        resonance_wavelengths = np.load(os.path.join('../Results','Sensitivity.npy'))
        print(len(resonance_wavelengths))
    except FileNotFoundError:
        resonance_wavelengths = np.asarray([fit_fano_shape(file,wave,background,reflectance_plot) for file in sorted_files[2100:4000]])
        np.save(os.path.join('../Results','Sensitivity.npy'), resonance_wavelengths)
    resonance_wavelengths = resonance_wavelengths[resonance_wavelengths < 865]
    resonance_wavelengths = resonance_wavelengths[100:]
    print(len(resonance_wavelengths))
    split_wavelengths = np.array_split(resonance_wavelengths, len(resonance_wavelengths)/30, axis = 0)
    print(len(split_wavelengths))
    print(split_wavelengths[0])
    mean_split_wavelengths = [np.mean(resonance) for resonance in split_wavelengths]
    std_split_wavelengths = [np.std(resonance) for resonance in split_wavelengths]
    time = np.arange(0,len(mean_split_wavelengths), 1)


    resonance_plot.errorbar(time,mean_split_wavelengths, std_split_wavelengths)
    resonance_plot.set_ylim([858.5,860.5])
    # for file in sorted_files[0:10]:
    #     reflectance = np.genfromtxt(os.path.join(data_directory, file), delimiter=',')
    #     reflectance_plot.plot(wave,reflectance)
    #     reflectance_plot.set_xlim([700, 950])
    #     reflectance_plot.set_ylim([0,1])

    plt.show()