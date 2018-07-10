import unittest
import codecs
import numpy as np
import os
from scipy import asarray as ar,exp
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt

class CVReader():
    def __init__(self, filename, set_cycle = 0):

        with codecs.open(filename, 'r', encoding='utf-8', errors='ignore') as file:

            if '.mpt' in filename:
                pass
            else:
                raise ValueError
            file_lines = file.readlines()

            self.header_line = self.get_header_line_number(file_lines)
            columns_line = file_lines[self.header_line-1]
            self.scan_rate = self.get_scan_rate(file_lines[:self.header_line])
            self.current_column = self.get_column_header(columns_line, '<I>/mA')
            self.voltage_column = self.get_column_header(columns_line, 'Ewe/V')

            self.cycle_column = self.get_column_header(columns_line, 'cycle')
            self.redox_colum = self.get_column_header(columns_line,'ox/red')


            if not set_cycle:
                raw_forward, raw_reverse = self.get_cv_data(file_lines[self.header_line:])
            else:
                raw_forward, raw_reverse = self.get_cv_data(file_lines[self.header_line:], cycle=set_cycle)


            forward_voltage, forward_current, reverse_voltage, reverse_current = self.calculate_graph_data(raw_forward,raw_reverse)

            self.forward_current_mean = np.mean(forward_current, axis=0)
            forward_current_std = np.std(forward_current, axis=0)
            self.reverse_current_mean = np.mean(reverse_current, axis=0)
            reverse_current_std = np.std(reverse_current, axis=0)

            current_mean = np.concatenate((self.forward_current_mean, self.reverse_current_mean[::-1]), axis=0)
            current_std = np.concatenate((forward_current_std, reverse_current_std[::-1]), axis=0)
            voltage = np.concatenate((forward_voltage, reverse_voltage[::-1]), axis=0)
            self.fwhm = self.calculate_fwhm(forward_voltage, self.forward_current_mean)
            self.forward_voltage = forward_voltage
            self.reverse_voltage = reverse_voltage
            self.voltage = voltage
            self.current = current_mean
            self.peak_forward_voltage = forward_voltage[np.argmax(self.forward_current_mean)]
            self.peak_reverse_voltage = reverse_voltage[np.argmin(self.reverse_current_mean)]
            self.peak_current = np.max(self.current)
            self.get_max_voltages_between_limits(self.forward_voltage[0],self.forward_voltage[-1])
            file.close()

    def get_column_header(self, header, column_value):

        header_columns = header.split('\t')
        current_column = [i for i, column in enumerate(header_columns) if column_value in column]
        return current_column[0]

    def calculate_fwhm(self, voltage, current):
        spline = UnivariateSpline(voltage, current - np.max(current) / 2, s=0)

        try:
            r1, r2 = spline.roots()  # find the roots
            fwhm = [r1, r2]
            #print("FWHM:" + str((fwhm[1]-fwhm[0])*1000) + 'mV')
            return fwhm
        except ValueError:
            return [0,0]

    def get_max_voltages_between_limits(self, lower, upper):
        forward_voltage_limits = np.where(np.logical_and(self.forward_voltage >= lower, self.forward_voltage <= upper))
        reverse_voltage_limits = np.where(np.logical_and(self.forward_voltage >= lower, self.forward_voltage <= upper))
        forward_voltage_limits_values = self.forward_voltage[forward_voltage_limits[0][0]:forward_voltage_limits[0][-1]]
        reverse_voltage_limits_values = self.reverse_voltage[reverse_voltage_limits[0][0]:reverse_voltage_limits[0][-1]]
        self.peak_forward_voltage = forward_voltage_limits_values[
            np.argmax(self.forward_current_mean[forward_voltage_limits[0][0]:forward_voltage_limits[0][-1]])]
        self.peak_reverse_voltage = reverse_voltage_limits_values[
            np.argmin(self.reverse_current_mean[reverse_voltage_limits[0][0]:reverse_voltage_limits[0][-1]])]

    def gaus(self,x, a, x0, sigma):
        return a * exp(-(x - x0) ** 2 / (2 * sigma ** 2))

    def get_cv_data(self, file_lines, cycle =0):
        current_forward = list()
        reverse = list()
        voltage_reverse = list()
        forward = list()
        for line in file_lines:
            sl = line.split()

            if not cycle:
                cycle = int(float(sl[self.cycle_column]))

            if int(float(sl[self.cycle_column])) == cycle:

                if int(float(sl[self.redox_colum])) == 1:

                    forward.append([float(sl[self.voltage_column]), float(sl[self.current_column])])

                elif int(float(sl[self.redox_colum])) == 0:
                    reverse.append([float(sl[self.voltage_column]), float(sl[self.current_column])])

        forward.sort()
        reverse.sort()

        return forward, reverse

    def get_header_line_number(self, file_lines):
        for file in file_lines:
            if 'Nb header' in file:
                header_string = str(file)
                split_header_string = header_string.split()
                return int(split_header_string[-1])
    def get_scan_rate(self, file_lines):
        for line in file_lines:

            if 'dE/dt' in line:
                scan_string = str(line)
                scan_rate = scan_string.split(' ')
                for value in scan_rate:
                    try:
                        scan_rate = float(value)
                    except ValueError:
                        pass
                return scan_rate

    def calculate_graph_data(self,forward,reverse, average=False):
        forward_list = list()
        reverse_list = list()
        forward_current_list = list()
        reverse_current_list = list()
        subtracted_reverse_current_list = list()
        subtracted_forward_current_list = list()

        if not average:
            forward_list.append(forward)
            reverse_list.append(reverse)
        else:
            for f,r in zip(forward,reverse):

                forward_list.append(f)
                reverse_list.append(r)

        #print(forward_list)

        voltage_forward = np.linspace(forward_list[0][0][0], forward_list[0][-1][0], 1000)
        voltage_reverse = np.linspace(reverse_list[0][0][0], reverse_list[0][-1][0], 1000)
        for data in forward_list:
            voltage_temp = list()
            current_temp = list()
            for x in data:
                voltage_temp.append(x[0])
                current_temp.append(x[1])
            interp_currents = np.interp(voltage_forward, voltage_temp, current_temp)

            non_faradaic = np.interp(0, voltage_temp, current_temp)
            forward_current_list.append(interp_currents)
            subtracted_forward_current_list.append(np.subtract(interp_currents, non_faradaic))

        for data in reverse_list:
            voltage_temp = list()
            current_temp = list()
            for x in data:
                voltage_temp.append(x[0])
                current_temp.append(x[1])
            interp_currents = np.interp(voltage_reverse, voltage_temp, current_temp)
            non_faradaic = np.interp(0, voltage_temp, current_temp)
            reverse_current_list.append(interp_currents)
            subtracted_reverse_current_list.append(np.subtract(interp_currents, non_faradaic))

        forward_current = np.array(forward_current_list)
        reverse_current = np.array(reverse_current_list)

        sub_forward_current = np.array(subtracted_forward_current_list)
        sub_reverse_current = np.array(subtracted_reverse_current_list)
        #


        sub_forward_current_mean = np.mean(sub_forward_current, axis=0)
        sub_forward_current_std = np.std(sub_forward_current, axis=0)
        sub_reverse_current_mean = np.mean(sub_reverse_current, axis=0)
        sub_reverse_current_std = np.std(sub_reverse_current, axis=0)



        sub_current_mean = np.concatenate((sub_forward_current_mean, sub_reverse_current_mean[::-1]), axis=0)
        sub_current_std = np.concatenate((sub_forward_current_std, sub_reverse_current_std[::-1]), axis=0)






        return voltage_forward, forward_current, voltage_reverse, reverse_current

