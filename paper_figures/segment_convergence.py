from pathlib import Path
import copy
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from fibropt.measure.electrodes_data_updater import ElectrodesDataUpdater


mpl.rcParams['axes.linewidth'] = 0.5
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['xtick.minor.width'] = 0.5
mpl.rcParams['ytick.major.width'] = 0.5
mpl.rcParams['ytick.minor.width'] = 0.5
mpl.rcParams['axes.titlesize'] = 'medium'
mpl.rcParams['xtick.minor.size'] = 1
mpl.rcParams['ytick.minor.size'] = 1


font_properties = {'family': 'serif', 'color':  'black', 'weight': 'normal', 'size': 12}

path_save = Path('/Users/arstanbek/Projects/fibrosis-workspace/fibrosisoptimization/data/figures')
path = Path('/Users/arstanbek/Thor/projects/fibrosisoptimization/data')
experiments = ['transmural', 'sub-endo', 'mid-wall', 'sub-epi']
patterns_label = ['Transmural', 'Sub-endocardial', 'Mid-myocardial', 'Sub-epicardial']
subdirs = [4, 12, 13, 9]

lines = []
fig, axs = plt.subplots(ncols=3, sharex=True, sharey=False , figsize=(8, 3.5),)
for i, experiment in enumerate(experiments):
    for surface in ['endo', 'epi']:
        active_segments = np.load(path.joinpath(experiment, '0', 'labels.npy'))

        data_updater = ElectrodesDataUpdater(path.joinpath(experiment), surface, lat_reference=0.78)

        els_data_target = copy.deepcopy(data_updater.update(0, fs=1 / (40 * 0.0015)))
        lat_array = []
        ptp_array = []
        for j in range(1, subdirs[i] + 1):
            els_data = data_updater.update(j, fs=1 / (40 * 0.0015))
            els_data = els_data_target - els_data

            lat_array.append(els_data.lat[data_updater.active_electrodes_mask(active_segments)])
            ptp_array.append(els_data.amplitude[data_updater.active_electrodes_mask(active_segments)])

        lat_array = - np.array(lat_array)
        ptp_array = np.array(ptp_array)

        if 'endo' in surface:
            line, = axs[0].plot(np.mean(ptp_array, axis=1), marker='o', ms=3, label=patterns_label[i])
            lines.append(line)
            continue

        axs[1].plot(np.mean(ptp_array, axis=1), marker='o', ms=3, label=patterns_label[i])
        axs[2].plot(np.mean(lat_array, axis=1), marker='o', ms=3, label=patterns_label[i])

axs[0].set_ylabel(r'Mean error',fontdict={'fontsize': 9})
axs[1].set_ylabel(r'Mean error', fontdict={'fontsize': 9})
axs[2].set_ylabel(r'Mean error', fontdict={'fontsize': 9})

for ax in axs:
    ax.set_xticks(list(range(0, 13, 2)))
    ax.set_xticklabels(list(range(1, 14, 2)))
    ax.set_xlabel('Iteration', fontdict={'fontsize': 9})
    # ax.set_ylabel('Mean error')
    # ax.legend()
    ax.grid(visible=True)
    
legend = fig.legend(title='Fibrosis patterns',
                    handles=lines, loc='lower center', 
                    bbox_to_anchor=(0.5, 0.8), ncol=4, fontsize=9)

for i, label in enumerate(['(a)', '(b)', '(c)']):
    axs[i].text(0.5, -0.35, label, transform=axs[i].transAxes,
                    ha='center', va='center', fontdict=font_properties)
    
plt.tight_layout(pad=0.1, h_pad=0.1, w_pad=0.8)
plt.subplots_adjust(top=0.8, bottom=0.25, right=0.98, left=0.1)
fig.savefig(path_save.joinpath('segment_convergence.png'), dpi=300)
plt.show()

