from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from fibrosisoptimization.measure.data_loader import DataLoader
from fibrosisoptimization.measure.residuals import Residuals
from fibrosisoptimization.core.surface_data import SurfaceData


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

path = Path('/Users/arstanbek/Projects/FibrosisOptimization/data')
path_save = path.joinpath('figures')
data_path = path.joinpath('models', 'test_models')
segments_path = path.joinpath('models', 'left_ventricle', '17')
electrodes_path = path.joinpath('models', 'left_ventricle', '17')
layers_path = path.joinpath('models')

models = ['transmural', 'sub-endo', 'mid-wall', 'sub-epi']
labels = ['(a)', '(b)', '(c)', 'd']
subdirs = [4, 12, 13, 9]
active_segment = 12
lat_reference = 13
fs = 1 / (40 * 0.0015)

base_data = SurfaceData(ptp=1, lat=1)

lines = []
fig, axs = plt.subplots(ncols=3, sharex=True, sharey=False, figsize=(8, 3.5))
for i, model in enumerate(models):
    for surface in ['endo', 'epi']:
        data_loader = DataLoader(surface_name=surface,
                                 segments_path=segments_path,
                                 electrodes_path=electrodes_path)
        data_loader.data_path = data_path.joinpath(model)

        residuals = Residuals(data_loader, lat_reference, fs, interpolate=True)
        residuals.base_data = base_data
        residuals.update_target('0')

        lat_array = []
        ptp_array = []
        for j in range(1, subdirs[i] + 1):
            subdir = '{}'.format(j)
            surface_data = residuals.update(subdir)

            segment_mask = surface_data.segments == active_segment

            lat_array.append(surface_data.lat[segment_mask])
            ptp_array.append(surface_data.ptp[segment_mask])

        lat_array = - np.array(lat_array)
        ptp_array = np.array(ptp_array)

        if 'endo' in surface:
            line, = axs[0].plot(np.mean(ptp_array, axis=1), marker='o', ms=3,
                                label=labels[i])
            lines.append(line)
            continue

        axs[1].plot(np.mean(ptp_array, axis=1), marker='o', ms=3,
                    label=labels[i])
        axs[2].plot(np.mean(lat_array, axis=1), marker='o', ms=3,
                    label=labels[i])

axs[0].set_ylabel(r'Mean error', fontdict={'fontsize': 9})
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
# fig.savefig(path_save.joinpath('segment_convergence.png'), dpi=300)
plt.show()
