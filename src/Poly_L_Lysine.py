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

fig, image_plot = plt.subplots()
fig2, image_ani = plt.subplots()
fig3, mean_plot = plt.subplots()
fig4, mag_plot = plt.subplots()
phase_plot = mag_plot.twinx()

data_directory = '../Data/Poly_L_Lysine'
results_directory = '../Results/Poly_L_Lysine'
elec_loop_directory = os.path.join(data_directory,'elec_loop')
elec_directory = os.path.join(data_directory,'elec')
photonics_directory = os.path.join(data_directory,'image')
results_image_path = os.path.join(results_directory, 'Photonics')
fit_slice_vertical = slice(500, 530)
fit_slice_horizontal = slice(70,100)
photonics_directories = os.listdir(photonics_directory)
sorted_photonics_directories = sorted(photonics_directories,key=natural_key)
print(sorted_photonics_directories)
images = list()
mean_resonance_fit = list()
std_resonance_fit = list()
mean = list()
std = list()
wavelengths = np.arange(800,870.5,0.5)
vertical_slice = slice(0,300)
horizontal_slice = slice(0,300)

eis_cycles = np.arange(2,20,3)

elec_loop_file = os.listdir(elec_loop_directory)[0]
eis_files = os.listdir(elec_directory)


for eis_cycle in eis_cycles:
    eis_reader = EISReader(os.path.join(elec_loop_directory,elec_loop_file),set_cycle=eis_cycle)
    mag_plot.loglog(eis_reader.eis.frequency, eis_reader.eis.magnitude, 'b')
    phase_plot.semilogx(eis_reader.eis.frequency, eis_reader.eis.phase, 'b--')

set_cycle = 2
for file in eis_files[:27]:
    try:
        eis_reader = EISReader(os.path.join(elec_directory, file), set_cycle=set_cycle)
        print(file)
        mag_plot.loglog(eis_reader.eis.frequency, eis_reader.eis.magnitude, 'r')

        phase_plot.semilogx(eis_reader.eis.frequency, eis_reader.eis.phase, 'r--')
        set_cycle = set_cycle + 3
    except ValueError:
        pass

for file in eis_files[27:]:
    try:
        eis_reader = EISReader(os.path.join(elec_directory, file), set_cycle=set_cycle)
        print(file)
        mag_plot.loglog(eis_reader.eis.frequency, eis_reader.eis.magnitude, 'g')

        phase_plot.semilogx(eis_reader.eis.frequency, eis_reader.eis.phase, 'g--')
        set_cycle = set_cycle + 3
    except ValueError:
        pass


plt.show()

for directory in sorted_photonics_directories:

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
    image = get_hyperspectral_image(os.path.join(results_image_path, directory), directory_path, wavelengths)
    mean.append(np.mean(image[vertical_slice, horizontal_slice]))
    std.append(np.std(image[vertical_slice, horizontal_slice]))
    print(image)
    images.append([image_plot.imshow(image, interpolation='nearest', cmap='hot', animated=True)])
ani = animation.ArtistAnimation(fig2, images, interval=250, blit=True,
                                 repeat_delay=0)

num_files = np.arange(0,len(mean),1)
mean_plot.errorbar(num_files, mean, std)
plt.show()