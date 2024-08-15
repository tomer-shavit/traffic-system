from itertools import product
from typing import List, Tuple

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

    def solve(self) -> np.ndarray:
        pass

    def train(self) -> None:
        pass

    def vote_on_assignment(self, actions: List[int]) -> np.ndarray:
        pass

    def evaluate(self, action: int) -> Tuple[int, bool]:
        pass

#def evaluate(self):
    # jkkLL

# def train():
# actions_for_current_tick = []
# set cities
# for city in cities:
    # for t in range(T):
        # for i in something():
            # for j in something():
                # sub = city.get_neighborhood(coor, coor, coor)
                # action, prob, val = self.agent.choose_aciton(sub.get_state())
                # reward, done = self.evaluate(action)
                # score += reward
                # actions_for_current_tick.append(action)
                # agent.remember(sub.state(), action, prob, val reward, done)

        # assignment = vote_on_assignment(actions_for_current_tick)
        # agent.learn()
        # city.update_city(assignment)

    # score_history.append(score)
    # avg_score = np.mean(score_history)
    # if avg_score > best_score:
    # best_score = avg_score
    # agent.save_models()


