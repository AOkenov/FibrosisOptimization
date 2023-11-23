import numpy as np
from finitewave.cpuwave3D.tissue.cardiac_tissue_3d import CardiacTissue3D
from finitewave.cpuwave3D.stencil.asymmetric_stencil_3d import (
    AsymmetricStencil3D
)
from finitewave.cpuwave3D.model.aliev_panfilov_3d.aliev_panfilov_3d import (
    AlievPanfilov3D
)
from finitewave.cpuwave3D.stimulation.stim_current_matrix_3d import (
    StimCurrentMatrix3D
)
from finitewave.core.stimulation.stim_sequence import StimSequence
from finitewave.core.tracker.tracker_sequence import TrackerSequence
from finitewave.cpuwave3D.tracker.ecg_3d_tracker import ECG3DTracker


def run_simulation(data_loaders, subdir, t_max, sampling_rate=40,
                   prog_bar=False):
    path_save = data_loaders['epi'].data_path
    fibers = data_loaders['epi'].load_fibers()
    stimul_coords = data_loaders['epi'].load_stimul_coords()
    mesh = data_loaders['epi'].load_mesh()

    tissue = CardiacTissue3D(mesh.shape)
    tissue.mesh = mesh
    tissue.add_boundaries()
    tissue.fibers = fibers
    tissue.stencil = AsymmetricStencil3D()
    tissue.D_al = 1
    tissue.D_ac = 1 / 9
    tissue.conductivity = 1

    model = AlievPanfilov3D()
    model.dt = 0.0015
    model.dr = 0.1
    model.t_max = t_max
    model.prog_bar = prog_bar

    stimul_matrix = np.zeros_like(mesh, dtype=bool)
    stimul_matrix[tuple(stimul_coords.T)] = 1

    stim = StimCurrentMatrix3D(0, 100, 0.2, stimul_matrix)
    stim_sequence = StimSequence()
    stim_sequence.add_stim(stim)

    tracker_sequence = TrackerSequence()

    egm_tracker = {}
    for surf_name, data_loader in data_loaders.items():
        electrodes = data_loader.load_electrodes()[:, :3]
        egm_tracker[surf_name] = ECG3DTracker(memory_save=True)
        egm_tracker[surf_name].step = sampling_rate
        egm_tracker[surf_name].measure_coords = electrodes
        tracker_sequence.add_tracker(egm_tracker[surf_name])

    model.cardiac_tissue = tissue
    model.stim_sequence = stim_sequence
    model.tracker_sequence = tracker_sequence

    model.run()

    for surf_name, tracker in egm_tracker.items():
        np.save(path_save.joinpath(subdir, 'egm_{}.npy'.format(surf_name)),
                tracker.ecg.astype(np.float32))
