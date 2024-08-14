from itertools import product

import numpy as np

from Direction import Direction
from Reporter import Reporter
from Solver import Solver


class PPOSolver(Solver):
    def __init__(self, n: int, m: int, t: int, reporter: Reporter):
        super().__init__(n, m, t, reporter)
        self.all_actions = []

        self.init_all_actions()

    def init_all_actions(self):
        possible_combinations = list(product([Direction.HORIZONTAL, Direction.VERTICAL], repeat=9))
        self.all_actions = [np.array(combination) for combination in possible_combinations]

