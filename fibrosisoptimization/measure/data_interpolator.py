import numpy as np
from scipy import spatial

from fibrosisoptimization.core.surface_data import SurfaceData


class DataIntepolator:
    """Interpolate data from electrodes to surface
    """
    def __init__(self, coords, segments):
        self.data = SurfaceData()
        self.data.coords = coords
        self.data.segments = segments
        self.data.indices = np.unique(segments[segments > 0])
        self.weights = None

    def add_weights(self, coords):
        self.weights = self.compute_weights(self.data.coords, coords)

    def interpolate(self, electrodes_data):
        """Interpolate LAT and PtP from electrodes to surface
        """
        out = self.data.copy()
        out.lat = self._interpolate(electrodes_data.lat)
        out.ptp = self._interpolate(electrodes_data.ptp)
        return out

    def _interpolate(self, values):
        values = self.weights * values
        return values.sum(axis=1) / self.weights.sum(axis=1)

    def compute_weights(self, surface_points, electrode_points, r=30):
        d = spatial.distance.cdist(surface_points, electrode_points)
        w = np.zeros_like(d)
        _ = np.divide(np.maximum(0, r - d), (r * d), where=d != 0, out=w) ** 2
        w[d == 0] = 1
        return w
