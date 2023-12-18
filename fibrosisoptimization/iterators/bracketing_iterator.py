from fibrosisoptimization.iterators.iterator import Iterator


class BracketingIterator(Iterator):
    """BracketingIterator class for iteratively updating and refining a
    bracketed range.

    Attributes
    ----------
    x_lower : float
        Lower boundary of the bracketed range.
    x_upper : float
        Upper boundary of the bracketed range.
    y_lower : float
        Value at the lower boundary.
    y_upper : float
        Value at the upper boundary.
    """

    def __init__(self):
        """Initialize a BracketingIterator object.
        """
        super().__init__()
        self.reset()

    def reset(self):
        """
        Set initial values assuming that for 0% fibrosis, mean residual
        is negative, and for 60% fibrosis, it is positive.
        """
        self.x_upper = 0.6
        self.x_lower = 0
        self.y_upper = 1
        self.y_lower = -1

    def update(self, x_new, y_new):
        """
        Update the bracketed range based on new values.

        Parameters
        ----------
        x_new : float
            New x-value.
        y_new : float
            New y-value.
        """
        if self.y_upper * y_new > 0:
            self.y_upper = y_new
            self.x_upper = x_new

        if self.y_lower * y_new > 0:
            self.y_lower = y_new
            self.x_lower = x_new

    def next(self):
        """Placeholder method for the next step or iteration.
        """
        pass
