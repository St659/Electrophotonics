import os
from src.hyperspectral_imaging import natural_key, get_hyperspectral_image, plot_spectra
from src.GratingDataCollector import grating_fit
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import fnmatch
import scipy as sci
from src.SPV_Reader import  SPV_Reader
from src.EIS_Reader import EISReader
from src.EC_Lab_CVReader import CVReader

data_directory = '../Data/Azide_Diaz'
results_directory = '../Results/Azide_Diaz'
elec_directory = os.path.join(data_directory,'Elec')

diaz_cv_directory = os.path.join(elec_directory,'Diaz_CV')
kpi_cv_directory = os.path.join(elec_directory,'KPI_CV')
nb_cv_directory = os.path.join(elec_directory,'NB_CV')

kpi_eis_directory = os.path.join(elec_directory,'KPI_EIS')
diaz_eis_directory = os.path.join(elec_directory,'Diaz_EIS')
nb_eis_directory = os.path.join(elec_directory, 'NB_EIS')

kpi_swv_directory = os.path.join(elec_directory, 'KPI_SWV')
nb_swv_directory = os.path.join(elec_directory,'NB_SWV')


photonics_directory = os.path.join(data_directory,'Photonics')
image_results_directory = os.path.join(results_directory,'image_results')

wavelengths = np.arange(800,850.5,0.5)
sub_directories = os.listdir(photonics_directory)
sorted_sub_directories = sorted(sub_directories, key=natural_key)

fig, mean_plot = plt.subplots()
fig2, image_plot = plt.subplots()
fig3, pixel_plot = plt.subplots()

fig4, diaz_cv_plot = plt.subplots()
fig5, diaz_mag_plot = plt.subplots()
diaz_phase_plot = diaz_mag_plot.twinx()

fig6, kpi_cv_plot = plt.subplots()
fig7, nb_cv_plot = plt.subplots()

fig8, nb_swv_plot = plt.subplots()
fig9, kpi_swv_plot = plt.subplots()


fig10, kpi_mag_plot = plt.subplots()
kpi_phase_plot = kpi_mag_plot.twinx()

fig11, nb_mag_plot = plt.subplots()
nb_phase_plot = nb_mag_plot.twinx()

vertical_slice = slice(475,-250)
horizontal_slice = slice(475,-350)

mean = list()
std = list()
images = list()
pixel_intensity = list()
fit_slice_vertical = slice(300, 310)
mean_resonance_fit = list()
std_resonance_fit = list()

for file in sorted(os.listdir(diaz_cv_directory),key=natural_key)[6:]:
    file_path = os.path.join(diaz_cv_directory,file)
    try:
        cv_reader = CVReader(file_path)
        diaz_cv_plot.plot(cv_reader.voltage, cv_reader.current)
    except ValueError:
        print('Not a parsed file')

for file in sorted(os.listdir(diaz_eis_directory),key=natural_key)[6:]:
    file_path = os.path.join(diaz_eis_directory, file)
    try:
        eis_reader = EISReader(file_path)
        diaz_mag_plot.loglog(eis_reader.eis.frequency, eis_reader.eis.magnitude)
        diaz_phase_plot.semilogx(eis_reader.eis.frequency,eis_reader.eis.phase, '--')
    except ValueError:
        print('Not an .mpt File')

kpi_eis_legends = list()
for file in sorted(os.listdir(kpi_eis_directory),key=natural_key)[6:]:
    file_path = os.path.join(kpi_eis_directory, file)
    try:
        eis_reader = EISReader(file_path)
        kpi_mag_plot.loglog(eis_reader.eis.frequency, eis_reader.eis.magnitude)
        kpi_phase_plot.semilogx(eis_reader.eis.frequency,eis_reader.eis.phase, '--')
        legend = file.split('_')[0]
        kpi_eis_legends.append(legend)
    except ValueError:
        print('Not an .mpt File')
kpi_mag_plot.legend(kpi_eis_legends)
for file in sorted(os.listdir(nb_eis_directory),key=natural_key):
    file_path = os.path.join(nb_eis_directory, file)
    try:
        eis_reader = EISReader(file_path)
        nb_mag_plot.loglog(eis_reader.eis.frequency, eis_reader.eis.magnitude)
        nb_phase_plot.semilogx(eis_reader.eis.frequency,eis_reader.eis.phase, '--')
    except ValueError:
        print('Not an .mpt File')

