from src.GratingDataCollector import grating_fit
import os
import numpy as np
import scipy as sci
import matplotlib.pyplot as plt
import glob
import scipy.stats as stats
import scipy.signal as signal


def linear_fit(m,x,c):
    return m*x + c
def subtract_linear_background(wavelength, reflectance):
    slope, intercept, r, p, s = stats.linregress([wavelength[0], wavelength[-1]], [reflectance[0], reflectance[-1]])
    line_fit = np.apply_along_axis(linear_fit, 0, wavelength, slope, intercept)
    return np.subtract(reflectance, line_fit)

def plot_fit_resonance(data_directory, ax):


    file_names = os.listdir(data_directory)

    wave = np.linspace(498.6174, 1103.161, 3648)

    w, background = np.genfromtxt(os.path.join(data_directory, 'ref.csv'), unpack=True, delimiter=',')
    file_names.remove('ref.csv')

    w, grating_reflectance = np.genfromtxt(os.path.join(data_directory, file_names[0]), unpack=True, delimiter=',')

    normalised_reflectance = np.divide(grating_reflectance, background)

    print('Detected Peaks: ' + str(signal.find_peaks_cwt(normalised_reflectance,[8,10])))




    min_wavelength = np.argmax(wave > 700)
    max_wavelength = np.argmin(wave < 950)

    wavelengths_fit = wave[min_wavelength:max_wavelength]



    reflectance_fit = subtract_linear_background(wavelengths_fit,normalised_reflectance[min_wavelength:max_wavelength])
    #reflectance_fit = normalised_reflectance[min_wavelength:max_wavelength]



    peak_reflectance_arg = np.argmax(reflectance_fit)
    data_point_range = 200
    min_peak_reflectance = peak_reflectance_arg - int(data_point_range/2)
    max_peak_reflectance = peak_reflectance_arg + int(data_point_range/2)


    print(wavelengths_fit[peak_reflectance_arg])
    try:
        popt, pcov = sci.optimize.curve_fit(grating_fit,
                                            wavelengths_fit[min_peak_reflectance:max_peak_reflectance],
                                            reflectance_fit[min_peak_reflectance:max_peak_reflectance],
                                            maxfev=15000,
                                            p0=[1,1,1,wavelengths_fit[peak_reflectance_arg],1])
        print(popt)


        ax.plot(wavelengths_fit[min_peak_reflectance:max_peak_reflectance],
                grating_fit(wavelengths_fit[min_peak_reflectance:max_peak_reflectance], *popt),'--')
        ax.plot(wavelengths_fit[min_peak_reflectance:max_peak_reflectance],
                reflectance_fit[min_peak_reflectance:max_peak_reflectance])
        return popt[2],popt[-2]
    except RuntimeError:
        print('Fit Failed')


data_directory = '../Data/Photonics_Quality'
fig, (reflectance_plot, resonance_plot) = plt.subplots(1,2)
sub_dirs = glob.glob(os.path.join(data_directory, '*'))
print(sub_dirs)

resonance = [plot_fit_resonance(directory,reflectance_plot) for directory in sub_dirs]

for res in resonance:
    qfactor = res[1]/((res[1]+res[0]/2) - (res[1]-res[0]/2))
    resonance_plot.plot(qfactor,res[1],'o')

reflectance_plot.set_ylabel('Normalised Relfectance')
reflectance_plot.set_xlabel('Wavelength (nm)')


resonance_plot.set_ylabel('Resonance Wavelength (nm)')
resonance_plot.set_xlabel('Linewidth (nm)')
plt.show()



