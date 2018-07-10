from src.hyperspectral_imaging import get_hyperspectral_image
from src.EIS_Reader import EISPlotter
from src.EC_Lab_CVReader import CV_Plotter
import os
import matplotlib.pyplot as plt
import numpy as np

#55m Sputtered ITO on Xylene Diluted PDMS 5/2/18 annealed for 3 hours in O2
#Hypespectral measurements from 810nm to 940nm
#Electrochemistry performed used 1mM MB in 100mM PB ph 7.2 and 100umM MB 100mM PB pH 7.2

import scipy.stats as sts

white_directory= '../Data/Xylene_Dilution_Imprint_Post_Anneal_ITO/Photonics/White_light'
image_directory = '../Data/Xylene_Dilution_Imprint_Post_Anneal_ITO/Photonics/image'
eis_directory = '../Data/Xylene_Dilution_Imprint_Post_Anneal_ITO/Electrochemistry/EIS'
uM_1_cv_directory = '../Data/Xylene_Dilution_Imprint_Post_Anneal_ITO/Electrochemistry/CV/100uM'
mM_1_cv_directory = '../Data/Xylene_Dilution_Imprint_Post_Anneal_ITO/Electrochemistry/CV/1mM'

white_files = os.listdir(white_directory)
print(white_files)

wavelengths = np.arange(810,940.5,0.5)
print(wavelengths)
image = get_hyperspectral_image('Xylene_Dilution_Imprint_Post_Anneal_ITO.npy',image_directory)



wave = np.linspace(498.6174,1103.161,3648)
raw_background = os.path.join(white_directory, white_files[0])
white_water = os.path.join(white_directory,white_files[-1])
fig, ax = plt.subplots()
fig2, ax2 = plt.subplots()
wavelength,mirror = np.genfromtxt(raw_background,unpack=True, delimiter=',')
wavelength,grating_water = np.genfromtxt(white_water, unpack=True, delimiter=',')

normalised_grating_reflectance = np.divide(grating_water,mirror)
ax.plot(wave,normalised_grating_reflectance)
ax.set_xlim([820,920])
ax.set_ylim([0,1])

colorbar = ax2.imshow(wavelengths[image], cmap='hot', interpolation='nearest')
cbar = fig2.colorbar(colorbar)

half_maximum = (0.597 - 0.265)
print('Half Maximum: ' + str(0.597 -half_maximum/2))
ax.set_ylabel('Reflectance')
ax.set_xlabel('Wavelength (nm)')

qfactor = 874/(879 - 868)
print('QFactor: ' + str(qfactor))
mean_resonance = np.mean(wavelengths[image])
std_resonance = np.std(wavelengths[image])

print('Mean Resonance: ' + str(mean_resonance))
print('Std Resonance: ' + str(std_resonance))

cv_half_max = 0.00366 - 0.0021
print('CV Half max: ' + str(0.00366 - cv_half_max/2))
print('CV FWHM: ' + str(0.105 -0.0163))

# eis_plotter = EISPlotter(eis_directory, legends=['100 $\mu$M PB', '1mM PB'])
# uM_100_cv_plotter = CV_Plotter(uM_1_cv_directory)
# mM_1_cv_plotter = CV_Plotter(mM_1_cv_directory)


plt.show()