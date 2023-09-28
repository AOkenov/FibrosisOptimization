from pathlib import Path
import numpy as np

from fibrosisoptimization.core.fibrosis_generator import FibrosisGenerator
from fibrosisoptimization.measure.residual import Residual
from fibrosisoptimization.measure.fibrosis_density import FibrosisDensity
from fibrosisoptimization.minimization.minimizator import Minimizator

path = Path('/Users/arstanbek/Hulk/Arstan/data')
path_step = path.joinpath('LV')

max_iter = 100

residual = Residual(path_step, 'epi', 13, fs=1 / (40 * 0.0015))
segments = np.load(path_step.joinpath('segments.npy'))

residual.update_base('1')
residual.update_target('0')

minimizator = Minimizator('LV', 'LAT')
generator = FibrosisGenerator(segments)

for i in range(1, max_iter):
    subdir = '{}'.format(i)
    data = residual.update(subdir)
    lat_mean = - data.lat_mean_per_segment[0]

    mesh = np.load(path_step.joinpath(subdir, 'tissue.npy'))
    density = FibrosisDensity.compute_density(mesh, segments)[0]

    density_next = minimizator.update(density, lat_mean)

    mesh = generator.update(mesh, [density_next], [1])
    density_next = FibrosisDensity.compute_density(mesh, segments)[0]

    print(i, ': ', '{:.3f}'.format(lat_mean), '{:.2f}'.format(density), "-->",
          '{:.2f}'.format(density_next))

    if np.abs(density_next - density) < 0.01:
        print('Convergence achived')
        break

    # subdir = '{}'.format(i + 1)
    # path_next = path_step.joinpath(subdir)
    # path_next.mkdir(parents=True, exist_ok=True)
    # np.save(path_next.joinpath('tissue.npy'), mesh.astype(np.uint8))
    # run_simulation(path, path_step, subdir)
