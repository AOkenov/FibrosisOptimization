from fibrosisoptimization.iterators.iterator import Iterator
from fibrosisoptimization.iterators.bisection_iterator import (
    BisectionIterator
)
from fibrosisoptimization.iterators.false_position_iterator import (
    FalsePositionIterator
)


class HybridIterator(Iterator):
    """HybridIterator class for iterative hybrid root-finding method.

    Methods
    -------
    reset():
        Reset the iterator to initial values.

    switch_iterator():
        Switch the iterator between Bisection and False Position methods.

    update(x_new, y_new):
        Update the iterator with new values and handle switching
        conditions.

    next():
        Get the next approximation based on the current iterator method.

    Attributes
    ----------
    it : int
        Iteration count.
    iterator : BisectionIterator or FalsePositionIterator
        Iterator object for root finding.
    y_prev : float
        revious y-value for comparison.
    """

    def __init__(self):
        """Initialize a HybridIterator object.
        """
        super().__init__()
        self.reset()

    def reset(self):
        """Reset the iterator to initial values.
        """
        self.iterator = BisectionIterator()
        self.iterator.reset()
        self.y_prev = 0
        self.it = 0

    def switch_iterator(self):
        """Switch the iterator between Bisection and False Position methods.
        """
        iterator = FalsePositionIterator()
        iterator.reset_from(self.iterator)
        self.iterator = iterator

    def update(self, x_new, y_new):
        """Update the iterator with new values and handle switching conditions.

        Parameters
        ----------
        x_new : float
            New x-value.
        y_new : float
            New y-value.
        """
        self.iterator.update(x_new, y_new)

        sign_changed = (self.it > 0) and ((self.y_prev * y_new) < 0)

        if sign_changed and isinstance(self.iterator, BisectionIterator):
            print('Switch iterator at DENSITY: {:.3f}'.format(x_new))
            self.switch_iterator()

        self.y_prev = y_new
        self.it += 1

    def next(self):
        """Get the next approximation based on the current iterator method.

        Returns
        -------
        float
            Next approximation using the current iterator method.
        """
        return self.iterator.next()
