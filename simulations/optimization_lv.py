from pathlib import Path
import numpy as np

from fibrosisoptimization.core.fibrosis_generator import FibrosisGenerator
from fibrosisoptimization.measure import (
    Residuals,
    DataLoader,
    FibrosisMeasurer
)
from fibrosisoptimization.minimizators import (
    ParallelMinimizators
)

from simulations import run_simulation


path = Path('./data/models')
model_dir = 'left_ventricle'
model_subdir = 'LV'
data_path = path.joinpath(model_dir, model_subdir)

surface_name = 'epi'
lat_reference = 13
fs = 1 / (40 * 0.0015)
max_iter = 10
segments_list = [1]

data_loader = DataLoader(surface_name=surface_name,
                         data_path=data_path,
                         electrodes_path=data_path,
                         segments_path=data_path,
                         layers_path=path,
                         stimul_path=path,
                         fibers_path=path)

residuals = Residuals(data_loader, lat_reference, fs, interpolate=True)
residuals.update_base('1')
residuals.update_target('0')

minimizators = ParallelMinimizators(segments_list, ['LAT'])

segments = data_loader.load_segments()
generator = FibrosisGenerator(segments)

for i in range(1, max_iter):
    print('--------------------------------------------')
    print('ITERATION: {}'.format(i))
    subdir = '{}'.format(i)
    data = residuals.update(subdir)

    mesh = data_loader.load_mesh(subdir)
    densities = FibrosisMeasurer.compute_density(mesh, segments)

    densities_next = minimizators.update(densities, data)

    if np.all(np.abs(densities_next - densities) < 0.01):
        print('CONVERGENCE ACHIVED')
        break

    mesh = generator.update(mesh, densities_next, segments)

    data_loaders = {'epi': data_loader}
    subdir = '{}'.format(i + 1)
    path_next = data_loaders['epi'].data_path.joinpath(subdir)
    path_next.mkdir(parents=True, exist_ok=True)
    # np.save(path_next.joinpath('tissue.npy'), mesh.astype(np.uint8))
    run_simulation(data_loaders, subdir, t_max=10, prog_bar=True)
