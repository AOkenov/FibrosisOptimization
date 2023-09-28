import numpy as np


class FibrosisGenerator:
    def __init__(self, segments):
        self.segments = segments
        self.random_mesh = np.random.random(segments.shape)

    def update(self, mesh, densities, active_segments):

        for segment, density in zip(active_segments, densities):
            mask = self.segments == segment
            mesh[mask] = 1
            mesh[mask & (self.random_mesh <= density)] = 2

        return mesh
