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


def sort_distant_segments(lats):
    """Sort group of segments based on mean error
    """
    distant_segments = [[1, 3, 5, 14, 16],
                        [2, 4, 6, 13, 15],
                        [7, 9, 11],
                        [8, 10, 12, 17]]
    out = []
    for s in distant_segments:
        out.append(np.mean(np.abs(lats[np.array(s) - 1])))

    res = []
    for i in np.argsort(-np.array(out)):
        res.append(np.array(distant_segments[i], dtype=int))

    return res


path = Path('./data/models')
model_dir = 'left_ventricle'
model_subdir = '17'
data_path = path.joinpath(model_dir, model_subdir)

surface_name = 'epi'
lat_reference = 13
fs = 1 / (40 * 0.0015)

max_iter = 18
start_iter = 4
segments_list = [1]

data_loader = DataLoader(surface_name=surface_name,
                         data_path=data_path,
                         electrodes_path=data_path,
                         segments_path=data_path,
                         layers_path=path)

residuals = Residuals(data_loader, lat_reference, fs, interpolate=True)
residuals.update_base('1')
residuals.update_target('0')

data = residuals.update('4')

lats_mean = - data.lat_mean_per_segment
distant_segments = sort_distant_segments(lats_mean)

full_segments_list = np.concatenate(distant_segments)

segments = data_loader.load_segments()

for segments_list in distant_segments:

    minimizators = ParallelMinimizators(segments_list,
                                        ['LAT'] * len(segments_list))

    generator = FibrosisGenerator(segments)

    print('============================================')
    print('SEGMENTS :', segments_list)
    print('============================================')

    for i in range(start_iter, max_iter):
        print('--------------------------------------------')
        print('ITERATION : {}'.format(i))
        print('--------------------------------------------')
        subdir = '{}'.format(i)
        data = residuals.update(subdir)

        mesh = data_loader.load_mesh(subdir)

        densities = FibrosisMeasurer.compute_density(mesh, segments)

        print(densities[full_segments_list - 1])

        densities_next = minimizators.update(densities, data)

        if np.all(np.abs(densities_next - densities) < 0.01):
            print('CONVERGENCE ACHIVED')
            start_iter = i
            break

        mesh = generator.update(mesh, densities_next, segments)

        # # subdir = '{}'.format(i + 1)
        # # path_next = path_step.joinpath(subdir)
        # # path_next.mkdir(parents=True, exist_ok=True)
        # # np.save(path_next.joinpath('tissue.npy'), mesh.astype(np.uint8))
        # # run_simulation(path, path_step, subdir)
