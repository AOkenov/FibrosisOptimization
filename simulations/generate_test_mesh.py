from pathlib import Path
import numpy as np
from fibrosisoptimization.core.fibrosis_generator import FibrosisGenerator


path = Path('./data')

layers = np.load(path.joinpath('layers.npy'))
segments = np.load(path.joinpath('segments_17.npy'))
mesh = (segments > 0).astype(int)

segment_12 = (segments == 12).astype(int) * layers

densities = {'transmural': [0.25, 0.25, 0.25],
             'subendo': [0.35, 0.15, 0.02],
             'midmyo': [0.10, 0.35, 0.15],
             'subepi': [0.02, 0.15, 0.35]}


fibrosis_generator = FibrosisGenerator(segment_12)

for name, densities in densities.items():
    tissue = fibrosis_generator.update(mesh.copy(), densities, [1, 2, 3])
    np.save(path.joinpath('test_models/meshes', '{}.npy'.format(name)),
            tissue.astype('uint8'))
