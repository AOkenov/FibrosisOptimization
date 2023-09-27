from pathlib import Path


path = Path('.')
mesh = np.load(path.joinpath('mesh.npy'))
fibers = np.load(path.joinpath('fibers.npy'))
stimul_coords = np.load(path.joinpath('stimul_coords.npy'))
stimul_voltage = np.load(path.joinpath('stimul_voltage.npy'))
electrodes = {}
electrodes['endo'] = np.load(path.joinpath('endo_electrodes.npy'))
electrodes['epi'] = np.load(paht.joinpath('epi_electrodes.npy'))


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

stim = StimVoltages3D(0, 3, stimul_voltage, stimul_coords)
stim_sequence = StimSequence()
stim_sequence.add_stim(stim)

tracker_sequence = TrackerSequence()

egm_tracker = {}
for k, v in electrodes.items():
    egm_tracker[k] = ECG3DTracker(memory_save=True)
    egm_tracker[k].step = 40
    egm_tracker[l].measure_coords = v
    tracker_sequence.add_tracker(egm_tracker[k])

model.cardiac_tissue = tissue
model.stim_sequence = stim_sequence
model.tracker_sequence = tracker_sequence

model.run()

for surf_name, tracker in egm_tracker.items():
    np.save(self.path.joinpath(subdir, 'ecg_{}.npy'.format(surf_name)),
            tracker.ecg.astype(np.float32))
