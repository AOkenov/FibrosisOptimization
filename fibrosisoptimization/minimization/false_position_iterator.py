from fibrosisoptimization.minimization.bracketing_iterator import BracketingIterator


class FalsePositionIterator(BracketingIterator):
    def __init__(self):
        BracketingIterator.__init__(self)
        self.reset()

    def reset(self):
        super().reset()
        self.it_upper = 0
        self.it_lower = 0

    def reset_from(self, iterator):
        self.reset()
        self.x_lower = iterator.x_lower
        self.y_lower = iterator.y_lower
        self.x_upper = iterator.x_upper
        self.y_upper = iterator.y_upper

    def update(self, x_new, y_new):
        super().update(x_new, y_new)

        # if self.y_upper * y_new > 0:
        #     self.it_upper = 0
        #     self.it_lower += 1
        #     if self.it_lower > 1:
        #         self.y_lower /= 2

        # if self.y_lower * y_new > 0:
        #     self.it_lower = 0
        #     self.it_upper += 1
        #     if self.it_upper > 1:
        #         self.y_upper /= 2

    def next(self):
        return self.x_upper - self.y_upper * ((self.x_lower - self.x_upper) / 
                                              (self.y_lower - self.y_upper))
