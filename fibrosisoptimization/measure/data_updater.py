import numpy as np
from copy import deepcopy

from fibrosisoptimization.core.surface_data import SurfaceData
from fibrosisoptimization.measure.measurers import Measurer


class DataUpdater:
    def __init__(self, coords, lat_reference, fs):
        self.lat_reference = lat_reference
        self.fs = fs

        self.data = SurfaceData()
        self.data.coords = coords
        self.data.ptp = np.zeros(len(coords))
        self.data.lat = np.zeros(len(coords))

    def update(self, egms):
        ptp, lat = Measurer.evaluate(egms, self.lat_reference, self.fs)
        out = self.data.copy()

        out.ptp = ptp
        out.lat = lat
        return out
