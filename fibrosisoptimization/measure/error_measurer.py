class ErrorMeasurer:
    def __init__(self, value_updater):
        self.value_updater = value_updater
        self.target = self.value_updater.add_record(0)
        self.base = self.value_updater.add_record(1)

    def compute(self, iteration):
        value = self.value_updater.add_record(iteration)
        return (self.target - value) / self.base