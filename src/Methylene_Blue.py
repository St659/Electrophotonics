import os
from src.hyperspectral_imaging import fit_fano_shape,natural_key
import matplotlib.pyplot as plt
import numpy as np
plt.style.use(['seaborn-white','seaborn-poster'])
back_directory = '../Data/meth_blue'
photonics_data_directory = '../Data/meth_blue/Photonics'
photonics_results_directory = '../Results/meth_blue/Photonics'
elec_data_diretory = '../Data/meth_blue/Electrical'


fig, (concentration_plot,reflectance_plot) = plt.subplots(1,2)
photonics_sub_dirs = os.listdir(photonics_data_directory)
print(photonics_sub_dirs)
background = np.genfromtxt(os.path.join(back_directory,'ref_methblue_edit.csv'))

wave = np.linspace(498.6174, 1103.161, 3648)
mean_resonance = list()
std_resonance = list()

for file in os.listdir(photonics_results_directory):
    if '7' in file:
        print(file)
        resonance_wavelengths = np.load(os.path.join(photonics_results_directory, file))
        split_wavelengths = np.array_split(resonance_wavelengths, len(resonance_wavelengths) / 30, axis=0)
        mean_split_wavelengths = [np.mean(resonance) for resonance in split_wavelengths]
        std_split_wavelengths = [np.std(resonance) for resonance in split_wavelengths]
        time = np.arange(0, len(mean_split_wavelengths), 1)
        mean_resonance.append(np.mean(resonance_wavelengths, axis=0))
        std_resonance.append(np.std(resonance_wavelengths, axis =0))

        reflectance_plot.errorbar(time,mean_split_wavelengths,std_split_wavelengths)
mean_resonance.pop(4)
std_resonance.pop(4)
concentration = np.arange(0, len(mean_resonance), 1)
concentration_plot.errorbar(concentration, mean_resonance,std_resonance,fmt='o')
concentration_plot.set_ylim([867,868])
reflectance_plot.set_ylim([866,869])
plt.show()


# for directory in photonics_sub_dirs:
#     if not os.path.exists(os.path.join(photonics_results_directory,directory)):
#         os.makedirs(os.path.join(photonics_results_directory,directory))
#     photonics_files = os.listdir(os.path.join(photonics_data_directory, directory))
#     sorted_photonics_files = sorted(photonics_files, key=natural_key)
#     data_directory = os.path.join(photonics_data_directory,directory)
#     resonance_wavelengths = np.asarray(
#         [fit_fano_shape(os.path.join(data_directory, file), wave, background, reflectance_plot) for file in
#          sorted_photonics_files])
#     np.save(os.path.join(photonics_results_directory,directory), resonance_wavelengths)
