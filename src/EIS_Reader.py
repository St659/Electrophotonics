import codecs
import matplotlib.pyplot as plt
import os
import numpy as np


class EISReader:

    def __init__(self, filename, set_cycle=0):
        with codecs.open(filename, 'r', encoding='utf-8', errors='ignore') as file:

            if '.mpt' in filename:
                pass
            else:
                raise ValueError

            file_lines = file.readlines()
            header_line = self.get_header_line_number(file_lines)
            print(header_line)

            self.eis = EISData()
            for line in file_lines[header_line:]:
                if not set_cycle:
                    set_cycle = float(line.split()[11])
                if float(line.split()[11]) == set_cycle:
                    eis_data = [float(line.split()[0]),float(line.split()[3]),float(line.split()[4])]

                    for data, data_list in zip(eis_data, self.eis.data_list):
                        data_list.append(data)

    def get_header_line_number(self,file_lines):
        for file in file_lines:

            if 'Nb header' in file:
                header_string = str(file)
                split_header_string =header_string.split()
                return int(split_header_string[-1])

class EISPlotter:
    def __init__(self, directory, average=False, block=True, legends=False):
        working_directory = os.getcwd()
        plt.style.use(['seaborn-white', 'seaborn-notebook'])
        sub_dirs =next(os.walk(directory))[1]
        print(sub_dirs)
        if sub_dirs:
            sub_directories = [os.path.join(directory,sub_dir) for sub_dir in sub_dirs]
        else:
            sub_directories = directory
        fig, self.mag_plot = plt.subplots()
        self.phase_plot = self.mag_plot.twinx()
        print(sub_directories)
        for directory in sub_directories:
            readers = [EISReader(file) for file in self.get_data_paths(os.path.join(working_directory,directory))]
            if average:
                mean_mag = np.mean(list([reader.eis.magnitude for reader in readers]),axis=0)
                print(mean_mag)
                mean_phase = np.mean(np.asarray([reader.eis.phase for reader in readers]).astype(np.float),axis=0)
                std_mag = np.std(list([reader.eis.magnitude for reader in readers]),axis=0)
                std_phase = np.std(list([reader.eis.phase for reader in readers]),axis=0)
                self.mag_plot.errorbar(readers[0].eis.frequency,mean_mag,std_mag)
                self.phase_plot.errorbar(readers[0].eis.frequency, mean_phase,std_phase,linestyle='--')
            else:
                for reader in readers:
                    print(reader.eis.frequency)
                    self.mag_plot.loglog(reader.eis.frequency, reader.eis.magnitude)
                    self.phase_plot.semilogx(reader.eis.frequency, reader.eis.phase, linestyle='--')
        self.mag_plot.set_xscale('log')
        self.mag_plot.set_yscale('log')
        self.phase_plot.set_xscale('log')
        self.mag_plot.set_xlabel('Frequency (Hz)')
        self.mag_plot.set_ylabel('|Z| ($\Omega$)')
        self.phase_plot.set_ylabel('$\\angle$ Z ($\degree$)')
        if legends:
            self.mag_plot.legend(legends)
        else:
            self.mag_plot.legend(sub_dirs)
        plt.show(block=block)

    def get_data_paths(self,directory):
        filenames = os.listdir(directory)
        paths = list()
        for name in filenames:
            if '.mpt' in name:
                new_name = os.path.join(directory, name)
                paths.append(new_name)
        print(paths)
        return paths



class EISData:
    def __init__(self):
        self.frequency = list()
        self.magnitude = list()
        self.phase = list()
        self.data_list = [self.frequency, self.magnitude, self.phase]

