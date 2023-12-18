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
                   'color': 'black',
                   'weight': 'normal',
                   'size': 12}

path = Path('/Users/arstanbek/Projects/FibrosisOptimization/data')
path_save = path.joinpath('figures')

data_path = path.joinpath('models', 'left_ventricle', '68')
electrodes_path = path.joinpath('models', 'left_ventricle', '68')

data_loader = DataLoader(electrodes_path=electrodes_path, data_path=data_path)

base_data = SurfaceData(ptp=1, lat=1)
lat_reference = 13
fs = 1 / (40 * 0.0015)

lines = []
fig, axs = plt.subplots(ncols=3, sharex=True, sharey=False, figsize=(8, 3))

for surface in ['endo', 'epi']:
    data_loader.surface_name = surface

    residuals = Residuals(data_loader, lat_reference, fs, interpolate=False)
    residuals.base_data = base_data
    residuals.update_target('0')

    lat_array = []
    ptp_array = []
    for j in range(1,  203):
        subdir = '{}'.format(j)
        els_data = residuals.update(subdir)

        lat_array.append(els_data.lat)
        ptp_array.append(els_data.ptp)

    lat_array = - np.array(lat_array)
    ptp_array = np.array(ptp_array)

    if 'endo' in surface:
        line, = axs[0].plot(np.sum(ptp_array**2, axis=1))
        lines.append(line)
        continue

    axs[1].plot(np.sum(ptp_array**2, axis=1))
    axs[2].plot(np.sum(lat_array**2, axis=1))

for ax in axs:
    ax.set_xticks([0] + list(range(49, 201, 50)))
    ax.set_xticklabels([1] + list(range(50, 201, 50)))
    ax.set_xlabel('Iteration', fontdict={'fontsize': 9})
    ax.set_ylabel('Sum of squares error')
    ax.set_xlim([1, 205])
    ax.set_yscale('log')
    ax.grid(visible=True)

axs[0].set_ylim([0.02, 3.5])
axs[0].set_yticks([0.05, 0.2, 0.8, 3.2])
axs[0].set_yticklabels([0.05, '0.20', '0.80', '3.20'])

axs[1].set_ylim([0.02, 3.5])
axs[1].set_yticks([0.05, 0.2, 0.8, 3.2])
axs[1].set_yticklabels([0.05, '0.20', '0.80', '3.20'])

axs[2].set_ylim([2, 350])
axs[2].set_yticks([5, 20, 80, 320])
axs[2].set_yticklabels([5, 20, 80, 320])

for i, label in enumerate(['(a)', '(b)', '(c)']):
    axs[i].text(0.5, -0.35, label, transform=axs[i].transAxes,
                ha='center', va='center', fontdict=font_properties)

plt.tight_layout(pad=0.1, h_pad=0.1, w_pad=0.8)
plt.subplots_adjust(top=0.98, bottom=0.3, right=0.98, left=0.1)
# fig.savefig(path_save.joinpath('lv_convergence.png'), dpi=300)
plt.show()
