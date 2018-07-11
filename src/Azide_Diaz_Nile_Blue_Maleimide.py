import os
from src.hyperspectral_imaging import natural_key, get_hyperspectral_image, plot_spectra
from src.GratingDataCollector import grating_fit
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import fnmatch
import scipy as sci
from src.SPV_Reader import  SPV_Reader
from src.EIS_Reader import EISReader
from src.EC_Lab_CVReader import CVReader

data_directory = '../Data/Azide_Diaz_Nile_Blue_Maleimide'
results_directory = '../Results/Azide_Diaz_Maleimide'
elec_directory = os.path.join(data_directory,'Elec')
photonics_directory = os.path.join(data_directory,'Photonics')
fit_slice_vertical = slice(300, 310)
photonics_directories = os.listdir(photonics_directory)
sorted_photonics_directories = sorted(photonics_directories,key=natural_key)
print(sorted_photonics_directories)
mean_resonance_fit = list()
std_resonance_fit = list()

fig, pixel_plot = plt.subplots()
fig2, mean_plot = plt.subplots()

pixel_intensity = list()
for directory in sorted_photonics_directories[:5]:
    directory_path = os.path.join(photonics_directory,directory)
    image_directory_path = os.path.join(directory_path,'image')
    image_filenames = os.listdir(image_directory_path)
    sorted_image_filenames = sorted(image_filenames,key=natural_key)
    for file in sorted_image_filenames:
        try:
            base=os.path.splitext(file)[0]
            numpy_filename = base + '.npy'
            image = np.load(os.path.join(image_directory_path,numpy_filename))
            if '.npy' in file:
                pixel_intensity.append(image[fit_slice_vertical,fit_slice_vertical])
            print(numpy_filename + ' File Read')

        except FileNotFoundError:
            print(file + ' Numpy File Not Found, Generating Numpy File')
            image = np.genfromtxt(os.path.join(image_directory_path,file),delimiter=',')
            np.save(os.path.join(image_directory_path,base),image)
            print(file + ' Numpy file saved')
    pixel_array = np.asarray(pixel_intensity)
    columns = pixel_array.shape[1]
    rows = pixel_array.shape[2]
    fitted_resonance = list()
    wavelengths = np.arange(800,870.5,0.5)

    for col in np.arange(0, columns, 1):
        for row in np.arange(0, rows, 1):

            pixel_values = pixel_array[:, col, row]
            peak_reflectance_arg = np.argmax(pixel_values)
            try:
                popt, pcov = sci.optimize.curve_fit(grating_fit,
                                                    wavelengths,
                                                    pixel_values,
                                                    maxfev=15000,
                                                    p0=[1, 1, 1, wavelengths[peak_reflectance_arg], 1])
                pixel_plot.plot(wavelengths, grating_fit(wavelengths, *popt), 'o')
                resonance_wavelength = popt[-2]
                fitted_resonance.append(resonance_wavelength)
            except RuntimeError:
                print('Fit Failed')

    mean_resonance_fit.append(np.mean(resonance_wavelength))
    std_resonance_fit.append(np.std(resonance_wavelength))

samples = np.arange(0,len(mean_resonance_fit),1)
mean_plot.errorbar(samples, mean_resonance_fit, std_resonance_fit)

plt.show()