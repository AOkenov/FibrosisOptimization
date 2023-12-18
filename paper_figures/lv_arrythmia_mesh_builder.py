from pathlib import Path
import numpy as np
from fibropt.vtktools.vtk_mesh_builder import VTKMeshBuilder


path = Path('/Users/arstanbek/Projects/FibrosisOptimization/data')
path_save = path.joinpath('vtk')

experiment = 'odf_frames'
subdirs = ['initial']
frame_inds = list(range(30))

path_exp = path.joinpath('rotor', experiment)

coords = np.loadtxt(path.joinpath('endo_surface.txt'))[:, :3].astype(int)
# coords = np.argwhere(mesh > 0)

pacing_interval = '28_15'

builder = VTKMeshBuilder()
builder.create_points(coords)

for subdir in subdirs:
    mesh = np.load(path.joinpath('rotor/meshes/{}/tissue.npy'.format(subdir)))
    for ind in frame_inds:
        scalar = np.load(path_exp.joinpath(str(subdir), str(pacing_interval),
                                            'u_{}.npy'.format(ind)))
        scalar_mesh = np.zeros_like(mesh, dtype='float')
        scalar_mesh[mesh > 0] = scalar
        # scalar_mesh = np.load(path_exp.joinpath(str(subdir), str(pacing_interval),
        #                                     'u_{}.npy'.format(ind)))
        scalars = scalar_mesh[tuple(coords.T)]

        builder.add_scalar(scalars, '{}_{}'.format(subdir, ind))

builder.add_vertexes()
# builder.write(str(path_save.joinpath('arrhythmia_{}.vtk'.format(experiment))))
