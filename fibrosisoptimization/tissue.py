import numpy as np


class Tissue:
    def __init__(self) -> None:
        pass

    @staticmethod
    def add_fibrosis(mesh, labels, density, active_labels):
        fibrosis = np.random.rand(*mesh.shape)

        for i, label in enumerate(active_labels):
            mask = labels == label
            mesh[mask] = 1
            mesh[mask & (fibrosis < density[i])] = 2

        return mesh
