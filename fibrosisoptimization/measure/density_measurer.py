import numpy as np
from scipy import ndimage


class DensityMeasurer:
    """Fibrosis density calculation module"""

    def __init__(self) -> None:
        """Initialize DensityMeasurer"""

    @staticmethod
    def compute_density_map(mesh, segments):
        """Compute the density map for segments.

        Parameters
        ----------
        mesh : np.ndarray
            Input mesh data.
        segments : np.ndarray
            Segmentation map.

        Returns
        -------
        np.ndarray
            Density map computed for the segments.
        """
        density_list = DensityMeasurer.compute_density(mesh, segments)
        density_map = density_list[segments - 1]
        density_map[segments == 0] = 0
        return density_map

    @staticmethod
    def compute_density(mesh, segments):
        """Compute mean density for labeled segments.

        This function computes the mean density for labeled segments.

        Parameters
        ----------
        mesh : np.ndarray
            Input mesh data.
        segments : np.ndarray
            Segmentation map.

        Returns
        -------
        np.ndarray
            Mean density for labeled segments.
        """
        index = np.unique(segments[segments > 0])
        density = ndimage.mean(mesh, segments, index=index)
        density -= 1
        return density
