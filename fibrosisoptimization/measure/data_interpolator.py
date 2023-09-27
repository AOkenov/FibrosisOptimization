import numpy as np

from fibropt.surface.surface import Surface
from fibropt.utils.surface_data import SurfaceData


class DataIntepolator:
    """Interpolate data from electrodes to surface
    """
    def __init__(self, coords, labels):
        self.surface_data = SurfaceData()
        self.surface_data.coords = coords
        self.surface_data.labels = labels
        self.surface_data.segments = np.unique(labels[labels > 0])

    def interpolate(self, electrodes_data: SurfaceData):
        """Interpolate LAT and PtP from electrodes to surface
        """
        pass
