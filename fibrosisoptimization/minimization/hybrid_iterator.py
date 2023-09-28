from fibrosisoptimization.minimization.bisection_iterator import BisectionIterator
from fibrosisoptimization.minimization.false_position_iterator import FalsePositionIterator


class HybridIterator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.iterator = BisectionIterator()
        self.iterator.reset()
        self.y_prev = 0
        self.it = 0

    def switch_iterator(self):
        iterator = FalsePositionIterator()
        iterator.reset_from(self.iterator)
        self.iterator = iterator

    def update(self, x_new, y_new):
        self.iterator.update(x_new, y_new)

        sign_changed = (self.it > 0) and ((self.y_prev * y_new) < 0)

        if sign_changed and isinstance(self.iterator, BisectionIterator):
            print('Switch at {}'.format(x_new))
            self.switch_iterator()

        self.y_prev = y_new
        self.it += 1

    def next(self):
        return self.iterator.next()
