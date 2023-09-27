from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.ticker as mtick
import matplotlib as mpl
from scipy import stats

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


def plot_regress(ax, x, y):
    res = stats.linregress(x, y)
    
    print('Intercept: {:2.3} Slope: {:2.3}'.format(res.intercept, res.slope))
    
    ax.plot(x, y, ls='', marker='o', ms=3)
    ax.plot(x, res.intercept + res.slope * x, 'r', 
             label='R = {:2.2}'.format(res.rvalue))
    
#     for i, (x_, y_) in enumerate(zip(x, y)):
#         ax.annotate(str(i), (x_, y_))
    
    ax.legend(loc='upper left')
    ax.set_xlabel('Target fibrosis')
    ax.set_ylabel('Algorithm result')
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ax.set_xlim([0, 40])
    ax.set_ylim([0, 40])


def load_and_plot(segments, path, experiment, ax_ind):
    mesh = np.load(path.joinpath(experiment, 'initial', 'tissue.npy'))
    target = 100 * FibrosisDensity.compute_density(mesh, segments)

    mesh = np.load(path.joinpath(experiment, 'endo', 'tissue.npy'))
    result = 100 * FibrosisDensity.compute_density(mesh, segments)

    plot_regress(axs[ax_ind], target, result)


path_save = Path('/Users/arstanbek/Projects/fibrosis-workspace/fibrosisoptimization/data/figures')
path = Path('/Users/arstanbek/Thor/projects/fibrosisoptimization/data')

subdirs = ['initial', 'endo']
experiment = 'rotor/meshes'

layers = np.load(path.joinpath('modes.npy'))
labels = np.load(path.joinpath('labels.npy')).astype(int)

titles = ['Sub-endocard segments ($N=68$)', 
          'Mid-myocard segments ($N=68$)', 
          'Sub-epicard segments ($N=68$)',
          'Total segments ($N=204$)',
          'Transmural segments ($N=68$)']

fig = plt.figure(figsize=(8.5, 6.))
axs = []
axs.append(plt.subplot2grid((4, 6), (0, 0), rowspan=2, colspan=2))
axs.append(plt.subplot2grid((4, 6), (0, 2), rowspan=2, colspan=2, sharex=axs[0], sharey=axs[0]))
axs.append(plt.subplot2grid((4, 6), (0, 4), rowspan=2, colspan=2, sharex=axs[0], sharey=axs[0]))

axs.append(plt.subplot2grid((4, 6), (2, 1), rowspan=2, colspan=2))
axs.append(plt.subplot2grid((4, 6), (2, 3), rowspan=2, colspan=2, sharex=axs[3], sharey=axs[3]))

# fig, axs = plt.subplots(ncols=3, figsize=(8, 2.7))


for layer in [1, 2, 3]:
    segments = labels.copy()
    segments[layers != layer] = 0 
    load_and_plot(segments, path, experiment, layer-1)

segments = (layers - 1) * 68 + labels
segments[layers == 0] = 0
load_and_plot(segments, path, experiment, 3)
load_and_plot(labels, path, experiment, 4)

# for ax, title in zip(axs, titles[:3]):
#     ax.set_title(title)

for i, (ax, label) in enumerate(zip(axs, ['(a)', '(b)', '(c)', '(d)', '(e)'])):
    axs[i].text(0.5, -0.3, label, transform=axs[i].transAxes,
                ha='center', va='center', fontdict=font_properties)
    axs[i].set_xticks(range(0, 41, 10))
    axs[i].set_yticks(range(0, 41, 10))

plt.tight_layout(pad=0.1)
plt.subplots_adjust(wspace=1, hspace=2)
plt.show()

fig.savefig(path_save.joinpath('lv_density_corr.png'), dpi=300)
