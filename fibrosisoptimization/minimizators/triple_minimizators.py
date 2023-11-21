from fibrosisoptimization.minimizators.minimizator import Minimizator


class MinimizatorsCollection:
    """MinimizatorsCollection class for managing multiple minimizators.

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
    minimizators : list
        List of Minimizator instances.
    switch_counter : int
        Counter for switches.
    """

    def __init__(self, segments, value_names=['PtP', 'PtP', 'LAT'],
                 density_step_tol=0.01, max_switch_number=9):
        """Initialize a MinimizatorsCollection object.

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
        """
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
        return [minimizator.segment for minimizator in self.minimizators]

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

    def _update(self, densities, surface_data):
        """Internal method to update Minimizator based on densities and
        surface data.

        Parameters
        ----------
        densities : list
            List of density values.
        surface_data : object
            Surface data object.

        Returns
        -------
        tuple
            Tuple of active minimizator density and new density value.
        """
        if self.active_minimizator.value_name == 'PtP':
            values = surface_data.ptp_mean_per_segment

        if self.active_minimizator.value_name == 'LAT':
            values = -surface_data.lat_mean_per_segment

        segment_ind = self.active_minimizator.segment - 1
        value = values[segment_ind]
        density = densities[segment_ind]

        density_new = self.active_minimizator.update(density, value)

        print('SEGMENT: {}'.format(self.active_minimizator.segment))
        print('    {}: {:.3f}'.format(self.active_minimizator.value_name,
                                      value))
        print('DENSITY: {:.3f} --> {:.3f}'.format(density, density_new))

        return density, density_new

    def update(self, densities, surface_data):
        """Update Minimizators based on densities and surface data.

        Parameters
        ----------
        densities : list
            List of density values.
        surface_data : object
            Surface data object.

        Returns
        -------
        list
            Updated list of density values.
        """

        densities = densities.copy()

        while self.switch_counter <= self.max_switch_number:
            density, density_new = self._update(densities, surface_data)

            if abs(density_new - density) < self.density_step_tol:
                self.switch_minimizator()

            else:
                densities[self.active_minimizator.segment - 1] = density_new
                return densities

        return densities

    def switch_minimizator(self):
        """Switch the active Minimizator instance.
        """
        self.switch_counter += 1

        ind = self.switch_counter % len(self.minimizators)

        self.active_minimizator = self.minimizators[ind]

        print('SWITCHED TO: {}'.format(self.active_minimizator.segment))
        self.active_minimizator.reset()
