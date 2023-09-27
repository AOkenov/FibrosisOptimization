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



def plot_map(ax, image, vmin=0, vmax=50, cmap='YlOrBr'):
    image = np.ma.masked_where(image == 0, image)

    im = ax.imshow(image, origin='lower', cmap=cmap, vmin=vmin, vmax=vmax)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)    
    plt.colorbar(im, cax=cax)
    cax.yaxis.set_major_formatter(mtick.PercentFormatter())
    cax.tick_params(labelsize=9)

    ax.set_xticks([])
    ax.set_yticks([])

path_save = Path('/Users/arstanbek/Projects/fibrosis-workspace/fibrosisoptimization/data/figures')
path = Path('/Users/arstanbek/Thor/projects/fibrosisoptimization/data')
experiments = ['transmural', 'sub-endo', 'mid-wall', 'sub-epi']
patterns_label = ['(a)', '(b)', '(c)', '(d)']
subdirs = ['4', '12', '13', '9']

active_segments = [29, 30, 41, 42]

modes = np.load(path.joinpath('transmural', 'modes.npy'))
labels = np.load(path.joinpath('transmural', 'labels.npy'))

segments = np.zeros_like(labels, dtype=int)

segments[np.isin(labels, active_segments)] = 1
segments *= modes

fig, axs = plt.subplots(ncols=5, nrows=2, sharey=True, figsize=(6, 4), 
                        gridspec_kw={'width_ratios': [15, 100, 100, 100, 100]})

for i, (label, experiment, subdir) in enumerate(zip(patterns_label, experiments, subdirs)):
        print(experiment)
        for j, subdir_ in enumerate(['0', subdir]):
            mesh = np.load(path.joinpath(experiment, subdir_, 'tissue.npy'))
            print('{}: {}'.format(subdir_, FibrosisDensity.compute_density(mesh, segments)))
            density_map = 100 * FibrosisDensity.compute_density(mesh, segments, as_map=True)
            image = density_map[55: 182, 90: 148, 100]
            plot_map(axs[j, i+1], image, vmin=0, vmax=50)

        axs[1, i+1].text(0.5, -0.1, label, transform=axs[1, i+1].transAxes,
                         ha='center', va='center', fontdict=font_properties)


for i, label in enumerate(['Target', 'Reconstructed']):
    axs[i, 0].axis('off')
    axs[i, 0].text(0.5, 63, label, rotation='vertical', ha='center', va='center', fontdict=font_properties)
    
# for i, label in enumerate(['Transmural', 'Sub-endocardial', 'Mid-myocardial', 'Sub-epicardial']):
#      axs[0, i+1].set_title(label)
    
plt.tight_layout(pad=0.1, h_pad=0., w_pad=0)
fig.savefig(path_save.joinpath('patterns_density.png'), dpi=300)
plt.show()