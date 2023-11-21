from fibrosisoptimization.iterators.bracketing_iterator import (
    BracketingIterator
)


class BisectionIterator(BracketingIterator):
    """BisectionIterator class for iterative bisection within a
    bracketed range.

    Inherits from BracketingIterator.

    Methods
    -------
    next():
        Compute the midpoint for bisection.

    Attributes
    ----------
    Inherits x_upper, x_lower, y_upper, y_lower from BracketingIterator.
    """

    def __init__(self):
        """Initialize a BisectionIterator object.
        """
        BracketingIterator.__init__(self)

    def next(self):
        """Compute the midpoint for bisection.

        Returns
        -------
        float
            Description
        """
        return 0.5 * (self.x_upper + self.x_lower)
