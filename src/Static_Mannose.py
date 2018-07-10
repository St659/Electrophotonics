import os
from src.hyperspectral_imaging import get_hyperspectral_image, plot_spectra, natural_key
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
data_directory = '../Data/Static Mannose Ecoli Hyperspec'
results_directory = '../Results/Static Mannose Ecoli Hyperspec'
spectra_data_directory = os.path.join(data_directory,'spectra')
image_data_directory = os.path.join(data_directory,'image')
spectra_results_directory = os.path.join(results_directory,'spectra')
image_results_directory = os.path.join(results_directory,'image')




results = os.listdir(results_directory)
hyperspectral_wavelengths = np.arange(820,875.5,0.5)

fig,(spectra_plot,spectra_maximum) = plt.subplots(1,2)
spectra_sub_directories = os.listdir(spectra_data_directory)
spectra_wavelengths = np.linspace(498.6174, 1103.161, 3648)

sorted_spectra_subdirectories = sorted(spectra_sub_directories,key=natural_key)
max_wavelengths = list()
# for directory in sorted_spectra_subdirectories:
#     print(directory)
#     max_wavelengths.append(plot_spectra(os.path.join(spectra_data_directory,directory), spectra_wavelengths, spectra_plot))
# spectra_maximum.plot(max_wavelengths)


fig2,image_plot = plt.subplots()
fig3, image_average = plt.subplots()

image_average.set_ylabel('$\Delta \lambda$ (nm)')
image_average.set_xlabel('Time (mins)')

mean = list()
std =list()
images = list()
image_subdirectories = os.listdir(image_data_directory)
results_subdirectories = os.listdir(image_results_directory)
image_subdirectories.remove('.DS_Store')
sorted_image_directories = sorted(image_subdirectories, key = natural_key)
#initial = get_hyperspectral_image(os.path.join(image_results_directory,sorted_image_directories[0]),os.path.join(image_data_directory,sorted_image_directories[0]), hyperspectral_wavelengths)
results_filenames = os.listdir(image_results_directory)
sorted_results_file = sorted(results_filenames,key=natural_key)


print('Results Files')
print(results_filenames)
initial= get_hyperspectral_image(os.path.join(image_results_directory,sorted_results_file[0]),os.path.join(image_data_directory,sorted_results_file[0]), hyperspectral_wavelengths)
for directory in sorted_results_file[1:]:
    print(directory)
    results_file = directory
    results_file_path = os.path.join(image_results_directory,results_file)
    hyperspec = get_hyperspectral_image(results_file_path,os.path.join(image_data_directory,directory), hyperspectral_wavelengths)
    hyperspec = np.subtract(hyperspec,initial)
    data_slice = slice(200,-200)
    side_slice = slice (0,-700)
    mean.append(hyperspec[data_slice, side_slice].mean())
    std.append(hyperspec[data_slice, side_slice].std())
    images.append([image_plot.imshow(hyperspec[data_slice, side_slice],interpolation='nearest', cmap='hot', animated=True)])
    colorbar = image_plot.imshow(hyperspec[data_slice, side_slice],interpolation='nearest', cmap='hot', animated=True)

image_average.errorbar(np.arange(0,len(sorted_results_file[1:]),1),mean,fmt='o')
cbar = fig.colorbar(colorbar)
ani = animation.ArtistAnimation(fig, images, interval=100, blit=True,
                                 repeat_delay=0)
plt.show()