import numpy as np


class DataLoader:
    def __init__(self, surface_name=None, data_path=None, electrodes_path=None,
                 segments_path=None, layers_path=None, stimul_path=None,
                 fibers_path=None):
        self.surface_name = surface_name
        self.data_path = data_path
        self.electrodes_path = electrodes_path
        self.segments_path = segments_path
        self.layers_path = layers_path
        self.stimul_path = stimul_path
        self.fibers_path = fibers_path

    def load_electrodes(self):
        """Load electrode coordinates and segment labels

        Returns
        -------
        np.ndarray
            Electrode coordinates
        """
        filename = 'electrodes_{}.npy'.format(self.surface_name)
        return self.load_measuring_points(self.electrodes_path, filename)

    def load_surface(self):
        """Load  or surface coordinates and segment labels

        Returns
        -------
        np.ndarray
            Electrode coordinates
        """
        filename = 'surface_{}.npy'.format(self.surface_name)
        return self.load_measuring_points(self.electrodes_path, filename)

    def load_measuring_points(self, path, filename):
        data = np.load(path.joinpath(filename))

        if data.shape[1] != 4:
            message = '{} array should contain segment labels'.format(filename)
            raise ValueError(message)

        coords = data[:, :3]
        segment_labels = data[:, 3]

        return coords, segment_labels

    def load_segments(self):
        segments = np.load(self.segments_path.joinpath('segments.npy'))
        return segments

    def load_layers(self):
        layers = np.load(self.layers_path.joinpath('layers.npy'))
        return layers

    def load_layered_segments(self, number_of_segments=17):
        segments = self.load_segments()
        layers = self.load_layers()
        segments = (layers - 1) * number_of_segments + segments
        segments[layers == 0] = 0
        return segments

    def load_egms(self, subdir):
        """Update the data based on the provided subdirectory.

        Parameters
        ----------
        subdir : str
            Subdirectory containing data.

        Returns
        -------
        np.ndarray
            Updated data set.
        """
        filename = 'egm_{}.npy'.format(self.surface_name)
        egms = np.load(self.data_path.joinpath(subdir, filename))
        return egms

    def load_mesh(self, subdir):
        mesh = np.load(self.data_path.joinpath(subdir, 'tissue.npy'))
        return mesh

    def load_fibers(self):
        return np.load(self.fibers_path.joinpath('fibers.npy'))

    def load_stimul_coords(self):
        return np.load(self.stimul_path.joinpath('stimul_coords.npy'))
