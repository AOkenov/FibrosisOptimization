from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.ticker as mtick
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable

from fibropt.measure.fibrosis_density import FibrosisDensity

mpl.rcParams['axes.linewidth'] = 0.5
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['xtick.minor.width'] = 0.5
mpl.rcParams['ytick.major.width'] = 0.5
mpl.rcParams['ytick.minor.width'] = 0.5
mpl.rcParams['axes.titlesize'] = 'medium'
mpl.rcParams['xtick.minor.size'] = 1
mpl.rcParams['ytick.minor.size'] = 1


cmap = colors.LinearSegmentedColormap.from_list(
    'fibrosis', [(0., '#e2a858'), (1, '#990102')])

font_properties = {'family': 'serif', 'color':  'black', 'weight': 'normal', 'size': 12}



def plot_image(ax, image):
    image = np.ma.masked_where(image == 0, image)
    ax.imshow(image, origin='lower', cmap=cmap)

    ax.set_xticks([])
    ax.set_yticks([])

path_save = Path('/Users/arstanbek/Projects/fibrosis-workspace/fibrosisoptimization/data/figures')
path = Path('/Users/arstanbek/Thor/projects/fibrosisoptimization/data')
experiments = ['transmural', 'sub-endo', 'mid-wall', 'sub-epi']
patterns_label = ['A', 'B', 'C', 'D']
subdirs = ['4', '12', '13', '9']

active_segments = [29, 30, 41, 42]

labels = np.load(path.joinpath('transmural', 'labels.npy'))

segments = np.zeros_like(labels, dtype=int)
segments[np.isin(labels, active_segments)] = 1

fig, axs = plt.subplots(ncols=4, nrows=1, sharey=True, figsize=(6, 2.7), 
                        gridspec_kw={'width_ratios': [100, 100, 100, 100]})

for i, (label, experiment, subdir) in enumerate(zip(patterns_label, experiments, subdirs)):
        mesh = np.load(path.joinpath(experiment, subdir, 'tissue.npy'))
        mesh[segments == 0] = 0
        image = mesh[55: 182, 90: 148, 100]
        plot_image(axs[i], image)

        axs[i].text(0.5, -0.1, label, transform=axs[i].transAxes,
                    ha='center', va='center', fontdict=font_properties)
    
plt.tight_layout(pad=0.1, h_pad=0.1, w_pad=0)
fig.savefig(path_save.joinpath('patterns_fibrosis.tiff'), dpi=300)
plt.show()