from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib as mpl

from fibrosisoptimization.measure.data_loader import DataLoader


mpl.rcParams['axes.linewidth'] = 0.5
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['xtick.minor.width'] = 0.5
mpl.rcParams['ytick.major.width'] = 0.5
mpl.rcParams['ytick.minor.width'] = 0.5
mpl.rcParams['axes.titlesize'] = 'medium'
mpl.rcParams['xtick.minor.size'] = 1
mpl.rcParams['ytick.minor.size'] = 1


cmap = colors.LinearSegmentedColormap.from_list('fibrosis',
                                                [(0., '#e2a858'),
                                                 (1, '#990102')])

font_properties = {'family': 'serif',
                   'color':  'black',
                   'weight': 'normal',
                   'size': 12}


def plot_image(ax, image):
    image = np.ma.masked_where(image == 0, image)
    ax.imshow(image, origin='lower', cmap=cmap)
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


path = Path('/Users/arstanbek/Projects/FibrosisOptimization/data')
path_save = path.joinpath('figures')
data_path = path.joinpath('models', 'test_models')
models = ['transmural', 'sub-endo', 'mid-wall', 'sub-epi']
labels = ['(a)', '(b)', '(c)', 'd']
subdirs = ['4', '12', '13', '9']

data_loader = DataLoader(segments_path=path.joinpath('models',
                                                     'left_ventricle', '17'))

segments = data_loader.load_segments()

fig, axs = plt.subplots(ncols=4, nrows=1, sharey=True, figsize=(6, 2.7),
                        gridspec_kw={'width_ratios': [100, 100, 100, 100]})

for i, (label, model, subdir) in enumerate(zip(labels, models, subdirs)):
    data_loader.data_path = path.joinpath(data_path, model)
    mesh = data_loader.load_mesh(subdir)
    mesh[segments != 12] = 0

    image = select_frame(mesh)
    plot_image(axs[i], image)

    axs[i].text(0.5, -0.1, label, transform=axs[i].transAxes,
                ha='center', va='center', fontdict=font_properties)

plt.tight_layout(pad=0.1, h_pad=0.1, w_pad=0)
# fig.savefig(path_save.joinpath('patterns_fibrosis.png'), dpi=300)
plt.show()
