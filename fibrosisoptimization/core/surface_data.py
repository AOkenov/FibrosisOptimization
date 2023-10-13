import numpy as np
from scipy import ndimage
from dataclasses import dataclass


@dataclass
class SurfaceData:
    """Class for keeping scalar values (PtP amplitudes, LAT)

    Args:
        coords (np.ndarray[N, 3]): Position of N points in 3D space
        segmenst (np.ndarray[N,]): Segment to which point are belong
        indices (np.ndarray[M,]): Array of unique segments
        ptp (np.ndarray[N,]): PtP amplitudes
        lat (np.ndarray[N,]): LAT values
    """
    coords: np.ndarray = None
    segments: np.ndarray = None
    indices: np.ndarray = None
    ptp: np.ndarray = None
    lat: np.ndarray = None

    def __add__(self, y):
        ptp = self.ptp + y.ptp
        lat = self.lat + y.lat
        return SurfaceData(self.coords, self.segments, self.indices, ptp, lat)

    def __sub__(self, y):
        ptp = self.ptp - y.ptp
        lat = self.lat - y.lat
        return SurfaceData(self.coords, self.segments, self.indices, ptp, lat)

    def __mul__(self, y):
        ptp = self.ptp * y.ptp
        lat = self.lat * y.lat
        return SurfaceData(self.coords, self.segments, self.indices, ptp, lat)

    def __truediv__(self, y):
        ptp = self.ptp / y.ptp
        lat = self.lat / y.lat
        return SurfaceData(self.coords, self.segments, self.indices, ptp, lat)

    def __pow__(self, n):
        ptp = self.ptp ** n
        lat = self.lat ** n
        return SurfaceData(self.coords, self.segments, self.indices, ptp, lat)

    def abs(self):
        self.lat = np.abs(self.lat)
        self.ptp = np.abs(self.ptp)
        return self

    def copy(self):
        return SurfaceData(self.coords, self.segments, self.indices)

    @property
    def lat_mean_per_segment(self):
        return ndimage.mean(self.lat, self.segments, self.indices)

    @property
    def ptp_mean_per_segment(self):
        return ndimage.mean(self.ptp, self.segments, self.indices)


# coords = np.arange(15).reshape((5, 3))
# segments = np.array([1, 1, 2, 3, 4])
# indices = np.unique(segments)
# ptp = np.arange(1, 6)
# lat = np.arange(1, 6)
# data_0 = SurfaceData(coords, segments, indices, ptp, lat)

# data_1 = data_0.copy()
# data_1.ptp = np.arange(3, 8)
# data_1.lat = np.arange(3, 8)

# out = (data_0 - data_1) / data_0

# print(out.ptp, out.ptp_mean_per_segment)
# print(out.lat, out.lat_mean_per_segment)
