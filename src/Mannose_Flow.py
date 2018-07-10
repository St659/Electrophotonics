import os
from src.hyperspectral_imaging import get_hyperspectral_image, natural_key, plot_spectra
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

data_directory = '../Data/Mannose_Hyperspec_Flow/image'
spectra_directory = '../Data/Mannose_Hyperspec_Flow/spectra'
results_directory = '../Results/Mannose_Hyperspec_Flow/numpy'

results = os.listdir(results_directory)



average_fig,ax2 = plt.subplots()
fig2, (ax3,ax4) = plt.subplots(1,2)
fig,ax = plt.subplots()
sub_directories = os.listdir(data_directory)
sub_directories.remove('.DS_Store')
wavelengths = np.arange(820, 870.5, 0.5)
spectra_wavelengths = np.linspace(498.6174, 1103.161, 3648)

results_files = os.listdir(results_directory)
sorted_files = sorted(results_files, key=natural_key)

images = list()
mean = list()
std =list()
initial = get_hyperspectral_image(os.path.join(results_directory,sorted_files[1]),os.path.join(data_directory,sorted_files[1]), wavelengths)
for file in sorted_files[2:]:
    if '.npy' in file:
        hyperspec = get_hyperspectral_image(os.path.join(results_directory,file),os.path.join(data_directory,file), wavelengths)
        hyperspec = np.subtract(hyperspec,initial)
        data_slice = slice(350,-150)
        side_slice = slice (350,-300)
        mean.append(hyperspec[data_slice, side_slice].mean())
        std.append(hyperspec[data_slice, side_slice].std())
        images.append([ax.imshow(hyperspec[data_slice, side_slice],interpolation='nearest', cmap='hot', animated=True)])
        image_file = file.split('.')[0] + '.png'
        #plt.savefig(os.path.join(results_directory,image_file))
        colorbar = ax.imshow(hyperspec[data_slice, side_slice],interpolation='nearest', cmap='hot', animated=True)


cbar = fig.colorbar(colorbar)



ax2.errorbar(np.arange(0,len(sorted_files[2:]),1)*6,mean,fmt='o')
ax2.set_ylabel('$\Delta \lambda$ (nm)')
ax2.set_xlabel('Time (mins)')
ani = animation.ArtistAnimation(fig, images, interval=500, blit=True,
                                 repeat_delay=0, )
#ani.save(os.path.join(results_directory,'mannose_flow_hyperspec.gif'),writer='imagemagick')
# spectra_sub_directories = os.listdir(spectra_directory)
#
# sorted_spectra_directories = sorted(spectra_sub_directories, key=natural_key)
# sorted_spectra_directories.pop(-1)
# max_wavelengths = list()
# for directory in sorted_spectra_directories[2:]:
#     print(directory)
#     max_wavelengths.append(plot_spectra(os.path.join(spectra_directory, directory), spectra_wavelengths, ax3))
# ax4.plot(max_wavelengths)


plt.show()