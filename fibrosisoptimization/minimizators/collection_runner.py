class CollectionRunner:
    def __init__(self):
        self.minimizators = []

    def update(self, densities, surface_data):
        for minimizator in self.minimizators:
            densities = minimizator.update(densities, surface_data)

        return densities
