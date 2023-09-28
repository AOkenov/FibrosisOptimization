from pathlib import Path
import numpy as np
from fibropt.vtktools.vtk_mesh_builder import VTKMeshBuilder


path = Path('/Users/arstanbek/Hulk/Arstan/optimization/data/real-like/exp_old')
path_save = Path('/Users/arstanbek/Projects/FibrosisOptimization/data/vtk')

mesh = np.load(path.joinpath('segments_68.npy'))

coords = np.argwhere(mesh > 0)
scalars = mesh[mesh > 0]

builder = VTKMeshBuilder()
builder.create_points(coords)
builder.add_scalar(scalars, 'Segments')
builder.add_vertexes()
builder.write(str(path_save.joinpath('segments_68.vtk')))
