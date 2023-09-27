import numpy as np
from fibropt.measure.fibrosis_density import FibrosisDensity


class Measurer:
    def __init__(self) -> None:
        pass

    def update_data(data_updater, data_interpolator, subdir, dt):
        point_data = data_updater.update(subdir, fs=1/dt)
        surface_data = data_interpolator.calculate_surface_data(point_data)
        surface_data.segments = np.arange(1, 69)
        return surface_data

    def update_data_list(data_updater, data_interpolator, subdirs, dt):
        out = []
        for subdir in subdirs:
            res = Measurer.update_data(data_updater, data_interpolator, subdir, dt)
            out.append(res)
        return out

    def lat_error_list(surface_data):
        lat = []
        for data in surface_data:
            residuals = (surface_data[0] - data) / surface_data[1]
            lat.append(residuals.calculate_mean_per_segment(- residuals.lat))

        return np.array(lat)

    def amplitudes_error_list(surface_data):
        '''
        Calculates normed EGM amplitudes residuals:
        (PP[0] - PP[i] ) / PP[1]

        Args:
            surface_data (list): list of surface data
        '''

        amplitudes = []
        for data in surface_data:
            residuals = (surface_data[0] - data) / surface_data[1]
            amplitudes.append(residuals.calculate_mean_per_segment(residuals.amplitudes))

        return np.array(amplitudes)

    def density_error(path, subdir, labels, target=0):
        density_target = Measurer.density(path, target, labels)
        density_estimated = Measurer.density(path, subdir, labels)
        return density_target - density_estimated

    def density_error_list(path, subdirs, labels):
        out = []
        for subdir in subdirs:
            out.append(Measurer.density_error(path, subdir, labels))

        return np.array(out)

    def density(path, subdir, labels):
        mesh = np.load(path.joinpath('{}/tissue.npy'.format(subdir)))
        return FibrosisDensity.compute_density(mesh, labels)