def get_data_paths(directory):
    filenames = os.listdir(directory)
    paths = list()
    for name in filenames:
        if '.mpt' in name:
            new_name = os.path.join(directory, name)
            paths.append(new_name)
    print(paths)
    return paths

def cv_plot_labels(cv_plot):
    cv_plot.set_xlabel('Voltage (V vs Ag/AgCl)')
    cv_plot.set_ylabel('Current  (mA)')


class CV_Plotter():
    def __init__(self, directory):

        fig, cv_plot = plt.subplots()
        working_directory = os.getcwd()
        cv_paths = get_data_paths(os.path.join(working_directory,directory))
        scan_rates = list()

        self._plot = plt

        for cv_path in cv_paths:
            cv_reader = CVReader(cv_path, set_cycle=2)
            cv_plot.plot(cv_reader.voltage, cv_reader.current)
            scan_rates.append(str(cv_reader.scan_rate) + ' mV/s')
        cv_plot.legend(scan_rates)
        cv_plot.set_xlabel('Voltage (V vs Ag/AgCl')
        cv_plot.set_ylabel('Current (mA)')
        plt.show()

    def get_data_paths(self,directory):
        filenames = os.listdir(directory)
        paths = list()
        for name in filenames:
            if '.mpt' in name:
                new_name = os.path.join(directory, name)
                paths.append(new_name)
        return paths


class CVReaderTest(unittest.TestCase):
    def setUp(self):
        files = os.listdir('../Data/Salt_Sensitivity_DI/Electrochemistry')
        filename = files[0]
        self.reader = CVReader(os.path.join('../Data/Salt_Sensitivity_DI/Electrochemistry',filename), set_cycle=2)

    def test_get_cv_data(self):
        self.assertEqual(len(self.reader.current), 2000)
        self.assertEqual(len(self.reader.voltage), 2000)
        self.assertEqual(self.reader.scan_rate,250)

    def test_get_header_lines(self):
        self.assertEqual(self.reader.header_line, 54)

    def test_get_current_column(self):
        self.assertEqual(self.reader.current_column, 8)
    def test_get_voltage_column(self):
        self.assertEqual(self.reader.voltage_column, 7)
    def test_get_cycle_column(self):
        self.assertEqual(self.reader.cycle_column, 9)
    def test_get_redox_column(self):
        self.assertEqual(self.reader.redox_colum, 1)


if __name__ == "__main__":
    file = 'E:\\Chrome Download\\blank_1_2.mpt'
    reader = CVReader(file)


