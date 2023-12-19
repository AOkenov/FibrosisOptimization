from pathlib import Path
import numpy as np

from fibrosisoptimization.measure.residuals import Residuals
from fibrosisoptimization.measure.data_loader import DataLoader
from fibrosisoptimization.plotter.interactive_plotter import InteractivePlotter


path = Path(__file__).parent.parent.joinpath('data')
data_path = path.joinpath('models', 'left_ventricle', 'LV')

subdir = '1'
lat_reference = 13
fs = 1 / (40 * 0.0015)

data_loader = DataLoader(surface_name='epi', 
                         electrodes_path=data_path,
                         data_path=data_path, 
                         segments_path=data_path)

surface_residuals = Residuals(data_loader, lat_reference, fs, interpolate=True)
surface_residuals.update_base('1')
surface_residuals.update_target('0')
surface_data = surface_residuals.update(subdir)

electrode_residuals = Residuals(data_loader, lat_reference, fs, 
                                interpolate=False)
electrode_residuals.update_base('1')
electrode_residuals.update_target('0')
electrode_data = electrode_residuals.update(subdir)

print(electrode_data.lat_mean_per_segment, surface_data.lat_mean_per_segment)

# scalar_lim = [np.min(surface_data.lat), np.max(surface_data.lat)]
scalar_lim = [-0.1, 0.35]

plotter = InteractivePlotter()
plotter.build_grid(surface_data.coords)
plotter.add_scalar(surface_data.lat)
plotter.add_grid(clim=scalar_lim)
plotter.add_points(electrode_data.coords.astype(np.float32),
                   render_points_as_spheres=True, point_size=20.0,
                   scalars=electrode_data.lat, clim=scalar_lim)
# plotter.update()
plotter.show()
