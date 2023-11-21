import numpy as np
from fibrosisoptimization.measure.data_updater import DataUpdater
from fibrosisoptimization.measure.data_interpolator import DataInterpolator


class Residuals:
    """Residuals class to compute residuals between base and target data sets.

    Attributes
    ----------
    base_data: np.ndarray
        Base data set.
    target_data : np.ndarray
        Target data set.
    last_data : np.ndarray
        Current data set.
    interpolate : bool
        Flag to enable interpolation
    data_interpolator : DataInterpolator
        Object for data interpolation.
    data_updater : DataUpdater
        Object for updating electrode data.
    path : str
        Path to the data directory.
    surface_name : str
        Name of the surface.
    """

    def __init__(self, path, surface_name, lat_reference, fs,
                 interpolate=True):
        """Initialize an instance of Residuals.

        Parameters
        ----------
        path : str
            Path to the data directory.
        surface_name : str
            Name of the surface.
        lat_reference : float
            Latency reference for data processing.
        fs : int
            Sampling frequency.
        interpolate : bool
            If True interpolated value will be returned, else original
            electrodes data. Default True.
        """
        self.path = path
        self.surface_name = surface_name
        self.interpolate = interpolate

        self.base_data = None
        self.target_data = None
        self.last_data = None

        # Load electrode coordinates
        electrode_coords = self.load_electrodes()
        electrode_segments = np.ones(len(electrode_coords))

        if electrode_coords.shape[1] == 4:
            electrode_segments = electrode_coords[:, 3]
            electrode_coords = electrode_coords[:, :3]

        # Initialize DataUpdater and DataInterpolator objects
        self.data_updater = DataUpdater(electrode_coords, lat_reference, fs,
                                        electrode_segments)

        self.data_interpolator = None

        if self.interpolate:
            filename = 'surface_{}.npy'.format(surface_name)
            surface = np.load(path.joinpath(filename))
            self.data_interpolator = DataInterpolator(surface[:, :3],
                                                      surface[:, 3])
            self.data_interpolator.add_weights(electrode_coords)

    def load_electrodes(self):
        """Load electrode coordinates

        Returns
        -------
        np.ndarray
            Electrode coordinates
        """
        filename = 'electrodes_{}.npy'.format(self.surface_name)
        return np.load(self.path.joinpath(filename))

    def update_base(self, subdir):
        """Update the base data set.

        Parameters
        ----------
        subdir : str
            Subdirectory containing data for base update.
        """
        self.base_data = self.load_data(subdir)

    def update_target(self, subdir):
        """Update the target data set.

        Parameters
        ----------
        subdir : str
            Subdirectory containing data for target update.
        """
        self.target_data = self.load_data(subdir)

    def update(self, subdir):
        """Update and compute residuals between target and current data.

        Parameters
        ----------
        subdir : str
            Subdirectory containing current data.

        Returns
        -------
        np.ndarray
            Residuals between target and current data.
        """
        self.last_data = self.load_data(subdir)
        return (self.target_data - self.last_data) / self.base_data

    def load_data(self, subdir):
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
        egms = np.load(self.path.joinpath(subdir, filename))
        electrode_data = self.data_updater.update(egms)

        if self.interpolate:
            return self.data_interpolator.interpolate(electrode_data)

        return electrode_data
