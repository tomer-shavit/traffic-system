import numpy as np
from Model.Direction import Direction
from Model.Reporter import Reporter
from Solvers.Solver import Solver


class BaseLineSolver(Solver):
    def __init__(self, n: int, m: int, t: int, reporter: Reporter):
        super().__init__(n, m, t, reporter)

    def solve(self) -> np.ndarray:
        """
        Assigns Direction.HORIZONTAL to even indices and Direction.VERTICAL to odd indices
        in an mxm matrix for t time steps using vectorized operations.

        Returns:
        - np.ndarray: A (t, n, m) array where each element is either Direction.HORIZONTAL or Direction.VERTICAL.
        """
        solution = np.empty((self.t, self.n, self.m), dtype=object)

        # Create a base (n, m) matrix for each direction
        horizontal_matrix = np.full((self.n, self.m), Direction.HORIZONTAL)
        vertical_matrix = np.full((self.n, self.m), Direction.VERTICAL)

        # Assign horizontal to even time steps and vertical to odd time steps
        solution[0::2] = horizontal_matrix
        solution[1::2] = vertical_matrix
        return solution