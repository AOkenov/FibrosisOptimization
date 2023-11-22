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

    def __init__(self, data_loader, lat_reference, fs, interpolate=True):
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
        model_subdir : str
            Subdirectory of current simulation
        """
        self.base_data = None
        self.target_data = None
        self.last_data = None

        self.interpolate = interpolate

        self.data_loader = data_loader

        els_coords, els_segments = data_loader.load_electrodes()
        self.data_updater = DataUpdater(els_coords, lat_reference, fs,
                                        els_segments)

        self.data_interpolator = None
        if self.interpolate:
            surf_coords, surf_segments = data_loader.load_surface()
            self.data_interpolator = DataInterpolator(surf_coords,
                                                      surf_segments)
            self.data_interpolator.add_weights(els_coords)

    def update_base(self, subdir):
        """Update the base data set.

        Parameters
        ----------
        subdir : str
            Subdirectory containing data for base update.
        """
        self.base_data = self.load_subdir_data(subdir)

    def update_target(self, subdir):
        """Update the target data set.

        Parameters
        ----------
        subdir : str
            Subdirectory containing data for target update.
        """
        self.target_data = self.load_subdir_data(subdir)

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
        self.last_data = self.load_subdir_data(subdir)
        return (self.target_data - self.last_data) / self.base_data

    def load_subdir_data(self, subdir):
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
        egms = self.data_loader.load_egms(subdir)
        electrode_data = self.data_updater.update(egms)

        if not self.interpolate:
            return electrode_data

        return self.data_interpolator.interpolate(electrode_data)
