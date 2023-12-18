from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from fibrosisoptimization.measure.data_loader import DataLoader
from fibrosisoptimization.measure.residuals import Residuals
from fibrosisoptimization.measure.fibrosis_measurer import FibrosisMeasurer
from fibrosisoptimization.plotter.interactive_plotter import InteractivePlotter


mpl.rcParams['axes.linewidth'] = 0.5
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['xtick.minor.width'] = 0.5
mpl.rcParams['ytick.major.width'] = 0.5
mpl.rcParams['ytick.minor.width'] = 0.5
mpl.rcParams['axes.titlesize'] = 'medium'
mpl.rcParams['xtick.minor.size'] = 1
mpl.rcParams['ytick.minor.size'] = 1

path = Path('/Users/arstanbek/Projects/FibrosisOptimization/data/models')

model_dir = '68'

layers_path = path
segments_path = path.joinpath('left_ventricle', model_dir)
electrodes_path = path.joinpath('left_ventricle', model_dir)
data_path = path.joinpath('left_ventricle', model_dir)

data_loader = {}
for surface_name in ['epi', 'endo']:
    data_loader[surface_name] = DataLoader(surface_name=surface_name,
                                           data_path=data_path,
                                           electrodes_path=electrodes_path,
                                           segments_path=segments_path,
                                           layers_path=layers_path)

els_coords = {}
els_labels = {}
egms = {}
egms_1 = {}

mesh = data_loader['epi'].load_mesh('0')
segments = data_loader['epi'].load_segments()
layered_segments = data_loader['epi'].load_layered_segments(68)

density = FibrosisMeasurer.compute_density(mesh, layered_segments)
density_map = FibrosisMeasurer.compute_density_map(mesh, layered_segments)

segments_list = np.argsort(density) % 68
layers_list = np.argsort(density) // 68

for i in range(68):
    print("{}: {:.2f}, {:.2f}, {:.2f}".format(i + 1, density[i],
                                              density[i + 68],
                                              density[i + 68 * 2]))

labels_list = [12, 44, 33, 9, 7]

fig, axs = plt.subplots(ncols=len(labels_list) + 1, nrows=2,
                        figsize=(9.5, 5.5),
                        gridspec_kw={'width_ratios': [15, 100, 100, 100, 100,
                                                      100]})

lines = []
for i, surface_name in enumerate(['endo', 'epi']):

    els_coords, els_labels = data_loader[surface_name].load_electrodes()
    egms = data_loader[surface_name].load_egms('0')
    egms_1 = data_loader[surface_name].load_egms('1')
    egms_202 = data_loader[surface_name].load_egms('202')

    residuals = Residuals(data_loader[surface_name], 0, fs=1,
                          interpolate=False)
    residuals.update_target('0')
    residuals.update_base('1')
    els_data = residuals.update('1')

    # print(np.argsort(np.abs(els_data.ptp)))

    for j, label in enumerate(labels_list):
        els_mask = np.isin(els_labels, [label])

        ind = np.argmax(np.abs(els_data.ptp[els_mask]))

        density_endo = 100 * density[label-1]
        density_mid = 100 * density[label - 1 + 68]
        density_epi = 100 * density[label - 1 + 68 * 2]

        if i == 1:
            axs[i, j+1].set_title('D = ({}%, {}%, {}%)'.format(int(density_endo),
                                                               int(density_mid),
                                                               int(density_epi)))

        els_ind = np.where(els_mask)[0]

        els_ind = els_ind[ind]
        # els_ind = [340]
        # print(els_labels[els_ind])

        if i == 1 and j == 0:
            lines.append(axs[i, j+1].plot(egms[els_ind].T, ls='-', label='Target')[0])
            lines.append(axs[i, j+1].plot(egms_1[els_ind].T, ls=':', label='Base')[0])
            lines.append(axs[i, j+1].plot(egms_202[els_ind].T, ls='--', label='Optimized')[0])
        else:
            axs[i, j+1].plot(egms[els_ind].T, ls='-')
            axs[i, j+1].plot(egms_1[els_ind].T, ls=':')
            axs[i, j+1].plot(egms_202[els_ind].T, ls='--')

        if surface_name == 'epi':
            axs[i, j+1].set_ylim([-0.05, 0.25])
        else:
            axs[i, j+1].set_ylim([-0.25, 0.05])

        axs[i, j+1].set_xlim([0, 150])
        axs[i, j+1].axis('off')

left, width = .1, .8
bottom, height = .1, .8
right = left + width
top = bottom + height
font_properties = {'family': 'serif',
                   'color': 'black',
                   'weight': 'normal',
                   'size': 12}

for i, label in enumerate(['Endo', 'Epi']):
    axs[i, 0].axis('off')
    axs[i, 0].text(0.5 * (left + right),
                   0.5 * (bottom + top),
                   label,
                   rotation='vertical',
                   ha='center',
                   va='center',
                   fontdict=font_properties)
legend = fig.legend(title='EGMs',
                    handles=lines, loc='lower center', 
                    bbox_to_anchor=(0.5, 0.8), ncol=4, fontsize=9)
plt.tight_layout(pad=0.1, h_pad=.1, w_pad=1.)
plt.subplots_adjust(top=0.8, bottom=0.05, right=0.98, left=0.05)
plt.show()

# fig.savefig('/Users/arstanbek/Projects/FibrosisOptimization/data/figures/egms.png', dpi=300)


# plotter = InteractivePlotter()
# plotter.build_grid(np.argwhere(mesh > 0))
# plotter.add_scalar(density_map[mesh > 0].astype(np.float32))
# plotter.add_grid(clim=[0, 0.4])
# # plotter.add_scalar(segments[mesh > 0].astype(np.float32))
# # plotter.add_grid(clim=[0, 68])
# plotter.add_sphere_points(els_coords[np.isin(els_labels, labels_list)],
#                           els_labels[np.isin(els_labels, labels_list)])
# # plotter.update()
# plotter.show()
