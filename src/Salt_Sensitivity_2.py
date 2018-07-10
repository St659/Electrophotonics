import os
import numpy as np
from src.Salt_Sensitivity import fit_fano_shape, natural_key
import matplotlib.pyplot as plt
from src.EC_Lab_CVReader import CVReader

photonics_directory = '../Data/Salt_Sensitivity_DI/Photonics'
electro_directory = '../Data/Salt_Sensitivity_DI/Electrochemistry'

electro_files =[file for file in os.listdir(electro_directory) if '.mpt' in file]
photonics_files = os.listdir(photonics_directory)

wave = np.linspace(498.6174, 1103.161, 3648)
background = np.genfromtxt(os.path.join(photonics_directory, 'ref.csv'), unpack=True, delimiter=',')


try:
    photonics_files.remove('ref.csv')
    photonics_files.remove('.DS_Store')
except ValueError:
    print('File not there to remove')

sorted_photonics_files = sorted(photonics_files, key=natural_key)

fig, reflectance_plot = plt.subplots()
fig2, (resonance_plot, cv_plot) = plt.subplots(1,2)

for file in electro_files[:7]:

    if '.mpt' in file:
        print(file)
        cv_reader = CVReader(os.path.join(electro_directory,file), set_cycle=2)

        split_current = np.array_split(cv_reader.current, len(cv_reader.voltage)/5)
        split_voltage = np.array_split(cv_reader.voltage, len(cv_reader.voltage)/5)
        mean_current = [np.mean(current) for current in split_current]
        voltage = [voltage[0] for voltage in split_voltage]
        cv_plot.plot(voltage, np.multiply(mean_current,1000))

data_path = os.path.join('../Results','Sensitivity_DI.npy')
try:
    resonance_wavelengths = np.load(data_path)
    print(len(resonance_wavelengths))
except FileNotFoundError:
    resonance_wavelengths = np.asarray([fit_fano_shape(os.path.join(photonics_directory,file),wave,background,reflectance_plot) for file in sorted_photonics_files])
    np.save(data_path, resonance_wavelengths)
resonance_wavelengths = np.asarray([fit_fano_shape(os.path.join(photonics_directory,file),wave,background,reflectance_plot) for file in sorted_photonics_files[:10]])
plt.show()
#resonance_wavelengths = resonance_wavelengths[resonance_wavelengths < 865]
#resonance_wavelengths = resonance_wavelengths[100:]

split_wavelengths = np.array_split(resonance_wavelengths, len(resonance_wavelengths)/30, axis = 0)

mean_split_wavelengths = [np.mean(resonance) for resonance in split_wavelengths]
std_split_wavelengths = [np.std(resonance) for resonance in split_wavelengths]
time_point = 55
time = np.arange(0,len(mean_split_wavelengths[time_point:]), 1)

resonance_plot.errorbar(time,mean_split_wavelengths[time_point:],std_split_wavelengths[time_point:])
#resonance_plot.set_ylim([858.5,860.5])
#resonance_plot.plot([70,70], [893,889], 'k--')

resonance_plot.text(4, 889.6, '1%')
resonance_plot.text(20, 890, '2%')
resonance_plot.text(45,890.5, '5%')
resonance_plot.text(80,891,'10%')
resonance_plot.text(120,892.7,'20%')

resonance_plot

cv_plot.set_xlabel('Voltage vs (Ag/AgCl)')
cv_plot.set_ylabel('Current ($\mu$A)')
cv_plot.legend(['DI', '1% NaCl', '2% NaCl', '5% NaCl', '10% NaCl', '20% NaCl', 'DI'])
resonance_plot.set_xlabel('Time (mins)')
resonance_plot.set_ylabel('Resonance Wavelength (nm)')
resonance_plot.set_ylim([889,893.1])
plt.subplots_adjust(wspace = 0.5)
plt.show()