from src.EIS_Reader import EISPlotter, EISReader
import os
import matplotlib.pyplot as plt
import numpy as np

eis_directory = '../Data/EIS_Optical/EIS'
photonics_directory = '../Data/EIS_Optical/Photonics'

photonics_files = os.listdir(photonics_directory)

print(photonics_files)

wavelength = np.linspace(498.6174,1103.161,3648)

photonics_fig, photonics_plot = plt.subplots()

w,background = np.genfromtxt(os.path.join(photonics_directory,photonics_files[-1]), unpack=True, delimiter=',')

for file in photonics_files[1:-1]:
    w, reflectance = np.genfromtxt(os.path.join(photonics_directory,file), unpack=True, delimiter=',')
    normalised_reflectance = np.divide(reflectance,background)
    photonics_plot.plot(wavelength, normalised_reflectance)
photonics_plot.set_xlim([850,950])
photonics_plot.set_ylim([0,0.6])
photonics_plot.legend(['100 mM', '10 mM', '1mM','100 $\mu $M', '10 $\mu $M'])
photonics_plot.set_xlabel('Wavelength (nm)')
photonics_plot.set_ylabel('Reflectance')

eis_files = os.listdir(eis_directory)

fig,eis_mag = plt.subplots()
eis_phase = eis_mag.twinx()
for file in eis_files[1:]:
    print(file)
    eis_reader = EISReader(os.path.join(eis_directory,file), set_cycle=2)
    eis_mag.loglog(eis_reader.eis.frequency, eis_reader.eis.magnitude)
    eis_phase.semilogx(eis_reader.eis.frequency, eis_reader.eis.phase, '--')

eis_mag.set_xlabel('Frequency (Hz)')
eis_mag.set_ylabel('|Z| ($\Omega $)')
eis_mag.legend(['100 mM', '10 mM', '1mM','100 $\mu $M', '10 $\mu $M'],loc='center right')
eis_phase.set_ylabel('$\\angle$ ($\degree $)')
plt.show()



#eis_plotter = EISPlotter(eis_directory)