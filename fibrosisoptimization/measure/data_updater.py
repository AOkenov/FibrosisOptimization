import numpy as np

from fibropt.utils.surface_data import SurfaceData
from fibropt.measure.measurers import Measurer


class ElectrodesDataUpdater:
    def __init__(self, path_exp, surface_name, lat_reference):
        self.path_exp = path_exp
        self.surface_name = surface_name
        self.lat_reference = lat_reference
        self.initialize()

    def initialize(self):
        coords, labels = self.load_electrodes()

        self.data = SurfaceData()
        self.data.coords = coords
        self.data.amplitude = np.zeros(len(coords))
        self.data.lat = np.zeros(len(coords))

        self.segment_electrodes_labels = labels

    def load_electrodes(self):
        '''
        Returns:
            np.ndarray[M, 3]: electrodes position on the surface
            np.ndarray[L, M]: Mask for each of L segments' electrodes
        '''
        filename = 'electrodes_{}.npy'.format(self.surface_name)
        coords = np.load(self.path_exp.joinpath(filename))

        filename = 'electrodes_{}_labels.npy'.format(self.surface_name)
        labels = np.load(self.path_exp.joinpath(filename))

        return coords, labels

    def load_signals(self, dirname):
        path = self.path_exp.joinpath(str(dirname))
        filename = 'ecg_{}.npy'.format(self.surface_name)
        signals = np.load(path.joinpath(filename))
        labels = np.load(path.joinpath('labels.npy'))
        return signals, labels

    def update(self, dirname, fs):
        signals, labels = self.load_signals(dirname)
        active_electrodes_mask = self.active_electrodes_mask(labels)

        amplitude, lat = Measurer.evaluate(signals, self.lat_reference, fs)

        self.data.amplitude[active_electrodes_mask] = amplitude
        self.data.lat[active_electrodes_mask] = lat
        return self.data

    def active_electrodes_mask(self, labels):
        return self.segment_electrodes_labels[:, labels - 1].any(axis=1)
