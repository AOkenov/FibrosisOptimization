from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

import matplotlib as mpl


mpl.rcParams['axes.linewidth'] = 0.5
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['xtick.minor.width'] = 0.5
mpl.rcParams['ytick.major.width'] = 0.5
mpl.rcParams['ytick.minor.width'] = 0.5
mpl.rcParams['axes.titlesize'] = 'medium'
mpl.rcParams['xtick.minor.size'] = 1
mpl.rcParams['ytick.minor.size'] = 1

font_properties = {'family': 'serif', 
                   'color':  'black', 
                   'weight': 'normal', 
                   'size': 12}

path = Path('/Users/arstanbek/Thor/projects/fibrosisoptimization/data')
path_save = Path('/Users/arstanbek/Projects/fibrosis-workspace/fibrosisoptimization/data/figures')
experiment = 'odp_period'
subdirs = ['initial', 'endo']
dt = 0.003

path_exp = path.joinpath('rotor', experiment)
plt.figure()

for subdir in subdirs:
    count = np.load(path_exp.joinpath(subdir, 'period_count.npy'))
    time_start = np.load(path_exp.joinpath(subdir, 'time_start.npy'))
    time_stop = np.load(path_exp.joinpath(subdir, 'time_stop.npy'))

    mask = count >= 20

    period = (time_stop[mask] -  time_start[mask]) / (count[mask] - 1)

    print(np.mean(period))

    plt.hist(period)
plt.show()
