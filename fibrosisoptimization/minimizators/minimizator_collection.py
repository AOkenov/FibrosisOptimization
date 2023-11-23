import numpy as np
from fibrosisoptimization.minimizators.minimizator import (
    Minimizator
)


class MinimizatorCollection:
    """MinimizatorCollection class for managing multiple independent
    minimizators.

    This class manages a collection of Minimizator instances for
    optimization purposes.

    Parameters
    ----------
    segments : list
        List of segment information.
    value_names : list, optional
        List of value names. Defaults to ['PtP', 'PtP', 'LAT'].
    density_step_tol : float, optional
        Tolerance for density step change. Defaults to 0.01.

    Attributes
    ----------
    density_step_tol : float
        Tolerance for density step change.
    minimizators : list
        List of Minimizator instances.
    """

    def __init__(self, segments=[], value_names=[], density_step_tol=0.01):
        """Initialize a MinimizatorCollection object.

        Parameters
        ----------
        segments : list
            List of segment information.
        value_names : list, optional
            List of value names. Defaults to [].
        density_step_tol : float, optional
            Tolerance for density step change. Defaults to 0.01.
        """
        self.density_step_tol = density_step_tol
        self.minimizators = self.make_minimizators(segments, value_names)

    @property
    def segments(self):
        """Get segment information for all Minimizator instances.

        Returns
        -------
        list
            List of segment information for each Minimizator.
        """
        return np.array([minimizator.segment for minimizator in self.minimizators])

    @property
    def value_names(self):
        """Get value names for all Minimizator instances.

        Returns
        -------
        list
            List of value names for each Minimizator.
        """
        return [minimizator.value_name for minimizator in self.minimizators]

    def make_minimizators(self, segments, value_names):
        """Create Minimizator instances based on segment and value names.

        Parameters
        ----------
        segments : list
            List of segment information.
        value_names : list
            List of value names.

        Returns
        -------
        list
            List of Minimizator instances.
        """
        minimizators = []
        for segment, value_name in zip(segments, value_names):
            minimizators.append(Minimizator(segment, value_name))
        return minimizators

    def update(self, densities, surface_data):
        pass
