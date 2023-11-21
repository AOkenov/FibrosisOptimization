from fibrosisoptimization.iterators import HybridIterator


class Minimizator:
    """Minimizator class for optimization.

    This class handles the optimization process using a HybridIterator.

    Args:
        segment (str): Segment information.
        value_name (str): Name of the value.

    Attributes:
        segment (str): Segment information.
        value_name (str): Name of the value.
        value_tol (float): Tolerance value for the specified value.
        prev_density (float): Previous density value.
        density_step_tol (float): Tolerance for the density step change.
        reset_number (int): Counter for reset occurrences.
        iterator (HybridIterator): Iterator for optimization.
    """

    def __init__(self, segment, value_name):
        """Initialize a Minimizator object.

        Args:
            segment (str): Segment information.
            value_name (str): Name of the value.
        """
        self.segment = segment
        self.value_name = value_name
        self.value_tol = 0.01
        self.prev_density = 0
        self.density_step_tol = 0.01  # 1%
        self.reset()

    def reset(self):
        """Reset the optimization parameters."""
        self.prev_density = 0
        self.iterator = HybridIterator()

    def update(self, density, value):
        """Update the optimization process based on density and value.

        Args:
            density (float): Current density value.
            value (float): Current value.

        Returns:
            float: Updated density value based on the optimization process.
        """
        if abs(value) <= self.value_tol:
            return density

        self.iterator.update(density, value)

        density_new = self.iterator.next()

        # print('NEW DENSITY: {} <-- {}'.format(density_new, self.prev_density))

        if abs(density_new - self.prev_density) <= self.density_step_tol:
            return density

        self.prev_density = density_new
        return density_new
