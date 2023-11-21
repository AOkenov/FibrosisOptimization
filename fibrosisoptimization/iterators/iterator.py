

class Iterator:
    """Base class for iterators.

    This serves as the base class for specific iterator implementations.

    Methods
    -------
    __init__():
        Initialize an Iterator object.

    update(x_new, y_new):
        Update the iterator with new values.

    next():
        Obtain the next value or approximation.

    Attributes
    ----------
    This base class does not contain specific attributes.
    """

    def __init__(self):
        """Initialize an Iterator object.
        """
        pass

    def update(self, x_new, y_new):
        """Update the iterator with new values.

        Parameters
        ----------
        x_new : Any
            New x-value or parameter.
        y_new : Any
            New y-value or function evaluation.
        """
        pass

    def next(self):
        """Get the next value or approximation.

        No Longer Returned
        ------------------
        Any
        Next value or approximation based on the iterator's method.
        """
        pass
