import os
import numpy as np
import fnmatch
import matplotlib.pyplot as plt
import re
from src.GratingDataCollector import sci
from src.GratingDataCollector import grating_fit
import scipy as sci


def fit_fano_shape(file_name,wavelength_range ,background_reflectance, reflectance_plot):
    print(file_name)
    grating_reflectance = np.genfromtxt(file_name, unpack=True, delimiter=',')


    normalised_reflectance = np.divide(grating_reflectance, background_reflectance)
    #normalised_reflectance = grating_reflectance
    min_wavelength = np.argmax(wavelength_range > 820)
    max_wavelength = np.argmin(wavelength_range < 900)

    wavelengths_fit = wavelength_range[min_wavelength:max_wavelength]

    #reflectance_fit = subtract_linear_background(wavelengths_fit, normalised_reflectance[min_wavelength:max_wavelength])
    reflectance_fit = normalised_reflectance[min_wavelength:max_wavelength]
    reflectance_plot.plot(wavelengths_fit, reflectance_fit)
    # reflectance_plot.set_ylim([0, 1])
    # reflectance_plot.set_xlim([750, 900])

    peak_reflectance_arg = np.argmax(reflectance_fit)
    data_point_range = 200
    min_peak_reflectance = peak_reflectance_arg - int(data_point_range / 2)
    max_peak_reflectance = peak_reflectance_arg + int(data_point_range / 2)
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


def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

def get_hyperspectral_image(results_filename, data_directory, wavelengths):
    file_name = results_filename
    print(file_name)

    working_directory = os.getcwd()
    #results_filename = os.path.join('../Results', result_file)


    try:
        resonance = np.load(results_filename)

    except OSError:
        data_directory_path = os.path.join(working_directory, data_directory)

        data_list = list()
        for file in os.listdir(data_directory):
            # if fnmatch.fnmatch(file, '*.csv'):
            #     print(os.path.join(data_directory, file))
            #     file = np.genfromtxt(os.path.join(data_directory, file), delimiter=',')
            if fnmatch.fnmatch(file, '*.npy'):
                file = np.load(os.path.join(data_directory,file))
                data_list.append(file)

        data = np.asarray(data_list)

        max_values = np.argmax(data, axis=0)
        print(max_values)
        resonance = wavelengths[max_values]
        #file_name = results_filename.strip('.')[0]
        print(file_name)
        np.save(results_filename,resonance)

    return resonance


def plot_spectra(data_directory, wavelength, ax):

    data = list()
    for file in os.listdir(data_directory):
        if fnmatch.fnmatch(file, '*.csv'):
            data.append(np.genfromtxt(os.path.join(data_directory, file), delimiter=','))
    max_reflectance = np.max(np.asarray(data), axis = 0)
    try:
        popt, pcov = sci.optimize.curve_fit(grating_fit,
                                            wavelength,
                                            max_reflectance,
                                            maxfev=15000,
                                            p0=[1, 1, 1, wavelength[np.argmax(max_reflectance)], 1])
        print(popt)
        resonance_wavelength = popt[-2]
    except RuntimeError:
        print('Fit Failed')
    except TypeError:
        print('Type Error Failure')
    ax.plot(wavelength,max_reflectance)
    return resonance_wavelength


if __name__ == "__main__":
    fig, ax = plt.subplots()
    fig2, ax3 = plt.subplots()


    water_directory = '../Data/image_3_hyperspectral/image'
    ethanol_directory = '../Data/image_3_ethanol/image'
    post_anneal_directory = '../Data/PostAnneal_notoptimised/image'

    water_hyperspectral = get_hyperspectral_image('image_3_hyperspectral.npy',water_directory)
    ethanol_hyperspectral = get_hyperspectral_image('image_3_ethanol.npy',ethanol_directory)
    post_anneal = get_hyperspectral_image('post_anneal_not_optimised.npy', post_anneal_directory)


    wavelengths = np.arange(830, 940.5, 0.5)
    post_anneal_wavelengths = np.arange(830,920.5,0.5)
    spectra_plot = plot_spectra('../Data/image_3_hyperspectral/spectra', wavelengths, ax3)
    colorbar = ax.imshow(wavelengths[water_hyperspectral],interpolation='nearest', cmap ='hot')
    #ax2.imshow(wavelengths[ethanol_hyperspectral], interpolation='nearest', cmap='hot')
    ax3.imshow(post_anneal_wavelengths[post_anneal],interpolation='nearest', cmap='hot')

    #cbar = fig.colorbar(colorbar)

    plt.show()


