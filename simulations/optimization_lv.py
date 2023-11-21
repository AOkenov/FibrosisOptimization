from pathlib import Path
import numpy as np

from fibrosisoptimization.core.fibrosis_generator import FibrosisGenerator
from fibrosisoptimization.measure.residuals import Residuals
from fibrosisoptimization.measure.fibrosis_density import FibrosisDensity
from fibrosisoptimization.minimizators import (
    MinimizatorsCollection
)


path = Path('./data')
path_step = path.joinpath('LV')

max_iter = 10
segments_list = [1]

residuals = Residuals(path_step, 'epi', 13, fs=1 / (40 * 0.0015))
segments = np.load(path_step.joinpath('segments.npy'))

residuals.update_base('1')
residuals.update_target('0')

minimizators = MinimizatorsCollection(segments_list, ['LAT'])

generator = FibrosisGenerator(segments)

for i in range(1, max_iter):
    print('--------------------------------------------')
    print('ITERATION: {}'.format(i))
    subdir = '{}'.format(i)
    data = residuals.update(subdir)

    mesh = np.load(path_step.joinpath(subdir, 'tissue.npy'))
    densities = FibrosisDensity.compute_density(mesh, segments)

    densities_next = minimizators.update(densities, data)

    if np.all(np.abs(densities_next - densities) < 0.01):
        print('CONVERGENCE ACHIVED')
        break

    mesh = generator.update(mesh, densities_next, segments)

    # subdir = '{}'.format(i + 1)
    # path_next = path_step.joinpath(subdir)
    # path_next.mkdir(parents=True, exist_ok=True)
    # np.save(path_next.joinpath('tissue.npy'), mesh.astype(np.uint8))
    # run_simulation(path, path_step, subdir)
