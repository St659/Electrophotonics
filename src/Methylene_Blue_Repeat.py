import os
from src.hyperspectral_imaging import fit_fano_shape,natural_key
import matplotlib.pyplot as plt
import numpy as np
from src.EC_Lab_CVReader import CVReader
from src.SPV_Reader import SPV_Reader
from src.EIS_Reader import EISReader
import matplotlib.patches as mpatches
plt.style.use(['seaborn-white','seaborn-notebook'])
back_directory = '../Data/meth_blue_2'
photonics_data_directory = '../Data/meth_blue_2/Photonics'
photonics_results_directory = '../Results/meth_blue_2/Photonics'
elec_data_directory = '../Data/meth_blue_2/Electrical'


fig, concentration_plot = plt.subplots()
#fig2, reflectance_plot = plt.subplots()
fig3, cv_plot = plt.subplots()
fig4, swv_plot = plt.subplots()
fig5, mag_plot = plt.subplots()
phase_plot = mag_plot.twinx()
photonics_sub_dirs = os.listdir(photonics_data_directory)
print(photonics_sub_dirs)
background = np.genfromtxt(os.path.join(back_directory,'methblue_2_ref_edit.csv'))

wave = np.linspace(498.6174, 1103.161, 3648)



# for directory in photonics_sub_dirs:
#     try:
#         npy_directory = directory + '.npy'
#         np.load(os.path.join(photonics_results_directory,npy_directory))
#     except FileNotFoundError:
#
#         photonics_files = os.listdir(os.path.join(photonics_data_directory, directory))
#         sorted_photonics_files = sorted(photonics_files, key=natural_key)
#         data_directory = os.path.join(photonics_data_directory,directory)
#         resonance_wavelengths = np.asarray(
#             [fit_fano_shape(os.path.join(data_directory, file), wave, background, reflectance_plot) for file in
#              sorted_photonics_files])
#         np.save(os.path.join(photonics_results_directory,directory), resonance_wavelengths)

elec_legend = list()
cv_legend = list()
for directory in os.listdir(elec_data_directory):
    try:
        for file in os.listdir(os.path.join(elec_data_directory,directory)):
            if '.mpt' in file:
                split_filename = split_filename = file.split('_')[0]
                if '6' in file:
                    colour = 'xkcd:red'
                elif '7' in split_filename:
                    colour = 'xkcd:green'
                elif '8' in split_filename:
                    colour = 'xkcd:blue'


                if 'CV' in file:
                    cv_reader = CVReader(os.path.join(os.path.join(elec_data_directory,directory),file))
                    if cv_reader.scan_rate == 100:
                        cv_legend.append(file)
                        cv_plot.plot(cv_reader.voltage, cv_reader.current, c = colour)
                elif 'SWV' in file:
                    split_filename = file.split('_')
                    if '6' in split_filename:
                        colour = 'xkcd:red'
                    elif '7' in split_filename:
                        colour = 'xkcd:green'
                    elif '8' in split_filename:
                        colour = 'xkcd:blue'
                    swv_reader = SPV_Reader(os.path.join(os.path.join(elec_data_directory,directory),file))
                    swv_plot.plot(swv_reader.voltage,swv_reader.normalised_current,  c = colour)
                elif 'PEIS' in file:
                    elec_legend.append(file)
                    print(file)
                    eis_reader = EISReader(os.path.join(os.path.join(elec_data_directory,directory),file))
                    print()
                    mag_plot.loglog(eis_reader.eis.frequency, eis_reader.eis.magnitude,)
                    phase_plot.semilogx(eis_reader.eis.frequency, eis_reader.eis.phase, linestyle='--')

        mag_plot.legend(elec_legend)
        swv_plot.legend(elec_legend)
        cv_plot.legend(cv_legend)
        mag_plot.set_xscale('log')
        mag_plot.set_yscale('log')
        phase_plot.set_xscale('log')
        mag_plot.set_xlabel('Frequency (Hz)')
        mag_plot.set_ylabel('|Z| ($\Omega$)')
        phase_plot.set_ylabel('$\\angle$ Z ($\degree$)')

    except NotADirectoryError:
        print('Not a directory')


for directory, colour in zip(os.listdir(photonics_results_directory),['xkcd:red','xkcd:green','xkcd:blue']):
    mean_resonance_pre = list()
    std_resonance_pre = list()

    mean_resonance_post = list()
    std_resonance_post = list()
    for file in os.listdir(os.path.join(photonics_results_directory,directory)):
        print(file)
        resonance_wavelengths = np.load(os.path.join(os.path.join(photonics_results_directory,directory), file))

        split_wavelengths_pre_elec = np.array_split(resonance_wavelengths[:100], len(resonance_wavelengths[:100]) / 10, axis=0)
        split_wavelengths_post_elec = np.array_split(resonance_wavelengths[100:], len(resonance_wavelengths[100:]) / 10, axis=0)
        mean_split_wavelengths_pre_elec = [np.mean(resonance) for resonance in split_wavelengths_pre_elec]
        mean_split_wavelengths_post_elec = [np.mean(resonance) for resonance in split_wavelengths_post_elec]
        std_split_wavelengths_pre_elec = [np.std(resonance) for resonance in split_wavelengths_pre_elec]
        std_split_wavelengths_post_elec = [np.std(resonance) for resonance in split_wavelengths_post_elec]
        time_pre = np.arange(0, len(mean_split_wavelengths_pre_elec), 1)
        time_post = np.arange(0, len(mean_split_wavelengths_post_elec), 1)
        mean_resonance_pre.append(np.mean(resonance_wavelengths[:100], axis=0))
        std_resonance_pre.append(np.std(resonance_wavelengths[:100], axis =0))
        mean_resonance_post.append(np.mean(resonance_wavelengths[100:], axis=0))
        std_resonance_post.append(np.std(resonance_wavelengths[100:], axis=0))
        print(mean_resonance_pre)


        #reflectance_plot.errorbar(time_pre,mean_split_wavelengths_pre_elec,std_split_wavelengths_pre_elec)
        #reflectance_plot.errorbar(time_pre, mean_split_wavelengths_pre_elec, std_split_wavelengths_pre_elec)

    concentration = np.arange(0, len(mean_resonance_pre), 1)
    zero = np.zeros(len(mean_resonance_pre))
    concentration_plot.errorbar(concentration, mean_resonance_pre,std_resonance_pre,fmt='v',color=colour)
    concentration_plot.errorbar(concentration, mean_resonance_post,std_resonance_post,fmt='o',color=colour)

colors = ['xkcd:red', 'xkcd:green','xkcd:blue']
texts = ['PH6', 'PH7', 'PH8']

pre_elec_patches = [plt.plot([],[], marker="^", ms=10, ls="", mec=None, color=colors[i],
            label="{:s}".format(texts[i]) )[0]  for i in range(len(texts)) ]
post_elec_patches = [plt.plot([],[], marker="o", ms=10, ls="", mec=None, color=colors[i],
            label="{:s}".format(texts[i]) )[0]  for i in range(len(texts)) ]

patches = pre_elec_patches + post_elec_patches
concentration_plot.legend(handles=patches)

#concentration_plot.set_ylim([867,868])
#reflectance_plot.set_ylim([866,869])
plt.show()



