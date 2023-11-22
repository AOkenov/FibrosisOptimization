import numpy as np
from fibrosisoptimization.minimizators.minimizator import Minimizator


class LocalMinimizatorsCollection:
    """LocalMinimizatorsCollection class for managing endo, mid, and epi
    segments minimizators.

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
    max_switch_number : int, optional
        Maximum switch count. Defaults to 9.

    Attributes
    ----------
    active_minimizator : Minimizator
        Active Minimizator instance.
    density_step_tol : float
        Tolerance for density step change.
    max_switch_number : int
        Maximum switch count.
    number_of_segments : int
            Number of segments in the surface data
    minimizators : list
        List of Minimizator instances.
    switch_counter : int
        Counter for switches.
    """

    def __init__(self, segments, number_of_segments,
                 value_names=['PtP_ENDO', 'PtP_EPI', 'LAT'],
                 density_step_tol=0.01, max_switch_number=9):
        """Initialize a MinimizatorsCollection object.

        Parameters
        ----------
        segments : list
            List of segment information.
        number_of_segments : int
            Number of segments in the surface data
        value_names : list, optional
            List of value names. Defaults to ['PtP', 'PtP', 'LAT'].
        density_step_tol : float, optional
            Tolerance for density step change. Defaults to 0.01.
        max_switch_number : int, optional
            Maximum switch count. Defaults to 9.
        """
        self.number_of_segments = number_of_segments
        self.density_step_tol = density_step_tol
        self.max_switch_number = max_switch_number
        self.minimizators = self.make_minimizators(segments, value_names)

        self.active_minimizator = None
        self.switch_counter = 0

        self.switch_minimizator()

    @property
    def segments(self):
        """Get segment information for all Minimizator instances.

        Returns
        -------
        list
            List of segment information for each Minimizator.
        """
        return np.array(
            [minimizator.segment for minimizator in self.minimizators])

    @property
    def value_names(self):
        """Get value names for all Minimizator instances.

        Returns
        -------
        list
            List of value names for each Minimizator.
        """
        return np.array(
            [minimizator.value_name for minimizator in self.minimizators])

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

    def _update(self, densities, surface_data_endo, surface_data_epi):
        """Internal method to update Minimizator based on densities and
        surface data.

        Parameters
        ----------
        densities : list
            List of density values.
        surface_data_endo : SurfaceData
            Endocardial surface data object.
        surface_data_epi: SurfaceData
            Epicardial surface data object.

        Returns
        -------
        tuple
            Tuple of active minimizator density and new density value.
        """
        if self.active_minimizator.value_name == 'PtP_ENDO':
            values = surface_data_endo.ptp_mean_per_segment

        if self.active_minimizator.value_name == 'PtP_EPI':
            values = surface_data_epi.ptp_mean_per_segment

        if self.active_minimizator.value_name == 'LAT':
            values = -surface_data_epi.lat_mean_per_segment

        segment_ind = self.active_minimizator.segment - 1
        value = values[segment_ind % self.number_of_segments]
        density = densities[segment_ind]

        density_new = self.active_minimizator.update(density, value)

        print('SEGMENT: {}'.format(self.active_minimizator.segment))
        print('    {}: {:.3f}'.format(self.active_minimizator.value_name,
                                      value))
        print('DENSITY: {:.3f} --> {:.3f}'.format(density, density_new))

        return density, density_new

    def update(self, densities, surface_data_endo, surface_data_epi):
        """Update Minimizators based on densities and surface data.

        Parameters
        ----------
        densities : list
            List of density values.
        surface_data_endo : SurfaceData
            Endocardial surface data object.
        surface_data_epi: SurfaceData
            Epicardial surface data object.

        Returns
        -------
        list
            Updated list of density values.
        """

        densities = densities.copy()

        while self.switch_counter <= self.max_switch_number:
            density, density_new = self._update(densities, surface_data_endo,
                                                surface_data_epi)

            if abs(density_new - density) < self.density_step_tol:
                self.switch_minimizator()

            else:
                densities[self.active_minimizator.segment - 1] = density_new
                return densities

        return densities

    def switch_minimizator(self):
        """Switch the active Minimizator instance.
        """
        ind = self.switch_counter % len(self.minimizators)
        self.switch_counter += 1

        self.active_minimizator = self.minimizators[ind]

        print('********************************************')
        print('SWITCHED TO: {} {}'.format(self.active_minimizator.segment,
                                          self.active_minimizator.value_name))
        self.active_minimizator.reset()
