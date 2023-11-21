import numpy as np
from scipy import spatial

from fibrosisoptimization.core.surface_data import SurfaceData


class DataInterpolator:
    """Interpolate data from electrodes to surface

    Attributes
    ----------
    data : SurfaceData
        Data obejct containing LAT and PtP
    weights : np.ndarray
        Weights to interpolate point data to surface
    """

    def __init__(self, coords, segments):
        """Initialize

        Parameters
        ----------
        coords : np.ndarray[N, 3]
            Coords of the surface points
        segments : np.ndarray[N,]
            Surface points labels (segment indexes)
        """
        self.data = SurfaceData()
        self.data.coords = coords
        self.data.segments = segments
        self.data.indices = np.unique(segments[segments > 0])
        self.weights = None

    def add_weights(self, coords):
        """Compute weights for interpolation

        Parameters
        ----------
        coords : np.ndarray[N, 3]
            Coords of the measuring electrodes
        """
        self.weights = self.compute_weights(self.data.coords, coords)

    def interpolate(self, electrodes_data):
        """Interpolate LAT and PtP from electrodes to surface

        Parameters
        ----------
        electrodes_data : SurfaceData
            Data object containing LAT and PtP
            at measuring electrodes

        Returns
        -------
        SurfaceData
            Data object with interpolated LAT and PtP
        """
        out = self.data.copy()
        out.lat = self._interpolate(electrodes_data.lat)
        out.ptp = self._interpolate(electrodes_data.ptp)
        return out

    def _interpolate(self, values):
        values = self.weights * values
        return values.sum(axis=1) / self.weights.sum(axis=1)

    def compute_weights(self, surface_points, electrode_points, r=30):
        """Summary

        Parameters
        ----------
        surface_points : np.ndarray
            Unknown point coords (surface)
        electrode_points : np.ndarray
            Known point coords (electrodes)
        r : float, optional
            All point within radius will be used for
            interpolation

        Returns
        -------
        np.ndarray
            Weights for interpolation
        """
        d = spatial.distance.cdist(surface_points, electrode_points)
        w = np.zeros_like(d)
        _ = np.divide(np.maximum(0, r - d), (r * d), where=d != 0, out=w) ** 2
        w[d == 0] = 1
        print(d.min())
        return w
