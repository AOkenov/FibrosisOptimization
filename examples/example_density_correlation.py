from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from fibrosisoptimization.measure.fibrosis_density import FibrosisDensity


path = Path('./data')
path_step = path.joinpath('17')

subdir_x = '0'
subdir_y = '7'

segments = np.load(path_step.joinpath('segments.npy'))

densities = {}

for subdir in [subdir_x, subdir_y]:
    mesh = np.load(path_step.joinpath(subdir, 'tissue.npy'))
    densities[subdir] = FibrosisDensity.compute_density(mesh, segments)

x = densities[subdir_x]
y = densities[subdir_y]

labels = np.unique(segments[segments > 0])

t = np.linspace(0, 0.3, 100)

plt.figure()
plt.scatter(x, y, c=labels)
plt.plot(t, t)

for label, x_, y_ in zip(labels, x, y):
    plt.annotate(str(label), xy=(x_, y_), xytext=(-20, 20),
                 textcoords='offset points', ha='right', va='bottom',
                 bbox=dict(boxstyle='round, pad=0.5', fc='yellow', alpha=0.5),
                 arrowprops=dict(arrowstyle='->',
                                 connectionstyle='arc3, rad=0'))
plt.show()

# # scalar_lim = [np.min(surface_data.lat), np.max(surface_data.lat)]
# scalar_lim = [-0.1, 0.35]

# plotter = InteractivePlotter()
# plotter.build_grid(surface_data.coords)
# plotter.add_scalar(surface_data.lat)
# plotter.add_grid(clim=scalar_lim)
# plotter.add_points(electrode_data.coords.astype(np.float32),
#                    render_points_as_spheres=True, point_size=20.0,
#                    scalars=electrode_data.lat, clim=scalar_lim)
# # plotter.update()
# plotter.show()
