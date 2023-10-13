import numpy as np
from scipy import ndimage


class FibrosisDensity:
    def __init__(self) -> None:
        pass

    @staticmethod
    def compute_density(mesh, segments, as_map=False):
        '''
        Computes density map for all segments
        '''
        index = np.unique(segments[segments > 0])
        out = ndimage.mean(mesh, segments, index=index)
        out -= 1

        if as_map:
            res = out[segments - 1]
            res[segments == 0] = 0
            return res

        return out
