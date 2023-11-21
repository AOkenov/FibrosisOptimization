import numpy as np

from fibrosisoptimization.core.surface_data import SurfaceData
from fibrosisoptimization.measure.measurers import Measurer


class DataUpdater:

    """Class for updating data

    Attributes
    ----------
    data : SurfaceData
        Description
    fs : float
        Sampling rate
    lat_reference : float
        Reference time used for measuring LAT
    """

    def __init__(self, coords, lat_reference, fs, segments=None):
        """Initialize

        Parameters
        ----------
        coords : np.ndarray
            Coords of the points
        lat_reference : float
            Reference time used for measuring LAT
        fs : float
            Sampling rate
        """
        self.lat_reference = lat_reference
        self.fs = fs

        self.data = SurfaceData()
        self.data.coords = coords
        self.data.segments = segments
        self.data.indices = np.unique(segments[segments > 0])
        self.data.ptp = np.zeros(len(coords))
        self.data.lat = np.zeros(len(coords))

    def update(self, egms):
        """Update data object and return new data object

        Parameters
        ----------
        egms : np.ndarray
            Array of the measured EGMs

        Returns
        -------
        SurfaceData
            Description
        """
        ptp, lat = Measurer.evaluate(egms, self.lat_reference, self.fs)
        out = self.data.copy()

        out.ptp = ptp
        out.lat = lat
        return out
