from pathlib import Path
import numpy as np

from fibrosisoptimization.plotter.interactive_plotter import InteractivePlotter


path = Path('./data')
path_step = path.joinpath('sub-epi')

segments_list = np.array([29, 30, 41, 42])

mesh = np.load(path.joinpath('17/1/tissue.npy'))
els_coords = np.load(path.joinpath('17/electrodes_endo.npy'))
egms = np.load(path.joinpath('17/1/egm_endo.npy'))
segments = np.load(path.joinpath('17/segments.npy'))
mesh_mask = np.isin(segments, [12])

print(mesh[mesh_mask].shape)

els_labels = np.load(path_step.joinpath('electrodes_endo_labels.npy'))
egms_mask = np.any(els_labels[:, segments_list - 1], axis=1)
segment_labels = np.load(path_step.joinpath('labels.npy'))
segment_mask = np.isin(segment_labels, segments_list)

print(segment_mask[segment_mask].shape)

for i in range(10):
    mesh_ = mesh.copy()
    egms_ = egms.copy()

    subdir = '{}'.format(i)

    segment_mesh = np.load(path_step.joinpath(subdir, 'tissue.npy'))
    segment_egm = np.load(path_step.joinpath(subdir, 'ecg_endo.npy'))

    print(subdir, segment_mesh.shape, segment_egm.shape)

    # mesh_[mesh_mask] = segment_mesh[segment_mask]
    egms_[egms_mask] = segment_egm
    # np.save(path_step.joinpath(subdir, 'tissue.npy'), mesh_.astype(np.uint8))
    np.save(path_step.joinpath(subdir, 'egm_endo.npy'),
            egms_.astype(np.float32))

coords = np.argwhere(mesh)
lat = mesh_mask[mesh > 0]

plotter = InteractivePlotter()
plotter.build_grid(coords)
plotter.add_scalar(lat.astype(np.float32))
plotter.add_grid(clim=[0, 2])
plotter.add_points(els_coords[:, :3].astype(np.float32),
                   render_points_as_spheres=True, point_size=20.0)
# plotter.update()
plotter.show()
