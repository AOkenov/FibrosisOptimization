from pathlib import Path
import numpy as np

from fibrosisoptimization.core.fibrosis_generator import FibrosisGenerator
from fibrosisoptimization.measure.residual import Residual
from fibrosisoptimization.measure.fibrosis_density import FibrosisDensity
from fibrosisoptimization.minimization.minimizator import Minimizator


distant_segments = [[1, 3, 5, 14, 16],
                    [2, 4, 6, 13, 15],
                    [7, 9, 11],
                    [8, 10, 12, 17]]


def sort_distant_segments(distant_segments, lats):
    out = []
    for s in distant_segments:
        out.append(np.mean(np.abs(lats[np.array(s) - 1])))

    res = []
    for i in np.argsort(-np.array(out)):
        res.append(np.array(distant_segments[i], dtype=int))

    return res


def update_densities(minimizators, densities, lats):
    out = []
    for minimizator, density, lat_mean in zip(minimizators, densities, lats_mean):
        out.append(minimizator.update(density, lat_mean))

    return np.array(out)


path = Path('./data')
path_step = path.joinpath('17')

max_iter = 100

residual = Residual(path_step, 'epi', 13, fs=1 / (40 * 0.0015))
segments = np.load(path.joinpath('segments_17.npy'))

residual.update_base('1')
residual.update_target('0')

minimizators = [Minimizator(i, 'LAT') for i in range(1, 18)]
generator = FibrosisGenerator(segments)

distant_segments_ind = 0

for i in range(4, 9):
    subdir = '{}'.format(i)
    data = residual.update(subdir)
    lats_mean = - data.lat_mean_per_segment

    if i == 4:
        distant_segments = sort_distant_segments(distant_segments, lats_mean)
        active_segments = distant_segments[0]
        print(i, 'Next segments', active_segments)

    mesh = np.load(path_step.joinpath(subdir, 'tissue.npy'))
    densities = FibrosisDensity.compute_density(mesh, segments)
    print(i, np.round(densities[active_segments - 1], decimals=3))

    densities_next = update_densities(minimizators, densities, lats_mean)

    print(i, np.round(lats_mean[active_segments - 1], decimals=3))
    print(i, np.round(densities_next[active_segments - 1], decimals=3))

    print()

    mesh = generator.update(mesh, densities_next[active_segments - 1],
                            active_segments)
    # density_next = FibrosisDensity.compute_density(mesh, segments)

    d_densities = densities_next - densities

    if np.all(np.abs(d_densities[active_segments - 1]) < 0.01):
        distant_segments_ind += 1

        if distant_segments_ind == len(distant_segments):
            print('Optimization finished')
            break

        active_segments = distant_segments[distant_segments_ind]
        print(i, 'Next segments', active_segments)
        print(i, np.round(lats_mean[active_segments - 1], decimals=3))
        print(i, np.round(densities_next[active_segments - 1], decimals=3))

        mesh = generator.update(mesh, densities_next[active_segments - 1],
                                active_segments)

    if np.all(np.abs(d_densities) < 0.01):
        print('Convergence achived')
        break

    # density_next = FibrosisDensity.compute_density(mesh, segments)

    # subdir = '{}'.format(i + 1)
    # path_next = path_step.joinpath(subdir)
    # path_next.mkdir(parents=True, exist_ok=True)
    # np.save(path_next.joinpath('tissue.npy'), mesh.astype(np.uint8))
    # run_simulation(path, path_step, subdir)
