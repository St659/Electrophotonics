import numpy as np
import os
import matplotlib.pyplot as plt

directory = os.getcwd()
precontact_directory = '../Data/S1813_Resist/Pre_Contact'
postcontact_directory = '../Data/S1813_Resist/Post_Contact'





wave = np.linspace(498.6174,1103.161,3648)



#Refelectance before putting contacts on
precontact_files = os.listdir(precontact_directory)
precontact_background = os.path.join(precontact_directory, precontact_files[1])
precontact_reflect_raw = os.path.join(precontact_directory,precontact_files[-1])
fig, ax = plt.subplots()
wavelength,mirror = np.genfromtxt(precontact_background,unpack=True, delimiter=',')
wavelength,precontact_reflectance = np.genfromtxt(precontact_reflect_raw, unpack=True, delimiter=',')
normalised_grating_reflectance = np.divide(precontact_reflectance,mirror)
ax.plot(wave,normalised_grating_reflectance)
ax.set_xlim([800,1000])
ax.set_ylim([0,1])

#Reflectance after putting contacts on and changing bias voltage from 0 - 8V

fig2, ax2 = plt.subplots()
postcontact_files = os.listdir(postcontact_directory)
post_contact_background = os.path.join(postcontact_directory,postcontact_files[-1])

legends_list = list()
wavelength, postcontact_mirror = np.genfromtxt(post_contact_background, unpack=True,delimiter=',')
wavelength, postcontact_0 = np.genfromtxt(os.path.join(postcontact_directory,postcontact_files[1]), unpack=True,delimiter=',')
print(postcontact_files[1:10])
for file in postcontact_files[1:10]:
    postcontact_reflecatance_file = os.path.join(postcontact_directory, file)
    wavelength,postcontact_reflectance = np.genfromtxt(postcontact_reflecatance_file, unpack=True,delimiter=',')
    postcontact_normalised_reflectance = np.divide(postcontact_reflectance,postcontact_mirror)
    ax2.plot(wave,postcontact_normalised_reflectance)
    legends_list.append(file[0] + 'V')
ax2.set_xlim([800,1000])
ax2.set_ylim([0,1])
ax2.legend(legends_list)

ax2.set_xlabel('Wavelength (nm)')
ax.set_xlabel('Wavelength (nm)')
ax.set_ylabel('Reflectance')
ax2.set_ylabel('Reflectance')

plt.show()

