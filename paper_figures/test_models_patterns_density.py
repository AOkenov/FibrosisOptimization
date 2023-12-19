from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.ticker as mtick
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable

from fibrosisoptimization.measure.data_loader import DataLoader
from fibrosisoptimization.measure.fibrosis_measurer import FibrosisMeasurer

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

font_properties = {'family': 'serif',
                   'color':  'black',
                   'weight': 'normal',
                   'size': 12}


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


def select_frame(mesh):
    z_ind = int(np.argwhere(mesh > 0)[:, 2].mean())
    image = mesh[:, :, z_ind]
    x_min = int(np.min(np.argwhere(image > 0)[:, 0]))
    x_max = int(np.max(np.argwhere(image > 0)[:, 0]))
    y_min = int(np.min(np.argwhere(image > 0)[:, 1]))
    y_max = int(np.max(np.argwhere(image > 0)[:, 1]))
    image = image[x_min-5: x_max+5, y_min-5: y_max+5]
    return image


path = Path(__file__).parent.parent.joinpath('data')
path_save = path.joinpath('figures')
data_path = path.joinpath('models', 'test_models')
segments_path = path.joinpath('models', 'left_ventricle', '17')
layers_path = path.joinpath('models')

models = ['transmural', 'sub-endo', 'mid-wall', 'sub-epi']
labels = ['(a)', '(b)', '(c)', 'd']
subdirs = ['4', '12', '13', '9']

data_loader = DataLoader(segments_path=segments_path,
                         layers_path=layers_path)

segments = data_loader.load_segments()
layered_segments = data_loader.load_layered_segments()

fig, axs = plt.subplots(ncols=5, nrows=2, sharey=True, figsize=(6, 4),
                        gridspec_kw={'width_ratios': [15, 100, 100, 100, 100]})

for i, (label, model, subdir) in enumerate(zip(labels, models, subdirs)):
    for j, subdir_ in enumerate(['0', subdir]):
        data_loader.data_path = path.joinpath(data_path, model)
        mesh = data_loader.load_mesh(subdir_)
        density_map = FibrosisMeasurer.compute_density_map(mesh,
                                                           layered_segments)
        density_map *= 100
        density_map[segments != 12] = 0
        image = select_frame(density_map)
        plot_map(axs[j, i+1], image, vmin=0, vmax=50)

    axs[1, i+1].text(0.5, -0.1, label, transform=axs[1, i+1].transAxes,
                     ha='center', va='center', fontdict=font_properties)

for i, label in enumerate(['Target', 'Reconstructed']):
    axs[i, 0].axis('off')
    axs[i, 0].text(0.5, 63, label, rotation='vertical', ha='center',
                   va='center', fontdict=font_properties)

plt.tight_layout(pad=0.1, h_pad=0., w_pad=0)
# fig.savefig(path_save.joinpath('patterns_density.png'), dpi=300)
plt.show()
