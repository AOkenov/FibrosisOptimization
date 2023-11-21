from pathlib import Path
import numpy as np

from fibrosisoptimization.measure.residuals import Residuals
from fibrosisoptimization.plotter.interactive_plotter import InteractivePlotter


path = Path('./data')
path_step = path.joinpath('17')

subdir = '1'

surface_residuals = Residuals(path_step, 'epi', 13, fs=1 / (40 * 0.0015))
surface_residuals.update_base('1')
surface_residuals.update_target('0')
surface_data = surface_residuals.update(subdir)

# scalar_lim = [np.min(surface_data.lat), np.max(surface_data.lat)]
scalar_lim = [0, 18]

segments = np.load(path_step.joinpath('segments.npy'))

coords = np.vstack((np.argwhere(segments > 0), surface_data.coords))

print(coords.shape)
segments = np.concatenate((segments[segments > 0], surface_data.segments))
print(segments.shape)

plotter = InteractivePlotter()
plotter.build_grid(coords)
plotter.add_scalar(segments.astype(np.float32))
plotter.add_grid(clim=scalar_lim)
# plotter.update()
plotter.show()
