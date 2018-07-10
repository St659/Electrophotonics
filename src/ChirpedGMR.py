import numpy as np
from src.hyperspectral_imaging import get_hyperspectral_image
from src.GratingDataCollector import grating_fit
import matplotlib.pyplot as plt
import os
from PIL import Image
import matplotlib.animation as animation
import itertools
import scipy as sci

def crop_image_file(image, vertical_slice, horizontal_slice):
    return np.asarray(Image.open(image))[vertical_slice, horizontal_slice]
data_directory = '../Data/Chirped GMR'
hyperspectral_data_directory = os.path.join(data_directory,'image')
chirp_image_data_directory = os.path.join(data_directory,'chirp_images')

chirp_image_directories = os.listdir(chirp_image_data_directory)
chirp_image_directories.remove('.DS_Store')
chirp_image_directories.remove('2salt')


fig1, hyperspectral_plot = plt.subplots()
fig2, (image_plot,mean_plot,fit_plot,peak_plot) = plt.subplots(1,4)
fig_images, (image_1, image_2, image_3, image_4, image_5) = plt.subplots(1,5)
image_plot_list = [image_1, image_2, image_3, image_4, image_5]
salt_02_vertical_slice = slice(150,-120)
salt_02_horizontal_slice = slice(150,-500)
salt_2_vertical_slice = slice(150,-120)
salt_2_horizontal_slice = slice(65,-585)

vertical_slices = [120,111,124,114,109]
horizontal_slices = [150,150,150,150,150]


chirp_image_filepaths = list()

#Get the file paths for the image folders
for chirp_sub_directories in chirp_image_directories:
    chirp_sub_directories_path = os.path.join(chirp_image_data_directory, chirp_sub_directories)
    for directory in os.listdir(chirp_sub_directories_path):
        chirp_image_files_path = os.path.join(chirp_sub_directories_path, directory)
        try:
            chirp_image_files = os.listdir(chirp_image_files_path)
            chirp_image_filepaths.append(chirp_image_files_path)
        except NotADirectoryError:
            pass

colour = ['r','g','b','k','c']
position = np.arange(0,350,1)

mean_peak_pos = list()
std_peak_pos = list()
for file_path, image_plot, vertical_slice, horizontal_slice, col in zip(chirp_image_filepaths, image_plot_list, horizontal_slices, horizontal_slices, colour):
    chirp_image_files = os.listdir(file_path)
    plot_image = True
    peak_positions = list()
    print(file_path)

    for file in chirp_image_files[:50]:
        try:
            chirp_image_file_path = os.path.join(chirp_image_files_path, file)
            image = np.asarray(Image.open(chirp_image_file_path))
            cropped_image = image[
                slice(vertical_slice, vertical_slice + 250), slice(horizontal_slice, horizontal_slice + 350)]
            if plot_image:
                image_plot.imshow(cropped_image)
            cropped_image_mean = np.mean(cropped_image, axis=0)
            mean_peak = np.argmax(cropped_image_mean)
            mean_plot.plot(cropped_image_mean)
            try:
                popt, pcov = sci.optimize.curve_fit(grating_fit,
                                                    position,
                                                    cropped_image_mean,
                                                    maxfev=15000,
                                                    p0=[1, 1, 1, position[mean_peak], 1])
                fit_plot.plot(position,grating_fit(position, *popt),c=col)
                peak_positions.append(popt[2])
            except RuntimeError:
                print('Fit Failed')


                plot_image = False
        except FileNotFoundError:
            pass
    mean_peak_pos.append(np.mean(peak_positions,axis=0))
    std_peak_pos.append(np.std(peak_positions, axis = 0))

concentrations = np.arange(0,len(mean_peak_pos),1)
peak_plot.errorbar(concentrations,mean_peak_pos,std_peak_pos, fmt='o')
    # try:
    #
    #
    #
    #     # image_files, = [ani_image_plot.imshow(image, interpolation='nearest', cmap='hot',
    #     #                        animated=True)]
    #     # images.append(image_files)
    #     cropped_image = image[vertical_slice, horizontal_slice]
    #     cropped_image_mean = np.mean(cropped_image, axis=0)
    #     mean_peak = np.argmax(cropped_image_mean)
    #     mean_plot.plot(cropped_image_mean)




# peak_positions = list()
# image_plots = list()
# print(chirp_image_directories)
#
# for chirp_sub_directories, horizontal_slice,vertical_slice, ani_image_plots in zip(chirp_image_directories, itertools.cycle(horizontal_slices),itertools.cycle(vertical_slices), image_plot_list):
#     print(chirp_sub_directories)
#     chirp_sub_directories_path =os.path.join(chirp_image_data_directory,chirp_sub_directories)
#     for directory, ani_image_plot in zip(os.listdir(chirp_sub_directories_path), ani_image_plots):
#         print(ani_image_plot)
#
#         plot_image = True
#         chirp_image_files_path = os.path.join(chirp_sub_directories_path, directory)
#
#         try:
#
#             chirp_image_files = os.listdir(chirp_image_files_path)
#             print(directory)
#             images = list()
#
#
#
#
#
#                 except OSError:
#                             print('Not a TIFF File')
#
#             image_plots.append(images)
#             peak_plot.plot(peak_positions,'o')
#
#
#         except NotADirectoryError:
#             print('Not A Directory')
# # ani = animation.ArtistAnimation(fig_images, image_plots, interval=100, blit=True,
# #                                                     repeat_delay=0)
# image_file = os.listdir(os.path.join(chirp_image_data_directory, '2salt/2salt_1'))[1]
# image = np.asarray(Image.open(os.path.join(os.path.join(chirp_image_data_directory, '2salt/2salt_1'),image_file)))
# image_plot.imshow(image[salt_2_vertical_slice,salt_2_horizontal_slice])


#HyperSpectral Imaging

hyperspectral_wavelengths = np.arange(850,900.5,0.5)
hyperspectral_results_file = '../Results/ChirpedGMR/Hyperspectral/chirpGMR.npy'
hyperspectral_image = get_hyperspectral_image(hyperspectral_results_file, hyperspectral_data_directory,hyperspectral_wavelengths)
hyperspectral_plot.imshow(hyperspectral_image,interpolation='nearest', cmap='hot')


plt.show()