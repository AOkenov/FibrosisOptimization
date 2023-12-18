from pathlib import Path
import numpy as np

from fibrosisoptimization.plotter.interactive_plotter import InteractivePlotter
from fibrosisoptimization.measure.data_loader import DataLoader


path = Path('/Users/arstanbek/Projects/FibrosisOptimization/data/models')

model_dir = '68'

layers_path = path
segments_path = path.joinpath('left_ventricle', model_dir)
electrodes_path = path.joinpath('left_ventricle', model_dir)
data_path = path.joinpath('left_ventricle', model_dir)

data_loader = DataLoader(surface_name='endo',
                         data_path=data_path,
                         electrodes_path=electrodes_path,
                         segments_path=segments_path,
                         layers_path=layers_path)

surface_coords, surface_labels = data_loader.load_surface()
electrodes_coords, electrodes_labels = data_loader.load_electrodes()
segments = data_loader.load_segments()

coords = np.vstack((np.argwhere(segments > 0), surface_coords))

print(coords.shape)
segments = np.concatenate((segments[segments > 0], surface_labels))
print(segments.shape)
scalar_lim = (0, 68)

plotter = InteractivePlotter()
plotter.build_grid(coords)
plotter.add_scalar(segments.astype(np.float32))
plotter.add_grid(clim=scalar_lim)
plotter.add_sphere_points(electrodes_coords, electrodes_labels)
# plotter.update()
plotter.show()
