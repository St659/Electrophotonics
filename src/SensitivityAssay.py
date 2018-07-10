from src.GratingDataCollector import WhiteLight_Data_Reader
import matplotlib.pyplot as plt
import os
import numpy as np
directory = '../Data/Sensitivity_Assay'

white_light_reader = WhiteLight_Data_Reader()

#white_light_reader.single_file(directory,'sensitivity_assay_data')

files = os.listdir(directory)

fig,ax = plt.subplots()


reflectance = np.genfromtxt(os.path.join(directory,files[1]), delimiter=',')
print(reflectance)
ax.plot(reflectance)

plt.show()