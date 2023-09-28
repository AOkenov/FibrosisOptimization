class BracketingIterator:
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        '''
        Set initial values assuming that for 0% fibroris mean residual is negative
        and for 60% fibroris is positive
        '''
        self.x_upper = 0.6
        self.x_lower = 0
        self.y_upper = 1
        self.y_lower = -1

    def update(self, x_new, y_new):
        if self.y_upper * y_new > 0:
            self.y_upper = y_new
            self.x_upper = x_new

        if self.y_lower * y_new > 0:
            self.y_lower = y_new
            self.x_lower = x_new

        # print('x_lower {:.2f} | y_lower {:.2f} | x_upper {:.2f} | y_upper {:.2f}'.format(
        #     self.x_lower, self.y_lower, self.x_upper, self.y_upper
        # ))

    def next(self):
        return