for file in sorted(os.listdir(kpi_cv_directory),key=natural_key):
    file_path = os.path.join(kpi_cv_directory,file)
    try:
        cv_reader = CVReader(file_path,set_cycle=2)
        kpi_cv_plot.plot(cv_reader.voltage, cv_reader.current)
    except ValueError:
        print('Not a parsed file')

for file in sorted(os.listdir(nb_cv_directory),key=natural_key):
    file_path = os.path.join(nb_cv_directory,file)
    try:
        cv_reader = CVReader(file_path,set_cycle=2)
        if cv_reader.scan_rate == 100:
            nb_cv_plot.plot(cv_reader.voltage, cv_reader.current)
    except ValueError:
        print('Not a parsed file')

for file in sorted(os.listdir(nb_swv_directory), key=natural_key):
    file_path = os.path.join(nb_swv_directory,file)
    try:
        swv_reader = SPV_Reader(file_path)
        nb_swv_plot.plot(swv_reader.voltage, swv_reader.normalised_current)
    except ValueError:
        print('Not a parsed file')
for file in sorted(os.listdir(kpi_swv_directory), key=natural_key):
    file_path = os.path.join(kpi_swv_directory,file)
    try:
        swv_reader = SPV_Reader(file_path)
        kpi_swv_plot.plot(swv_reader.voltage, swv_reader.normalised_current)
    except ValueError:
        print('Not a parsed file')
try:
    results_file_paths = os.listdir(image_results_directory)
    print(results_file_paths)
    sorted_results_file_paths = sorted(results_file_paths, key=natural_key)
    print(sorted_results_file_paths)

    for sub_directory in sorted_sub_directories[6:]:
        sub_directory_image_path = os.path.join(photonics_directory, os.path.join(sub_directory, 'image'))
        pixel_intensity = list()
        print(sub_directory)
        for file in os.listdir(sub_directory_image_path):
            base = os.path.splitext(file)[0]
            print(base)
            npy_file = base + '.npy'
            npy_path = os.path.join(sub_directory_image_path, npy_file)
            try:
                pixel_data = np.load(npy_path)
                pixel_intensity.append(pixel_data)
            except FileNotFoundError:
                pixel_data = np.genfromtxt(os.path.join(sub_directory_image_path, file), delimiter=',')
                pixel_intensity.append(pixel_data[fit_slice_vertical,fit_slice_vertical])
                np.save(os.path.join(sub_directory_image_path,base),pixel_data[fit_slice_vertical,fit_slice_vertical])
        pixel_array = np.asarray(pixel_intensity)
        print(pixel_array.shape)
        columns = pixel_array.shape[1]
        rows = pixel_array.shape[2]
        fitted_resonance = list()

        for col in np.arange(0, columns, 1):
            for row in np.arange(0, rows, 1):

                pixel_values = pixel_array[:, col, row]
                peak_reflectance_arg = np.argmax(pixel_values)
                try:
                    popt, pcov = sci.optimize.curve_fit(grating_fit,
                                                        wavelengths,
                                                        pixel_values,
                                                        maxfev=15000,
                                                        p0=[1, 1, 1, wavelengths[peak_reflectance_arg], 1])
                    pixel_plot.plot(wavelengths, grating_fit(wavelengths, *popt), 'o')
                    resonance_wavelength = popt[-2]
                    fitted_resonance.append(resonance_wavelength)
                except RuntimeError:
                    print('Fit Failed')

        mean_resonance_fit.append(np.mean(resonance_wavelength))
        std_resonance_fit.append(np.std(resonance_wavelength))

    for sub_directory in sorted_results_file_paths[6:]:
        sub_directory_image_path = os.path.join(photonics_directory, os.path.join(sub_directory, 'image'))
        results_image_path = os.path.join(image_results_directory, sub_directory)
        image = get_hyperspectral_image(results_image_path, sub_directory_image_path, wavelengths)
        images.append(
            [image_plot.imshow(image[vertical_slice, horizontal_slice], interpolation='nearest', cmap='hot',
                               animated=True)])
        mean.append(np.mean(image[vertical_slice, horizontal_slice]))
        std.append(np.std(image[vertical_slice, horizontal_slice]))
except ValueError:
    pass




#pixel_plot.plot(wavelengths,grating_fit(wavelengths,*popt))
time_points = np.arange(0,len(mean_resonance_fit),1)
mean_plot.errorbar(time_points,mean_resonance_fit, std_resonance_fit, fmt='o')
ani = animation.ArtistAnimation(fig2, images, interval=500, blit=True,
                                 repeat_delay=0)

plt.show()