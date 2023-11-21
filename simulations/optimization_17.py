from pathlib import Path
import numpy as np

from fibrosisoptimization.core.fibrosis_generator import FibrosisGenerator
from fibrosisoptimization.measure.residuals import Residuals
from fibrosisoptimization.measure.fibrosis_density import FibrosisDensity
from fibrosisoptimization.minimizators import (
    MinimizatorsCollection
)


def sort_distant_segments(lats):
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


path = Path('./data')
path_step = path.joinpath('17')

max_iter = 18
start_iter = 4
segments_list = [1]

residuals = Residuals(path_step, 'epi', 13, fs=1 / (40 * 0.0015))
segments = np.load(path_step.joinpath('segments.npy'))

residuals.update_base('1')
residuals.update_target('0')

data = residuals.update('4')

lats_mean = - data.lat_mean_per_segment
distant_segments = sort_distant_segments(lats_mean)

print(distant_segments)

full_segments_list = np.concatenate(distant_segments)

print(full_segments_list)

for segments_list in distant_segments:

    minimizators = MinimizatorsCollection(segments_list,
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

        mesh = np.load(path_step.joinpath(subdir, 'tissue.npy'))

        densities = FibrosisDensity.compute_density(mesh, segments)

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
