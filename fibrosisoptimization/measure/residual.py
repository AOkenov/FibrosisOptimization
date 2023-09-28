import numpy as np
from fibrosisoptimization.measure.data_updater import DataUpdater
from fibrosisoptimization.measure.data_interpolator import DataIntepolator


class Residual:
    def __init__(self, path, surface_name, lat_reference, fs):
        self.path = path
        self.surface_name = surface_name
        electrode_coords = np.load(path.joinpath('electrodes_{}.npy'.format(surface_name)))
        self.data_updater = DataUpdater(electrode_coords, lat_reference, fs)

        surface = np.load(path.joinpath('surface_{}.npy'.format(surface_name)))
        self.data_interpolator = DataIntepolator(surface[:, :3], surface[:, 3])
        self.data_interpolator.add_weights(electrode_coords)

    def update_base(self, subdir):
        self.base = self._update(subdir)

    def update_target(self, subdir):
        self.target = self._update(subdir)

    def update(self, subdir):
        curr = self._update(subdir)
        return (self.target - curr) / self.base


    def _update(self, subdir):
        egms = np.load(self.path.joinpath(subdir,
                                          'egm_{}.npy'.format(self.surface_name)))
        electrode_data = self.data_updater.update(egms)
        return self.data_interpolator.interpolate(electrode_data)
