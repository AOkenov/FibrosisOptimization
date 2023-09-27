import numpy as np
from pathlib import Path


class Electrogram:
    def __init__(self, path: Path, surface_name: str):
        self.path = path
        self.surface_name = surface_name
        self.electrodes_labels = np.load(self.path.joinpath('electrodes_{}_labels.npy'.format(surface_name)))
        self.signals = None

    def load(self, dirname):
        self.signals = np.load(self.path.joinpath(str(dirname)).joinpath('ecg_{}.npy'.format(self.surface_name)))
        return self.signals
    
    def update(self, dirname):
        labels = np.load(self.path.joinpath(str(dirname)).joinpath('labels.npy'))
        egms = np.load(self.path.joinpath(str(dirname)).joinpath('ecg_{}.npy'.format(self.surface_name)))
        active_electrodes_mask = self.active_electrodes_mask(labels)
        self.signals[active_electrodes_mask] = egms 
        return self.signals
    
    def active_electrodes_mask(self, labels):
        return self.electrodes_labels[:, labels - 1].any(axis=1)