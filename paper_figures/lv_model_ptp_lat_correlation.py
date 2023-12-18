from pathlib import Path
import copy
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib as mpl
from scipy import stats

from fibrosisoptimization.measure.data_loader import DataLoader
from fibrosisoptimization.measure.residuals import Residuals


mpl.rcParams['axes.linewidth'] = 0.5
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['xtick.minor.width'] = 0.5
mpl.rcParams['ytick.major.width'] = 0.5
mpl.rcParams['ytick.minor.width'] = 0.5
mpl.rcParams['axes.titlesize'] = 'medium'
mpl.rcParams['xtick.minor.size'] = 1
mpl.rcParams['ytick.minor.size'] = 1


font_properties = {'family': 'serif',
                   'color':  'black', 'weight': 'normal', 'size': 12}


def plot_regress(ax, x, y):
    res = stats.linregress(x, y)

    print('Intercept: {:2.3} Slope: {:2.3}'.format(res.intercept, res.slope))

    ax.plot(x, y, ls='', marker='o', ms=3)
    ax.plot(x, res.intercept + res.slope * x, 'r',
            label='R = {:2.2}'.format(res.rvalue))

#     for i, (x_, y_) in enumerate(zip(x, y)):
#         ax.annotate(str(i), (x_, y_))

    ax.legend(loc='upper left')


path = Path('/Users/arstanbek/Projects/FibrosisOptimization/data')
data_path = path.joinpath('models', 'left_ventricle', '68')
electrodes_path = path.joinpath('models', 'left_ventricle', '68')

lat_reference = 13
fs = 1 / (40 * 0.0015)

data_loader = DataLoader(electrodes_path=electrodes_path,
                         data_path=data_path)

fig, axs = plt.subplots(ncols=3, figsize=(8, 3))

for surface in ['endo', 'epi']:
    data_loader.surface_name = surface

    residuals = Residuals(data_loader, lat_reference, fs, interpolate=False)

    lat_array = []
    ptp_array = []
    for j in [0, 202]:
        subdir = '{}'.format(j)
        els_data = residuals.load_subdir_data(subdir)
        lat_array.append(copy.deepcopy(els_data.lat))
        ptp_array.append(copy.deepcopy(els_data.ptp))

    if 'endo' in surface:
        plot_regress(axs[0], *ptp_array)
        continue

    plot_regress(axs[1], *ptp_array)
    plot_regress(axs[2], *lat_array)

axs[0].set_xticks(np.arange(0.04, 0.33, 0.08))
axs[0].set_yticks(np.arange(0.04, 0.33, 0.08))

axs[1].set_xticks(np.arange(0.05, 0.21, 0.05))
axs[1].set_yticks(np.arange(0.05, 0.21, 0.05))

axs[2].set_xticks(np.arange(1, 8, 2))
axs[2].set_yticks(np.arange(1, 8, 2))

for ax in axs:
    ax.set_xlabel('Target')
    ax.set_ylabel('Algorithm result')


for i, label in enumerate(['(a)', '(b)', '(c)']):
    axs[i].text(0.5, -0.35, label, transform=axs[i].transAxes,
                ha='center', va='center', fontdict=font_properties)

plt.tight_layout(pad=0.1, h_pad=0.1, w_pad=0.8)
plt.subplots_adjust(top=0.98, bottom=0.3, right=0.98, left=0.1)
# fig.savefig(path_save.joinpath('lv_correlation.png'), dpi=300)
plt.show()
