import os
from src.hyperspectral_imaging import natural_key, get_hyperspectral_image, plot_spectra
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from src.SPV_Reader import  SPV_Reader
from src.EIS_Reader import EISReader
from src.EC_Lab_CVReader import CVReader

data_directory = '../Data/Thiol_Diazonium'
photonics_directory = os.path.join(data_directory,'Photonics')

photonics_sub_directories = os.listdir(photonics_directory)
sorted_photonics_sub_directories = sorted(photonics_sub_directories,key=natural_key)
photonics_results_directory = '../Results/Diaz_Nile_Blue_Repeat/Photonics'
print(sorted_photonics_sub_directories)
hyperspectral_wavelengths = np.arange(830,890.5,0.5)
images = list()
mean = list()
std = list()

elec_main_directory = os.path.join(data_directory,'Elec')
cv_directory = os.path.join(elec_main_directory,'CV')
eis_directory = os.path.join(elec_main_directory,'EIS')
swv_directory = os.path.join(elec_main_directory, 'SWV')

fig, image_plot = plt.subplots()
fig2, mean_plot = plt.subplots()
fig3, thiol_plot = plt.subplots()
fig7, thiol_mag_plot = plt.subplots()
thiol_phase_plot = thiol_mag_plot.twinx()
fig4, cv_plot = plt.subplots()
fig5, mag_plot = plt.subplots()
phase_plot = mag_plot.twinx()
fig6, swv_plot = plt.subplots()
cv_legend = list()
swv_legend = list()


for file in os.listdir(cv_directory)[:9]:
    if '.mpt' in file:
        print(file)
        cv_reader = CVReader(os.path.join(cv_directory,file), set_cycle=1)
        split_current = np.array_split(cv_reader.current, len(cv_reader.voltage) / 10)
        split_voltage = np.array_split(cv_reader.voltage, len(cv_reader.voltage) / 10)
        mean_current = [np.mean(current) for current in split_current]
        voltage = [voltage[0] for voltage in split_voltage]
        cv_legend.append(file)
        cv_plot.plot(voltage, mean_current,'o', markersize=2)
for file in os.listdir(cv_directory)[14:]:
    if '.mpt' in file:
        print(file)
        cv_reader = CVReader(os.path.join(cv_directory,file), set_cycle=1)
        split_current = np.array_split(cv_reader.current, len(cv_reader.voltage) / 10)
        split_voltage = np.array_split(cv_reader.voltage, len(cv_reader.voltage) / 10)
        mean_current = [np.mean(current) for current in split_current]
        voltage = [voltage[0] for voltage in split_voltage]
        cv_legend.append(file)
        thiol_plot.plot(voltage, mean_current,'o', markersize=2)
for file in os.listdir(eis_directory)[:9]:
    if '.mpt' in file:
        eis_reader = EISReader(os.path.join(eis_directory,file),set_cycle=2)
        mag_plot.loglog(eis_reader.eis.frequency, eis_reader.eis.magnitude)
        phase_plot.semilogx(eis_reader.eis.frequency, eis_reader.eis.phase, '--')
for file in os.listdir(eis_directory)[14:]:
    if '.mpt' in file:
        eis_reader = EISReader(os.path.join(eis_directory,file),set_cycle=2)
        thiol_mag_plot.loglog(eis_reader.eis.frequency, eis_reader.eis.magnitude)
        thiol_phase_plot.semilogx(eis_reader.eis.frequency, eis_reader.eis.phase, '--')

for file in os.listdir(swv_directory)[:9]:
    if '.mpt' in file:
        swv_legend.append(file)
        swv_reader = SPV_Reader(os.path.join(swv_directory,file))
        swv_plot.plot(swv_reader.voltage, swv_reader.normalised_current)
cv_legend = ['KPI','KPI Post NB 1', 'KPI Post NB 2', '5 $\mu$M Nile Blue ']
thiol_legend = ['1','2','3']
swv_plot.set_xlabel('V vs Ag/AgCl (V)')
swv_plot.set_ylabel('$\Delta$A ($\mu$A)')
cv_plot.set_xlabel('V vs Ag/AgCl (V)')
cv_plot.set_ylabel('Current (mA)')
thiol_plot.set_xlabel('V vs Ag/AgCl (V)')
thiol_plot.set_ylabel('Current (mA)')
thiol_plot.legend(thiol_legend)
mean_plot.set_ylabel('Peak $\lambda$ (nm)')
mean_plot.set_xlabel('Scan')
mag_plot.legend(cv_legend, loc='center right')
mag_plot.set_xlabel('Frequency (Hz)')
mag_plot.set_ylabel('|Z| ($\Omega$)')
phase_plot.set_ylabel('$\\angle$ Z ($\degree$)')
thiol_mag_plot.legend(thiol_legend, loc='center right')
thiol_mag_plot.set_xlabel('Frequency (Hz)')
thiol_mag_plot.set_ylabel('|Z| ($\Omega$)')
thiol_phase_plot.set_ylabel('$\\angle$ Z ($\degree$)')
swv_plot.legend(cv_legend)
cv_plot.legend(cv_legend)
cv_plot.set_ylim([-0.01, 0.01])


results_files = os.listdir(os.path.join(photonics_results_directory,'image'))
sorted_results_files = sorted(results_files, key=natural_key)
spectra_wavelengths = np.linspace(498.6174, 1103.161, 3648)
vertical_slice = slice(100,600)
horizontal_slice = slice(600,800)
max_wavelengths = list()

try:
    results_files_path = os.path.join(photonics_results_directory, 'spectra')
    spectra_results_file = os.listdir(results_files_path)[0]
    print(spectra_results_file)
    max_wavelengths = np.load(os.path.join(results_files_path,spectra_results_file))
except IndexError:
    for directory in sorted_photonics_sub_directories:

        spectra_directory = os.path.join(directory,'spectra')
        results_files = os.path.join(photonics_results_directory, 'spectra')
        data_path = os.path.join(photonics_directory,spectra_directory)
        max_wavelength = plot_spectra(data_path,spectra_wavelengths, spectra_plot)
        max_wavelengths.append(max_wavelength)
    np.save(os.path.join(results_files, 'spectra_results'), max_wavelengths)

for directory in sorted_results_files:
    image_results_path = os.path.join(photonics_results_directory,'image')
    results_file = os.path.join(image_results_path,directory)
    image_directory = os.path.join(directory,'image')
    data_path = os.path.join(photonics_directory,image_directory)
    image = get_hyperspectral_image(results_file,data_path,hyperspectral_wavelengths)
    images.append(
        [image_plot.imshow(image[vertical_slice, horizontal_slice], interpolation='nearest', cmap='hot', animated=True)])
    mean.append(np.mean(image[vertical_slice, horizontal_slice]))
    std.append(np.std(image[vertical_slice, horizontal_slice]))

print(len(mean))
print(len(std))
range = np.arange(0,len(mean),1)
print(len(range))
mean_plot.errorbar(range,mean,std, fmt='o')
#mean_plot.set_ylim([865,872])


ani = animation.ArtistAnimation(fig2, images, interval=1000, blit=True,
                                 repeat_delay=0)

plt.show()