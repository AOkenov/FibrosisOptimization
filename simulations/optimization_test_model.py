from pathlib import Path
import numpy as np

from fibrosisoptimization.core.fibrosis_generator import FibrosisGenerator
from fibrosisoptimization.measure import (
    DataLoader,
    Residuals,
    FibrosisMeasurer
)

from fibrosisoptimization.minimizators import (
    ParallelMinimizators,
    SequentialMinimizators
)

from run_simulation import run_simulation

path = Path('./data/models')
model_dir = 'test_models'
model_subdir = 'sub-epi'

data_path = path.joinpath(model_dir, model_subdir)
segments_path = path.joinpath('left_ventricle', '17')
electrodes_path = path.joinpath('left_ventricle', '17')

surface_name = 'epi'
segment_target = 12
number_of_segments = 17
segments_list = [segment_target]
lat_reference = {'endo': 0, 'epi': 13}
fs = 1 / (40 * 0.0015)

subdir = '1'
max_iter = 20

data_loaders = {}
residuals = {}

for surface_name in ['endo', 'epi']:
    data_loaders[surface_name] = DataLoader(surface_name=surface_name,
                                            data_path=data_path,
                                            electrodes_path=electrodes_path,
                                            segments_path=segments_path,
                                            layers_path=path,
                                            stimul_path=path,
                                            fibers_path=path)

    residuals[surface_name] = Residuals(data_loaders[surface_name],
                                        lat_reference[surface_name],
                                        fs, interpolate=True)
    residuals[surface_name].update_base('1')
    residuals[surface_name].update_target('0')


# LAT MINIMIZATION ON SEGMENT 12
minimizators = ParallelMinimizators(segments_list, ['LAT'])
segments = data_loaders['epi'].load_segments()
generator = FibrosisGenerator(segments)

for i in range(1, max_iter):
    print('--------------------------------------------')
    print('ITERATION: {}'.format(i))
    subdir = '{}'.format(i)
    data = residuals['epi'].update(subdir)

    mesh = data_loaders['epi'].load_mesh(subdir)
    densities = FibrosisMeasurer.compute_density(mesh, segments)

    densities_next = minimizators.update(densities, data)

    if np.all(np.abs(densities_next - densities) < 0.01):
        print('CONVERGENCE ACHIVED')
        last_iter = i
        break

    mesh = generator.update(mesh, densities_next, segments)

    subdir = '{}'.format(i + 1)
    path_next = data_loaders['epi'].data_path.joinpath(subdir)
    path_next.mkdir(parents=True, exist_ok=True)
    # np.save(path_next.joinpath('tissue.npy'), mesh.astype(np.uint8))
    run_simulation(data_loaders, subdir, t_max=10, prog_bar=True)

print('============================================')
print('LOCAL OPTIMIZATION')
print('============================================')
segments_list = [segment_target,                           # ENDO
                 2 * number_of_segments + segment_target,  # EPI
                 number_of_segments + segment_target]      # MID
layered_segments = data_loaders['epi'].load_layered_segments()
minimizators = SequentialMinimizators(segments_list, number_of_segments)
generator = FibrosisGenerator(layered_segments)

for i in range(last_iter, max_iter):
    print('--------------------------------------------')
    print('ITERATION: {}'.format(i))
    subdir = '{}'.format(i)
    data = {}
    data['endo'] = residuals['endo'].update(subdir)
    data['epi'] = residuals['epi'].update(subdir)

    mesh = data_loaders['epi'].load_mesh(subdir)
    densities = FibrosisMeasurer.compute_density(mesh, layered_segments)

    print(densities[minimizators.segments - 1])

    densities_next = minimizators.update(densities, data)

    if np.all(np.abs(densities_next - densities) < 0.01):
        print('CONVERGENCE ACHIVED')
        last_iter = i
        break

    mesh = generator.update(mesh, densities_next, layered_segments)

    subdir = '{}'.format(i + 1)
    path_next = data_loaders['epi'].data_path.joinpath(subdir)
    path_next.mkdir(parents=True, exist_ok=True)
    # np.save(path_next.joinpath('tissue.npy'), mesh.astype(np.uint8))
    run_simulation(data_loaders, subdir, t_max=10, prog_bar=True)
