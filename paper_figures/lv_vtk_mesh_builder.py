from pathlib import Path
import numpy as np
from fibropt.vtktools.vtk_mesh_builder import VTKMeshBuilder


path = Path('/Users/arstanbek/Projects/fibrosis-workspace/fibrosisoptimization/data')
path_save = path.joinpath('vtk')

mesh = np.load(path.joinpath('exp_endo/0/tissue.npy'))

coords = np.argwhere(mesh > 0)
scalars = mesh[mesh > 0]

builder = VTKMeshBuilder()
builder.create_points(coords)
builder.add_scalar(scalars, 'Mesh')
builder.add_vertexes()
builder.write(str(path_save.joinpath('mesh.vtk')))
