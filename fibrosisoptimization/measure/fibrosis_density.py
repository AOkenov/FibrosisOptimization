import numpy as np
from scipy import ndimage


class FibrosisDensity:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def compute_density(mesh, labels, as_map=False):
        '''
        Computes density map for all labels
        '''
        index = np.unique(labels[labels > 0])
        out = ndimage.mean(mesh, labels, index=index)
        out -= 1

        if as_map:
            res = out[labels - 1]
            res[labels == 0] = 0
            return res
        
        return out