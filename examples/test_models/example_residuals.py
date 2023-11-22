from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from fibrosisoptimization.measure import (
    Residuals,
    DataLoader,
)
from fibrosisoptimization.plotter.interactive_plotter import InteractivePlotter


path = Path('./data/models')
model_dir = 'test_models'
model_subdir = 'mid-wall'

data_path = path.joinpath(model_dir, model_subdir)
segments_path = path.joinpath(model_dir)

surface_name = 'epi'
lat_reference = 13
fs = 1 / (40 * 0.0015)

subdir = '1'

data_loader = DataLoader(surface_name=surface_name,
                         data_path=data_path,
                         electrodes_path=path,
                         segments_path=segments_path,
                         layers_path=path)


surface_residuals = Residuals(data_loader, lat_reference, fs, interpolate=True)
surface_residuals.update_base('1')
surface_residuals.update_target('0')
surface_data = surface_residuals.update(subdir)

electrode_residuals = Residuals(data_loader, lat_reference, fs,
                                interpolate=False)
electrode_residuals.update_base('1')
electrode_residuals.update_target('0')
electrode_data = electrode_residuals.update(subdir)

err_lim = [0, 0.2]
surf_err = np.abs(surface_data.lat)
els_err = np.abs(electrode_data.lat)

plotter = InteractivePlotter()
plotter.build_grid(surface_data.coords)
plotter.add_scalar(surf_err)
plotter.add_grid(clim=err_lim)
plotter.add_points(electrode_data.coords.astype(np.float32),
                   render_points_as_spheres=True, point_size=20.0,
                   scalars=els_err, clim=err_lim)
# plotter.update()
plotter.show()
