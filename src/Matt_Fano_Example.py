import numpy as np
import matplotlib.pyplot as plt
import scipy as sci
import os


def fano_fit(wavelength, scaling_factor,fano_parameter,resonance_linewidth,resonance_wavelength,vertical_shift):
    numerator = np.square(fano_parameter*resonance_linewidth+ wavelength- resonance_wavelength)
    demonimator = np.square(resonance_linewidth) + np.square(wavelength-resonance_wavelength)
    quotient = numerator/demonimator
    result = scaling_factor * quotient + vertical_shift
    return result


fig, reflectance_plot = plt.subplots()
wavelengths = np.linspace(498.6174, 1103.161, 3648)

#Get a list of the reflectance file names
reflectance_files_directory = '../Data/Matt_Data_Example'
reflectances_files = os.listdir(reflectance_files_directory)

#Remove the background reflectance file from the list of data files (This isn't particularly elegant but it is the
# easiest way
reflectances_files.remove('ref.csv')

#Create the file path to the mirror reflectance file
mirror_file_path = os.path.join(reflectance_files_directory,'ref.csv')
background = np.genfromtxt(mirror_file_path,unpack=True)

#Get the first reflectance file
reflectance_file_path = os.path.join(reflectance_files_directory, reflectances_files[1])
#The Thorlabs spectrometer saves both the wavelengths and the reflectance, which are unpacked to separate variables
#The mirror file doesn't have the wavelengths because the labview script for saving spectra continuously is shit and
#can't read the second column in the file containing the reflectance
print(reflectance_file_path)
grating_reflectance = np.genfromtxt(reflectance_file_path, unpack=True, delimiter=',')
print(grating_reflectance)

#normalised_reflectance = np.divide(grating_reflectance,background)


reflectance_plot.plot(wavelengths,grating_reflectance)
reflectance_plot.set_ylim([0,1])
reflectance_plot.set_xlim([600,1000])

plt.show()

popt, pcov = sci.optimize.curve_fit(fano_fit,
                                            wavelengths,
                                            reflectance_fit[min_peak_reflectance:max_peak_reflectance],
                                            maxfev=15000,
                                            p0=[1,1,1,wavelengths_fit[peak_reflectance_arg],1])