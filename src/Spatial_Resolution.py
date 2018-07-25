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

data_directory = '../Data/Spatial_Resolution'
results_directory = '../Results/Spatial_Resolution'
elec_directory = os.path.join(data_directory,'Elec')
photonics_directory = os.path.join(data_directory,'image')
results_image_path = os.path.join(results_directory, 'Photonics')
fit_slice_vertical = slice(500, 530)
fit_slice_horizontal = slice(70,100)
photonics_directories = os.listdir(photonics_directory)
sorted_photonics_directories = sorted(photonics_directories,key=natural_key)
print(sorted_photonics_directories)
mean_resonance_fit = list()
std_resonance_fit = list()

wavelengths = np.arange(800,870.5,0.5)

fig, pixel_plot = plt.subplots()
fig2, slice_plot = plt.subplots()
fig3, image_plot = plt.subplots()
images = list()

for directory in sorted_photonics_directories[:1]:

    print(directory)
    pixel_intensity = list()
    directory_path = os.path.join(photonics_directory,directory)
    image_filenames = os.listdir(directory_path)
    sorted_image_filenames = sorted(image_filenames,key=natural_key)
    for file in sorted_image_filenames:
        try:
            base=os.path.splitext(file)[0]
            numpy_filename = base + '.npy'
            image = np.load(os.path.join(directory_path,numpy_filename))
            if '.npy' in file:
                pixel_intensity.append(image[fit_slice_horizontal,fit_slice_vertical])

        except FileNotFoundError:
            print(file + ' Numpy File Not Found, Generating Numpy File')
            image = np.genfromtxt(os.path.join(directory_path,file),delimiter=',')
            np.save(os.path.join(directory_path,base),image)
            print(file + ' Numpy file saved')
    image = get_hyperspectral_image(os.path.join(results_image_path,directory), directory_path, wavelengths)

image_plot.imshow(image,interpolation='nearest', cmap='hot',animated=True)
print(image.shape)
slice_plot.plot(image[428,190:561])
slice_plot.plot(image[57:429,565])
print(image[480])
plt.show()