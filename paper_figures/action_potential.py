from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

import matplotlib as mpl

from scipy import signal


mpl.rcParams['axes.linewidth'] = 0.5
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['xtick.minor.width'] = 0.5
mpl.rcParams['ytick.major.width'] = 0.5
mpl.rcParams['ytick.minor.width'] = 0.5
mpl.rcParams['axes.titlesize'] = 'medium'
mpl.rcParams['xtick.minor.size'] = 1
mpl.rcParams['ytick.minor.size'] = 1

font_properties = {'family': 'serif', 
                   'color': 'black',
                   'weight': 'normal', 
                   'size': 12}

path = Path('./data')
path_save = Path('./data/figures')
experiment = 'rotor'
subdirs = ['initial', 'endo']
dt = 0.003

path_exp = path.joinpath(experiment)

offsets = [19, 18]

peaks = []

fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(6, 4),
                        gridspec_kw={'width_ratios': [5, 100]})

for i, (subdir, offset) in enumerate(zip(subdirs, offsets)):
    act_pot = np.load(path_exp.joinpath(subdir, 'act_pot.npy'))
    peak = signal.find_peaks(act_pot, height=0.5, distance=20)[0]
    peaks.append(peak)
    print(dt * np.mean(np.diff(peak[:-1])))
    time = dt * np.arange(len(act_pot)) - offset
    axs[i, 1].plot(time, act_pot, lw=1.5)
    axs[i, 1].set_ylabel('$u$', fontdict={'fontsize': 12})
    axs[i, 1].set_xlabel('$t$', fontdict={'fontsize': 12})
    axs[i, 1].set_xlim([0., 258])

for i, label in enumerate(['(a)', '(b)']):
    axs[i, 0].axis('off')
    axs[i, 0].text(0.5, 1, label, rotation='horizontal', ha='center',
                   va='center', fontdict=font_properties)

plt.tight_layout()
# print(peaks)
plt.show()

# fig.savefig(path_save.joinpath('action_potentials.png'), dpi=300)
