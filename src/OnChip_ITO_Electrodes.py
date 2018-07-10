from src.EIS_Reader import EISReader
import os
import matplotlib.pyplot as plt

eis_directory = '../Data/On Chip ITO Electrodes'

eis_files = os.listdir(eis_directory)

fig, eis_mag = plt.subplots()
eis_phase = eis_mag.twinx()

for file in eis_files:
    print(file)
    eis_reader = EISReader(os.path.join(eis_directory,file), set_cycle=2)
    eis_mag.loglog(eis_reader.eis.frequency, eis_reader.eis.magnitude)
    eis_phase.semilogx(eis_reader.eis.frequency, eis_reader.eis.phase, '--')

eis_mag.set_xlabel('Frequency (Hz)')
eis_mag.set_ylabel('|Z| ($\Omega $)')
eis_mag.legend(['100 mM', '10 mM', '1mM','100 $\mu $M', '10 $\mu $M', '1 $\mu $M'],loc='center right')
eis_phase.set_ylabel('$\\angle$ ($\degree $)')
plt.show()