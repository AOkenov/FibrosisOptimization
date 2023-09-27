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

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)  
    cax.axis('off')

    ax.set_xticks([])
    ax.set_yticks([])


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

modes = np.load(path.joinpath('modes.npy'))
labels = np.load(path.joinpath('labels.npy'))

segments = (modes - 1) * 68 + labels
segments[modes == 0] = 0
segments = segments.astype(int)

experiment = 'rotor/meshes'
subdirs = ['initial', 'endo']
z_inds = [50, 90, 150, 200]

fig, axs = plt.subplots(ncols=5, nrows=3,
                        figsize=(8.5, 4.5), 
                        gridspec_kw={'width_ratios': [15, 100, 100, 100, 100]})

for i, z_ind in enumerate(z_inds):
    mesh = np.load(path.joinpath(experiment, 'initial', 'tissue.npy'))
    image = mesh[:, :, z_ind]
    plot_image(axs[0, i+1], image)

for j, subdir in enumerate(subdirs):
    mesh = np.load(path.joinpath(experiment, subdir, 'tissue.npy'))
    density_map = 100 * FibrosisDensity.compute_density(mesh, segments, as_map=True)

    for i, z_ind in enumerate(z_inds):
        image = density_map[:, :, z_ind]
        plot_map(axs[j+1, i+1], image, vmin=0, vmax=50)

left, width = .1, .8
bottom, height = .1, .8
right = left + width
top = bottom + height

for i, label in enumerate(['Fibrosis', 'Target', 'Reconstructed']):
    axs[i, 0].axis('off')
    axs[i, 0].text(0.5 * (left + right), 
                   0.5 * (bottom + top),
                   label, 
                   rotation='vertical',
                   ha='center',
                   va='center',
                   fontdict=font_properties)
plt.tight_layout(pad=0.1, h_pad=0.5, w_pad=0.1)
fig.savefig(path_save.joinpath('slices.png'), dpi=300)
plt.show()