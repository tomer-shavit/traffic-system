from itertools import product
from typing import List, Tuple
import numpy as np

from City import City, Neighborhood
from Coordinate import Coordinate
from Direction import Direction
from PPO.Agent import Agent
from Reporter import Reporter
from Solver import Solver

NEIGHBORHOOD_N = 3
NEIGHBORHOOD_M = 3
# If learning is too slow: Try increasing the batch size or the number of epochs.
# If learning is unstable: Try decreasing the batch size or the number of epochs.
# If you're facing memory constraints: Decrease the batch size.
BATCH_SIZE = 128
NUM_OF_EPOCHS = 5
NUM_OF_SIMULATIONS = 6


class PPOSolver(Solver):
    def __init__(self, n: int, m: int, t: int, reporter: Reporter):
        super().__init__(n, m, t, reporter)
        self.all_actions = self.init_all_actions()
        self.agent = self.init_agent()

    def init_agent(self) -> Agent:
        return Agent(n_actions=len(self.all_actions),
                     batch_size=BATCH_SIZE,
                     n_epoch=NUM_OF_EPOCHS,
                     input_dims=self.get_input_dims())

    def get_input_dims(self) -> Tuple[int]:
        return NEIGHBORHOOD_M * NEIGHBORHOOD_M,

    def init_all_actions(self) -> List[np.ndarray]:
        possible_combinations = list(product([Direction.HORIZONTAL, Direction.VERTICAL], repeat=9))
        return [np.array(combination) for combination in possible_combinations]

    def solve(self) -> np.ndarray:
        pass

    def train(self, num_cities: int, num_cars: int, time_limit: int) -> None:
        cities = City.generate_cities(self.n, self.m, num_cars, num_cities)
        score_history = []
        best_score = float('-inf')

        for city in cities:
            score = 0
            for t in range(time_limit):
                actions_for_current_tick = []
                for i in range(self.n - NEIGHBORHOOD_N + 1):
                    for j in range(self.m - NEIGHBORHOOD_M + 1):
                        score = self.neighborhood_iteration(actions_for_current_tick, city, i, j, score)

                assignment = self.vote_on_assignment(actions_for_current_tick)
                self.agent.learn()
                city.update_city(assignment)

            score_history.append(score)
            avg_score = np.mean(score_history[-100:])
            if avg_score > best_score:
                best_score = avg_score
                self.agent.save_models()

        # need to consider what we want to report
        self.reporter.report_training_results(score_history, best_score)

    def neighborhood_iteration(self, actions_for_current_tick, city, i, j, score):
        top_left, top_right, bottom_left = self.build_neighborhood_coords(i, j)
        neighborhood = city.get_neighborhood(top_left, top_right, bottom_left)
        action, prob, val = self.agent.choose_action(neighborhood.get_state())
        reward, done = self.evaluate_neighborhood(action, neighborhood)
        score += reward
        actions_for_current_tick.append(action)
        self.agent.remember(neighborhood.get_state(), action, prob, val, reward, done)

        return score

    def build_neighborhood_coords(self, i, j):
        top_left = Coordinate(i, j)
        top_right = Coordinate(i, j + NEIGHBORHOOD_M - 1)
        bottom_left = Coordinate(i + NEIGHBORHOOD_N - 1, j)
        return bottom_left, top_left, top_right

    def vote_on_assignment(self, actions: List[int]) -> np.ndarray:
        # Initialize the voting matrix with zeros, each cell has two counts: [horizontal_votes, vertical_votes]
        votes = np.zeros((self.n, self.m, 2), dtype=int)

        # Iterate over the sliding window positions
        for i in range(self.n - NEIGHBORHOOD_N + 1):
            for j in range(self.m - NEIGHBORHOOD_M + 1):
                action_idx = actions.pop(0)
                action = self.all_actions[action_idx]

                # Vote for each junction in the neighborhood
                for ni in range(NEIGHBORHOOD_N):
                    for nj in range(NEIGHBORHOOD_M):
                        global_i = i + ni
                        global_j = j + nj

                        if action[ni * NEIGHBORHOOD_M + nj] == Direction.HORIZONTAL:
                            votes[global_i][global_j][0] += 1
                        else:
                            votes[global_i][global_j][1] += 1

        # Create the assignment array based on majority votes
        assignment = np.empty((self.n, self.m), dtype=Direction)

        for i in range(self.n):
            for j in range(self.m):
                if votes[i][j][0] >= votes[i][j][1]:
                    assignment[i][j] = Direction.HORIZONTAL
                else:
                    assignment[i][j] = Direction.VERTICAL

        return assignment

    def evaluate_neighborhood(self, action: int, neighborhood: Neighborhood, report: bool = False) -> Tuple[int, bool]:
        for _ in range(NUM_OF_SIMULATIONS):
            neighborhood.update_neighborhood(self.all_actions[action])

        total_avg_wait_time = neighborhood.grid.get_total_avg_wait_time()
        not_reaching_cars = neighborhood.active_cars_amount()
        moving_cars_amount = neighborhood.grid.total_car_movements
        total_wait_time_punishment = self.get_wait_time_punishment(neighborhood)

        reward = self.evaluate(1, neighborhood.original_num_of_cars, not_reaching_cars, total_avg_wait_time,
                               moving_cars_amount, total_wait_time_punishment, report)
        done = neighborhood.original_num_of_cars == 0

        return reward, done

    def get_wait_time_punishment(self, neighborhood: Neighborhood) -> float:
        wait_times = neighborhood.grid.get_all_junctions_wait_time()
        total_punishment = 0
        for row_wait_times in wait_times:
            for wait_time in row_wait_times:
                total_punishment += self.get_junction_wait_time_punishment(wait_time)

        return total_punishment\
