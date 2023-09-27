import numpy as np
from scipy import ndimage
from dataclasses import dataclass


@dataclass
class SurfaceData:
    '''Class for keeping scalar values (amplitude, LAT)'''
    coords: np.ndarray = None
    labels: np.ndarray = None
    segments: np.ndarray = None
    amplitude: np.ndarray = None
    lat: np.ndarray = None

    def __add__(self, y):
        amplitude = self.amplitude + y.amplitude
        lat = self.lat + y.lat
        return SurfaceData(self.coords, self.labels, self.segments, amplitude, lat)
    
    def __sub__(self, y):
        amplitude = self.amplitude - y.amplitude
        lat = self.lat - y.lat
        return SurfaceData(self.coords, self.labels, self.segments, amplitude, lat)
    
    def __mul__(self, y):
        amplitude = self.amplitude * y.amplitude
        lat = self.lat * y.lat
        return SurfaceData(self.coords, self.labels, self.segments, amplitude, lat)
    
    def __truediv__(self, y):
        amplitude = self.amplitude / y.amplitude
        lat = self.lat / y.lat
        return SurfaceData(self.coords, self.labels, self.segments, amplitude, lat)
    
    def __pow__(self, n):
        amplitude = self.amplitude ** n
        lat = self.lat ** n
        return SurfaceData(self.coords, self.labels, self.segments, amplitude, lat)
    
    def abs(self):
        self.lat = np.abs(self.lat)
        self.amplitude = np.abs(self.amplitude)
        return self
    
    def copy(self):
        return SurfaceData(self.coords, self.labels, self.segments)
    
    def calculate_mean_per_segment(self, values):
        return ndimage.mean(values, self.labels, self.segments)   


class AmplitudeData(SurfaceData):
    @property
    def scalar(self):
        return self.amplitude
    
    @property
    def mean_per_segment(self):
        return super().calculate_mean_per_segment(self.amplitudes)
    

class LATData(SurfaceData):
    @property
    def scalar(self):
        return self.lat
    
    @property
    def mean_per_segment(self):
        return super().calculate_mean_per_segment(self.lat)


# coords = np.arange(15).reshape((5, 3))
# labels = np.array([1, 1, 2, 3, 4])
# segments = np.unique(labels)
# ampl = np.arange(1, 6)
# lat = np.arange(1, 6)

# data_0 = SurfaceData(coords, labels, segments, ampl, lat)
# data_1 = data_0.copy()
# data_1.amplitude = np.arange(3, 8)
# data_1.lat = np.arange(3, 8)

# out = ((data_0 - data_1) ** 2) / data_0

# print(out.amplitude, out.amplitude_label_mean)
# print(out.lat, out.lat_label_mean)