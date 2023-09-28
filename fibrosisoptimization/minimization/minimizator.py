from fibrosisoptimization.minimization.hybrid_iterator import HybridIterator


class Minimizator:
    def __init__(self, segment, value_name) -> None:
        self.segment = segment
        self.value_name = value_name
        self.value_tol = 0.01
        self.prev_density = 0
        self.density_step_tol = 0.01  # 1%
        self.reset_number = 0
        self.reset()

    def reset(self):
        self.reset_number += 1
        self.prev_density = 0
        self.iterator = HybridIterator()

    def update(self, density, value):
        if abs(value) <= self.value_tol:
            return density

        self.iterator.update(density, value)
        density_new = self.iterator.next()

        if abs(density_new - self.prev_density) <= self.density_step_tol:
            return density

        self.prev_density = density_new
        return density_new
