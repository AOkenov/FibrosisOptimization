import numpy as np
import pyvista as pv


class InteractivePlotter(pv.Plotter):
    """InteractivePlotter class for visualizing scalar fields on a grid.

    This class extends pyvista.Plotter to facilitate the visualization of
    scalar fields on a grid.

    Attributes:
        grid (pyvista.UniformGrid): Uniform grid for visualization.
        scalar_idx (numpy.ndarray): Sorted indexes of 'F' order array for
            future scalar values.
    """

    def __init__(self):
        """Initialize an InteractivePlotter object."""
        super().__init__()

    def build_grid(self, coords, shape=(269, 279, 240)):
        """Build the uniform grid for visualization based on coordinates.

        Args:
            coords (numpy.ndarray): Coordinates for creating the scalar mask.
            shape (tuple, optional): Shape of the grid.
                Defaults to (269, 279, 240).
        """
        scalar_mask = np.zeros(shape, dtype=float)
        scalar_mask[tuple(coords.T)] = 1.

        grid = pv.UniformGrid()
        grid.dimensions = np.array(shape) + 1
        grid.spacing = (1, 1, 1)
        grid.cell_data['scalar_mask'] = scalar_mask.flatten(order='F')
        self.grid = grid.threshold([0.5, 1])

        # make sorted indexes of 'F' order array for future scalar values
        f_idx = np.ravel_multi_index(coords.T[::-1], shape[::-1])
        self.scalar_idx = np.argsort(f_idx)

    def add_grid(self, clim=[0, 255], cmap='viridis', opacity=1):
        """Add the grid to the plotter.

        Args:
            clim (list, optional): Color map limits. Defaults to [0, 255].
            cmap (str, optional): Color map name. Defaults to 'viridis'.
            opacity (float, optional): Opacity level. Defaults to 1.
        """
        self.add_mesh(self.grid, opacity=opacity, name='grid_base', cmap=cmap,
                      clim=clim)

    def add_scalar(self, scalar, name='Scalar'):
        """Add scalar values to the grid.

        Args:
            scalar (numpy.ndarray): Scalar values to be added.
            name (str, optional): Name of the scalar field.
                Defaults to 'Scalar'.
        """
        self.grid.cell_data[name] = scalar[self.scalar_idx]
        self.grid.set_active_scalars(name)

    def update_scalar(self, scalar):
        """Update the scalar values on the grid.

        Args:
            scalar (numpy.ndarray): Updated scalar values.
        """
        self.update_scalars(scalar[self.scalar_idx], self.grid)
        self.update()
        # plotter.show(interactive_update=interactive_update)
        # return plotter
