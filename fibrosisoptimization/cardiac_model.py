import numpy as np
import numba
from finitewave.cpuwave3D.tracker import ECG3DTracker
from finitewave.core.tracker import TrackerSequence
from finitewave.core.stimulation import StimSequence
from finitewave.cpuwave3D.stencil import AsymmetricStencil3D
from finitewave.cpuwave3D.stimulation import StimVoltages3D
from finitewave.cpuwave3D.model import AlievPanfilov3D
from finitewave.cpuwave3D.tissue import CardiacTissue3D


numba.set_num_threads(4)


class CardiacModel:
    def __init__(self):
        self._fibers = None
        self._stimul_coords = None
        self._stimul_voltage = None
        self._electrodes = {}
        self._electrodes_labels = {}
        self.path = ''
    
    def load_fibers(self, path, filename='fibers.npy'):
        self._fibers = np.load(path.joinpath(filename)).astype('float32')

    def load_stimul_coords(self, path, filename='stimuls_coords.npy'):
        self._stimul_coords = np.load(path.joinpath(filename)
                                      ).astype('int32')
    
    def load_stimul_voltage(self, path, filename):
        self._stimul_voltage = np.load(path.joinpath(filename))

    def load_electrodes(self, path):
        for surf_name in ['endo', 'epi']:
            self._electrodes[surf_name] = np.load(
                path.joinpath('electrodes_{}.npy'.format(surf_name))
                ).astype('int32')
            self._electrodes_labels[surf_name] = np.load(
                path.joinpath('electrodes_{}_labels.npy'.format(surf_name))
            )

    def run(self, subdir, t_max=10, memory_save=False, prog_bar=True,
            surfaces=['endo', 'epi']):
        mesh = np.load(self.path.joinpath(subdir, 'tissue.npy')).astype('uint8')

        active_labels = np.load(self.path.joinpath(subdir, 'labels.npy')
                                ).astype('int32')

        tissue = CardiacTissue3D(mesh.shape)
        tissue.mesh = mesh
        tissue.add_boundaries()
        tissue.fibers = self._fibers
        tissue.stencil = AsymmetricStencil3D()
        tissue.D_al = 1
        tissue.D_ac = tissue.D_al/9
        tissue.conductivity = 1

        model = AlievPanfilov3D()
        model.dt = 0.0015
        model.dr = 0.1
        model.t_max = t_max
        model.prog_bar = prog_bar

        stim = StimVoltages3D(0, 3, self._stimul_voltage, self._stimul_coords)
        stim_sequence = StimSequence()
        stim_sequence.add_stim(stim)

        tracker_sequence = TrackerSequence()

        egm_tracker = {}
        for surf_name in surfaces:
            mask = np.any(self._electrodes_labels[surf_name][:, active_labels - 1], axis=1)
            electrodes = self._electrodes[surf_name][mask]
            egm_tracker[surf_name] = ECG3DTracker(memory_save=memory_save)
            egm_tracker[surf_name].step = 40
            egm_tracker[surf_name].measure_coords = electrodes
            tracker_sequence.add_tracker(egm_tracker[surf_name])

        model.cardiac_tissue = tissue
        model.stim_sequence = stim_sequence
        model.tracker_sequence = tracker_sequence

        print('RUNNING {}'.format(subdir))

        model.run()

        for surf_name, tracker in egm_tracker.items():
            np.save(self.path.joinpath(subdir, 'ecg_{}.npy'.format(surf_name)),
                    tracker.ecg.astype(np.float32))
