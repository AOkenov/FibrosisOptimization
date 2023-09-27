import numpy as np
from fibropt.simulation.cardiac_model import CardiacModel
from fibropt.measure.fibrosis_density import FibrosisDensity
from fibropt.minimization.minimizator import Minimizator


class ApexStimulation:
    def __init__(self, path, experiment) -> None:
        self.path_data = path
        self.path_exp = self.path_data.joinpath(experiment)

    def run_simulation(self, iteration, t_max, prog_bar=False,
                       surfaces=['endo', 'epi']):
        cardiac_model = CardiacModel()
        cardiac_model.path = self.path_exp
        cardiac_model.load_fibers(self.path_data, 'fibers.npy')
        cardiac_model.load_electrodes(self.path_data)
        cardiac_model.load_stimul_coords(self.path_exp, 'stimuls_coords.npy')
        cardiac_model.load_stimul_voltage(self.path_data,
                                          'action_potential_0015_1.npy')

        cardiac_model.run(str(iteration), t_max=t_max, memory_save=False,
                          prog_bar=prog_bar, surfaces=surfaces)

    def init_minimizator(self, labels, value_name='Amplitude'):
        minimizators = []
        for label in labels:
            minimizator = Minimizator(label, value_name)
            minimizator.reset()
            minimizators.append(minimizator)
        return minimizators

    def next_density(self, density_prev, amplitudes_error, minimizators):
        density_next = []
        for i, minimizator in enumerate(minimizators):
            density_next.append(minimizator.update(density_prev[i],
                                                   amplitudes_error[i]))
        return density_next
