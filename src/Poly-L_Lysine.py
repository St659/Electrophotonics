from src.EIS_Reader import EISPlotter
import matplotlib.pyplot as plt

eis_directory = '../Data/PolyLLysine'

plotter = EISPlotter(eis_directory,average=True, block=False)

plotter.mag_plot.legend(['0 min', '30 min', '60 min'], loc='center right')
plt.show()
