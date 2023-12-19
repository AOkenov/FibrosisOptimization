from pathlib import Path
import numpy as np

from fibrosisoptimization.core.fibrosis_generator import FibrosisGenerator
from fibrosisoptimization.measure import (
    Residuals,
    DataLoader,
    FibrosisMeasurer
)
from fibrosisoptimization.minimizators import (
    CollectionRunner,
    SequentialMinimizators
)


def make_local_minimizators(segment_list, number_of_segments):
    local_minimizators = []
    for segment in segment_list:
        segments = [0 * number_of_segments + segment,  # ENDO
                    2 * number_of_segments + segment,  # EPI
                    1 * number_of_segments + segment]  # MID
        local_minimizator = SequentialMinimizators(segments,
                                                   number_of_segments)
        local_minimizators.append(local_minimizator)

    return local_minimizators


distant_segments = [[1, 3, 5, 14, 16],
                    [2, 4, 6, 13, 15],
                    [7, 9, 11],
                    [8, 10, 12, 17]]


path = Path(__file__).parent.parent.joinpath('data')
path = path.joinpath('models')
model_dir = 'left_ventricle'
model_subdir = '68'
data_path = path.joinpath(model_dir, model_subdir)

number_of_segments = 68
surface_name = 'epi'
lat_reference = 13
fs = 1 / (40 * 0.0015)

max_iter = 18
last_iter = 4

data_loaders = {}
residuals = {}

for surface_name in ['endo', 'epi']:
    data_loader = DataLoader(surface_name=surface_name,
                             data_path=data_path,
                             electrodes_path=data_path,
                             segments_path=data_path,
                             layers_path=path)
    data_loaders[surface_name] = data_loader

    residuals_ = Residuals(data_loader, lat_reference, fs, interpolate=True)
    residuals_.update_base('1')
    residuals_.update_target('0')

    residuals[surface_name] = residuals_

segments = data_loaders['epi'].load_segments()
layered_segments = data_loaders['epi'].load_layered_segments()

for segment_list in distant_segments:

    for subsegment in range(1, 5):
        subsegment_list = 4 * (np.array(segment_list) - 1) + subsegment

        minimizators = CollectionRunner()
        minimizators.minimizators = make_local_minimizators(subsegment_list,
                                                            number_of_segments)

        generator = FibrosisGenerator(layered_segments)

        for i in range(last_iter, max_iter):
            print('--------------------------------------------')
            print('ITERATION: {}'.format(i))
            subdir = '{}'.format(i)
            data = {}
            data['endo'] = residuals['endo'].update(subdir)
            data['epi'] = residuals['epi'].update(subdir)

            mesh = data_loaders['epi'].load_mesh(subdir)
            densities = FibrosisMeasurer.compute_density(mesh,
                                                         layered_segments)

            densities_next = minimizators.update(densities, data)

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
