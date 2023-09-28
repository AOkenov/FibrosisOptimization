from fibrosisoptimization.minimization.bracketing_iterator import BracketingIterator


class BisectionIterator(BracketingIterator):
    def __init__(self):
        BracketingIterator.__init__(self)

    def next(self):
        return 0.5 * (self.x_upper + self.x_lower)
