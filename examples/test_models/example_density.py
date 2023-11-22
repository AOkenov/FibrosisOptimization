from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from fibrosisoptimization.measure import DataLoader, DensityMeasurer

path = Path('./data/models')
model_dir = 'test_models'
model_subdir = 'mid-wall'

subdir = '4'

segments_path = path.joinpath(model_dir)
data_path = path.joinpath(model_dir, model_subdir)

data_loader = DataLoader(data_path=data_path,
                         segments_path=segments_path,
                         layers_path=path)

layered_segments = data_loader.load_layered_segments()

densities = []

mesh = data_loader.load_mesh(subdir)
densities = DensityMeasurer.compute_density(mesh, layered_segments)

segments_list = [11, 17 + 11, 34 + 11]

print(segments_list)

print(densities[segments_list])

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
