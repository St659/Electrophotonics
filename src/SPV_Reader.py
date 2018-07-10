import unittest
import numpy as np
import scipy.stats as stats

class SPV_Reader():

    def __init__(self, file):
        file = file
        self.header = 0
        with open(file, encoding='utf-8', errors='ignore') as f:
            if '.mpt' in file:
                pass
            else:
                raise ValueError
            read_data = f.readlines()
            for line in read_data:
                if 'Nb header' in line:
                    strip_line = line.strip('\\n')
                    split_line = strip_line.split(" ")
                    self.header = int(split_line[4])

        data = np.genfromtxt(file, skip_header=self.header, unpack=True)
        current = data[11]

        if np.isnan(current).any():
            self.current = [x for x in current if not np.isnan(x)][1:]
        else:
            self.current = [x for x in current if x != 0][1:]

        voltage_min = np.round(data[12][0], decimals=1)
        voltage_max = np.round(data[12][-1], decimals=1)
        self.voltage = np.linspace(voltage_min, voltage_max, len(self.current))
        self.normalised_current = self.normalise_current(self.current, self.voltage)

    def normalise_current(self, current, voltage):

        slope,intercept,r,p,s = stats.linregress([voltage[0], voltage[-1]], [current[0], current[-1]])
        line_fit = np.apply_along_axis(self.linear_fit,0, voltage, slope, intercept)
        return np.subtract(current,line_fit)

    def linear_fit(self,x,slope,intercept):
        return slope*x + intercept



class SPV_Reader_Test(unittest.TestCase):

    def test_spv_reader(self):
        file = 'E:\\Chrome Download\\2min etch\\2min etch\\Electrochemistry\\SPV\\Methylene Blue\\100uM MB 100mM PB square wave 2mv step 50mV 80hz_C01.mpt'
        spv_reader = SPV_Reader(file)
        self.assertTrue(spv_reader)

    def test_spv_current(self):
        file = 'E:\\Chrome Download\\2min etch\\2min etch\\Electrochemistry\\SPV\\Methylene Blue\\100uM MB 100mM PB square wave 2mv step 50mV 80hz_C01.mpt'
        spv_reader = SPV_Reader(file)
        spv_current = spv_reader.current
        spv_voltage = spv_reader.voltage
        self.assertEquals(len(spv_current), len(spv_voltage))
        self.assertEquals(spv_voltage[0], -0.4)
        self.assertEquals(spv_voltage[-1], 0.1)

    def test_get_header(self):
        file = 'E:\\Chrome Download\\2min etch\\2min etch\\Electrochemistry\\SPV\\Methylene Blue\\100uM MB 100mM PB square wave 2mv step 50mV 80hz_C01.mpt'
        spv_reader = SPV_Reader(file)
        self.assertEquals(spv_reader.header, 48)

    def test_get_header_loop(self):
        file = 'E:\\Chrome Download\\2min etch\\2min etch\\Electrochemistry\\SPV\\Square Wave Loop\\Methylene Blue\\100uM MB 100mM PB_01_SWV_C01_loop0.mpt'
        spv_reader = SPV_Reader(file)
        self.assertEquals(spv_reader.header, 3)