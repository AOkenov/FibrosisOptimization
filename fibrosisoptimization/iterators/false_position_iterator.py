from fibrosisoptimization.iterators.bracketing_iterator import (
    BracketingIterator
)


class FalsePositionIterator(BracketingIterator):
    """FalsePositionIterator class for iterative False Position method within
    a bracketed range.

    Inherits from BracketingIterator.

    Methods
    -------
    reset():
        Reset the iterator to initial values.

    reset_from(iterator):
        Reset the iterator from another iterator's values.

    update(x_new, y_new):
        Update the bracketed range with new values.

    modified(x_new, y_new):
        Modify the bracketed range based on specific conditions.

    next():
        Compute the next approximation based on False Position method.

    Attributes
    ----------
    it_lower : int
        Count of iterations for lower boundary conditions.
    it_upper : int
        Count of iterations for upper boundary conditions.
    x_lower : float
        Lower bound of x-value
    x_upper : float
        Upper bound of x-value
    y_lower : float
        Lower bound of y-value
    y_upper : float
        Upper bound of y-value
    """

    def __init__(self):
        """Initialize a FalsePositionIterator object.
        """
        BracketingIterator.__init__(self)
        self.reset()

    def reset(self):
        """Reset the iterator to initial values.
        """
        super().reset()
        self.it_upper = 0
        self.it_lower = 0

    def reset_from(self, iterator):
        """Reset the iterator from another iterator's values.

        Parameters
        ----------
        iterator : BracketingIterator
            Another bracketing iterator object.
        """
        self.reset()
        self.x_lower = iterator.x_lower
        self.y_lower = iterator.y_lower
        self.x_upper = iterator.x_upper
        self.y_upper = iterator.y_upper

    def update(self, x_new, y_new):
        """Update the bracketed range with new values.

        Parameters
        ----------
        x_new : float
            New x-value.
        y_new : float
            New y-value.
        """
        super().update(x_new, y_new)

    def modified(self, x_new, y_new):
        """Modify the bracketed range based on specific conditions.

        Parameters
        ----------
        x_new : float
            New x-value.
        y_new : float
            New y-value.
        """
        if self.y_upper * y_new > 0:
            self.it_upper = 0
            self.it_lower += 1
            if self.it_lower > 1:
                self.y_lower /= 2

        if self.y_lower * y_new > 0:
            self.it_lower = 0
            self.it_upper += 1
            if self.it_upper > 1:
                self.y_upper /= 2

    def next(self):
        """Compute the next approximation based on False Position method.

        Returns
        -------
        float
            Next approximation using False Position method.
        """
        return self.x_upper - self.y_upper * ((self.x_lower - self.x_upper)
                                              / (self.y_lower - self.y_upper))
