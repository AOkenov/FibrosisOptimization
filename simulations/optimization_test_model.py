from pathlib import Path
import numpy as np

from fibrosisoptimization.core.fibrosis_generator import FibrosisGenerator
from fibrosisoptimization.measure import (
    DataLoader,
    Residuals,
    DensityMeasurer
)

from fibrosisoptimization.minimizators import (
    MinimizatorsCollection,
    LocalMinimizatorsCollection
)


path = Path('./data/models')
model_dir = 'test_models'
model_subdir = 'sub-epi'

data_path = path.joinpath(model_dir, model_subdir)
segments_path = path.joinpath(model_dir)

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
                                            electrodes_path=path,
                                            segments_path=segments_path,
                                            layers_path=path)

    residuals[surface_name] = Residuals(data_loaders[surface_name],
                                        lat_reference[surface_name],
                                        fs, interpolate=True)
    residuals[surface_name].update_base('1')
    residuals[surface_name].update_target('0')


# LAT MINIMIZATION ON SEGMENT 12
minimizators = MinimizatorsCollection(segments_list, ['LAT'])
segments = data_loaders['epi'].load_segments()
generator = FibrosisGenerator(segments)

for i in range(1, max_iter):
    print('--------------------------------------------')
    print('ITERATION: {}'.format(i))
    subdir = '{}'.format(i)
    data = residuals['epi'].update(subdir)

    mesh = data_loaders['epi'].load_mesh(subdir)
    densities = DensityMeasurer.compute_density(mesh, segments)

    densities_next = minimizators.update(densities, data)

    if np.all(np.abs(densities_next - densities) < 0.01):
        print('CONVERGENCE ACHIVED')
        last_iter = i
        break

    mesh = generator.update(mesh, densities_next, segments)

    # subdir = '{}'.format(i + 1)
    # path_next = path_step.joinpath(subdir)
    # path_next.mkdir(parents=True, exist_ok=True)
    # np.save(path_next.joinpath('tissue.npy'), mesh.astype(np.uint8))
    # run_simulation(path, path_step, subdir)

print('============================================')
print('LOCAL OPTIMIZATION')
print('============================================')

segments_list = [12, 2 * number_of_segments + 12, number_of_segments + 12]
layered_segments = data_loaders['epi'].load_layered_segments()
minimizators = LocalMinimizatorsCollection(segments_list, 17)
generator = FibrosisGenerator(layered_segments)

for i in range(last_iter, max_iter):
    print('--------------------------------------------')
    print('ITERATION: {}'.format(i))
    subdir = '{}'.format(i)
    data_endo = residuals['endo'].update(subdir)
    data_epi = residuals['epi'].update(subdir)

    mesh = data_loaders['epi'].load_mesh(subdir)
    densities = DensityMeasurer.compute_density(mesh, layered_segments)

    print(densities[minimizators.segments - 1])

    densities_next = minimizators.update(densities, data_endo, data_epi)

    if np.all(np.abs(densities_next - densities) < 0.01):
        print('CONVERGENCE ACHIVED')
        last_iter = i
        break

    mesh = generator.update(mesh, densities_next, layered_segments)

    # subdir = '{}'.format(i + 1)
    # path_next = path_step.joinpath(subdir)
    # path_next.mkdir(parents=True, exist_ok=True)
    # np.save(path_next.joinpath('tissue.npy'), mesh.astype(np.uint8))
    # run_simulation(path, path_step, subdir)
