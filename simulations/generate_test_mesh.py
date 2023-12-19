from pathlib import Path
import numpy as np
from fibrosisoptimization.core.fibrosis_generator import FibrosisGenerator

from fibrosisoptimization.measure import DataLoader


path = Path(__file__).parent.parent.joinpath('data')

segments_path = path.joinpath('models', 'left_ventricle', '17')
layers_path = path.joinpath('models')

data_loader = DataLoader(layers_path=layers_path, segments_path=segments_path)

segments = data_loader.load_segments()
layered_segments = data_loader.load_layered_segments()

mesh = (segments > 0).astype(int)

segment_12 = layered_segments.copy()
segment_12[segments != 12] = 0

densities = {'transmural': [0.25, 0.25, 0.25],
             'subendo': [0.35, 0.15, 0.02],
             'midmyo': [0.10, 0.35, 0.15],
             'subepi': [0.02, 0.15, 0.35]}


fibrosis_generator = FibrosisGenerator(segment_12)

for name, densities in densities.items():
    tissue = fibrosis_generator.update(mesh.copy(), densities, [1, 2, 3])
    # np.save(path.joinpath('test_models/meshes', '{}.npy'.format(name)),
    #         tissue.astype('uint8'))
