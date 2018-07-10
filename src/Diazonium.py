import os
import numpy as np
from src.hyperspectral_imaging import natural_key,get_hyperspectral_image
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from src.EC_Lab_CVReader import CVReader
from src.EIS_Reader import EISReader
from src.SPV_Reader import SPV_Reader
fig, flat_plot = plt.subplots()
fig2, image_plot = plt.subplots()
fig3, mean_plot = plt.subplots()


data_directory = '../Data/Diazonium'
results_directory = '../Results/Diazonium'
photonics_main_directory = os.path.join(data_directory,'Photonics')
photonics_images_directory = os.path.join(photonics_main_directory,'images')

elec_main_directory = os.path.join(data_directory,'Elec')
cv_directory = os.path.join(elec_main_directory,'CV')
eis_directory = os.path.join(elec_main_directory,'EIS')
swv_directory = os.path.join(elec_main_directory, 'SWV')

fig4, cv_plot = plt.subplots()
fig5, mag_plot = plt.subplots()
phase_plot = mag_plot.twinx()
fig6, swv_plot = plt.subplots()
cv_legend = list()
for file in os.listdir(cv_directory)[:30]:
    if '.mpt' in file:
        print(file)
        cv_reader = CVReader(os.path.join(cv_directory,file), set_cycle=1)
        split_current = np.array_split(cv_reader.current, len(cv_reader.voltage) / 12)
        split_voltage = np.array_split(cv_reader.voltage, len(cv_reader.voltage) / 12)
        mean_current = [np.mean(current) for current in split_current]
        voltage = [voltage[0] for voltage in split_voltage]
        cv_legend.append(file)
        cv_plot.plot(voltage, mean_current,'o')
for file in os.listdir(eis_directory):
    if '.mpt' in file:
        eis_reader = EISReader(os.path.join(eis_directory,file))
        mag_plot.loglog(eis_reader.eis.frequency, eis_reader.eis.magnitude)
        phase_plot.semilogx(eis_reader.eis.frequency, eis_reader.eis.phase, '--')
for file in os.listdir(swv_directory):
    if '.mpt' in file:
        swv_reader = SPV_Reader(os.path.join(swv_directory,file))
        swv_plot.plot(swv_reader.voltage, swv_reader.normalised_current)

cv_plot.legend(cv_legend)

photonics_results_directory = os.path.join(results_directory, 'Photonics')

photonics_subdirectories = os.listdir(photonics_images_directory)
hyperspectral_wavelengths = np.arange(830,890.5,0.5)

sorted_photonics_subdirectories = sorted(photonics_subdirectories, key=natural_key)
photonics_results_files = os.listdir(photonics_results_directory)
sorted_photonics_results_files = sorted(photonics_results_files, key= natural_key)


flat_images = list()
images = list()
mean = list()
std = list()
for file in sorted_photonics_results_files:
    image =get_hyperspectral_image( os.path.join(photonics_results_directory,file), os.path.join(photonics_images_directory,file),hyperspectral_wavelengths)
    flat_images.append(image.flatten())
    v_slice = slice(500,600)
    images.append([image_plot.imshow(image[v_slice,slice(100,300)], interpolation='nearest', cmap='hot', animated=True)])
    mean.append(np.mean(image[v_slice,slice(200,300)]))
    std.append(np.std(image[v_slice,slice(200,300)]))

print(len(mean))
print(len(std))
range = np.arange(0,len(mean),1)
print(len(range))
mean_plot.errorbar(range,mean,std, fmt='o')
mean_plot.set_ylim([865,872])
flat_plot.imshow(flat_images,interpolation='nearest', aspect='auto')
print(sorted_photonics_subdirectories)
ani = animation.ArtistAnimation(fig2, images, interval=100, blit=True,
                                 repeat_delay=0)

plt.show()
