import random
from itertools import product
from typing import List, Tuple
import numpy as np

from Model.City import City, Neighborhood
from Model.Coordinate import Coordinate
from Model.Direction import Direction
from PPO.Agent import Agent
from Model.Reporter import Reporter
from Solvers.Solver import Solver

# The value 4 because:
# 1) Num of cars that are waiting vertical.
# 2) Num of cars that are waiting Horizontal
# 3) Is it vertical highway (0/1)
# 4) Is it horizontal highway (0/1)
NUM_OF_REPRESENTATIONS = 4

NEIGHBORHOOD_N = 3
NEIGHBORHOOD_M = 3

# How many experiences are included in each mini-batch during the training process
# A batch size of 20 strikes a balance between stability and efficiency in learning.
# Smaller batch sizes can lead to noisier updates, while larger ones provide more stable
# gradients but require more memory.
BATCH_SIZE = 20

# The number of epochs in a machine learning context refers to the number of times the learning algorithm will
# pass through the entire training dataset. In each epoch, the model's parameters are updated based on the
# gradients computed from the mini-batches.
NUM_OF_EPOCHS = 5


NUM_OF_SIMULATIONS = 6
MAX_ITERATIONS = 100


class PPOSolver(Solver):
    """
    A solver that uses Proximal Policy Optimization (PPO) to optimize traffic light configurations
    within a city grid.

    Attributes:
        all_actions (List[np.ndarray]): A list of all possible traffic light configurations for neighborhoods.
        agent (Agent): The PPO agent that learns and selects actions.
    """

    def __init__(self, n: int, m: int, t: int, reporter: Reporter):
        """
        Initializes the PPOSolver with the grid dimensions, time steps, and reporter.
        Args:
            n (int): Number of rows in the city grid.
            m (int): Number of columns in the city grid.
            t (int): Number of time steps for the simulation.
            reporter (Reporter): An object for recording results and metrics.
        """
        super().__init__(n, m, t, reporter)
        self.all_actions = self.init_all_actions()
        self.agent = self.init_agent()

    def init_agent(self) -> Agent:
        return Agent(n_actions=len(self.all_actions),
                     batch_size=BATCH_SIZE,
                     n_epoch=NUM_OF_EPOCHS,
                     input_dims=self.get_state_dims())

    def get_state_dims(self) -> Tuple[int]:
        return NEIGHBORHOOD_M * NEIGHBORHOOD_M * NUM_OF_REPRESENTATIONS,

    def init_all_actions(self) -> List[np.ndarray]:
        """
        Initializes all possible traffic light configurations for neighborhoods.

        Returns:
            List[np.ndarray]: A list of all possible configurations.
        """
        possible_combinations = list(product([Direction.HORIZONTAL, Direction.VERTICAL],
                                             repeat=NEIGHBORHOOD_M * NEIGHBORHOOD_M))
        return [np.array(combination).reshape(NEIGHBORHOOD_N, NEIGHBORHOOD_M) for combination in possible_combinations]

    def solve(self, city: City) -> np.ndarray:
        """
        Solves the traffic light optimization problem for the given city over the time steps.

        Args:
            city (City): The city grid to optimize.

        Returns:
            np.ndarray: The optimal traffic light configuration for each time step.
        """
        counter = 0
        solution = []

        for t in range(self.t):
            actions_for_current_tick = []
            for i in range(self.n - NEIGHBORHOOD_N + 1):
                for j in range(self.m - NEIGHBORHOOD_M + 1):
                    top_left, top_right, bottom_left = self.build_neighborhood_coords(i, j)
                    neighborhood = city.get_neighborhood(top_left, top_right, bottom_left)
                    action, _, _ = self.agent.choose_action(neighborhood.get_state())
                    actions_for_current_tick.append(action)

            assignment = self.vote_on_assignment(actions_for_current_tick)
            solution.append(assignment)
            city.update_city(assignment)

        city.reset_city()
        return np.array(solution)

    def neighborhood_count(self):
        """
        Calculates the number of neighborhoods in the city grid.

        Returns:
            int: The number of neighborhoods.
        """
        return (self.n - NEIGHBORHOOD_N + 1) * (self.m - NEIGHBORHOOD_M + 1)

    def train(self, num_cities: int, num_cars: int) -> None:
        """
       Trains the PPO agent on a set of generated cities.

       Args:
           num_cities (int): The number of cities to generate for training.
           num_cars (int): The number of cars in each city.
       """
        cities = City.generate_cities(self.n, self.m, num_cars, num_cities)
        best_score = float('-inf')
        scores = []

        for index, city in enumerate(cities):
            total_score = 0
            print(f"starting to going over city number {index + 1} out of {len(cities)}")
            for t in range(self.t):
                if t < 8:
                    city.update_city(np.random.choice(list(Direction), size=(self.n, self.m)))
                    continue

                neighborhood = self.get_random_neighborhood(city)
                while neighborhood.original_num_of_cars == 0:
                    neighborhood = self.get_random_neighborhood(city)
                # city.print(np.random.choice(list(Direction), size=(self.n, self.m)))
                counter = 0
                total_reward = 0
                done = False
                while not done:
                    counter += 1
                    reward, done = self.neighborhood_iteration(neighborhood, counter)
                    total_reward += reward

                total_score += total_reward / counter

                self.agent.learn()
                assignment = np.random.choice(list(Direction), size=(self.n, self.m))
                city.update_city(assignment)

            print(f"The score for city {index} is: {total_score / self.t}")
            scores.append(total_score / self.t)
            city.reset_city()
            solution = self.solve(city)
            self.reporter.record_generations_best_solutions(self.evaluate_solution(solution, [city], report=True),
                                                            solution)
            if scores[-1] > best_score:
                self.reporter.save_all_data('../ReporterData/PPO')
                self.agent.save_models()
                best_score = scores[-1]

    def get_random_neighborhood(self, city):
        i = random.randint(0, self.n - NEIGHBORHOOD_N)
        j = random.randint(0, self.m - NEIGHBORHOOD_M)
        top_left, top_right, bottom_left = self.build_neighborhood_coords(i, j)
        return city.get_neighborhood(top_left, top_right, bottom_left)

    def neighborhood_iteration(self, neighborhood, iteration: int):
        """
        Executes one iteration of the PPO agent on a neighborhood.

        Args:
            neighborhood (Neighborhood): The neighborhood to optimize.
            iteration (int): The current iteration number.

        Returns:
            Tuple[int, bool]: The reward and a boolean indicating if the episode is done.
        """
        action, prob, val = self.agent.choose_action(neighborhood.get_state())
        reward, done = self.evaluate_neighborhood(action, neighborhood)
        if iteration == MAX_ITERATIONS:
            reward = 0
            done = True
        self.agent.remember(neighborhood.get_state(), action, prob, val, reward, done)

        return reward, done

    def build_neighborhood_coords(self, i, j):
        top_left = Coordinate(i, j)
        top_right = Coordinate(i, j + NEIGHBORHOOD_M - 1)
        bottom_left = Coordinate(i + NEIGHBORHOOD_N - 1, j)
        return top_left, top_right, bottom_left

    def vote_on_assignment(self, actions: List[int]) -> np.ndarray:
        """
       Aggregates votes from multiple actions to determine the final traffic light assignment.

       Args:
           actions (List[int]): A list of action indices selected by the agent.

       Returns:
           np.ndarray: The final traffic light assignment for the city grid.
       """
        votes = np.zeros((self.n, self.m, 2), dtype=int)

        for i in range(self.n - NEIGHBORHOOD_N + 1):
            for j in range(self.m - NEIGHBORHOOD_M + 1):
                action_idx = actions.pop(0)
                action = self.all_actions[action_idx]

                # Ensure action is 2D and iterate over its elements directly
                for ni in range(NEIGHBORHOOD_N):
                    for nj in range(NEIGHBORHOOD_M):
                        global_i = i + ni
                        global_j = j + nj

                        if action[ni, nj] == Direction.HORIZONTAL:
                            votes[global_i][global_j][0] += 1
                        else:
                            votes[global_i][global_j][1] += 1

        return self.build_assignments(votes)

    def build_assignments(self, votes: np.ndarray):
        assignment = np.empty((self.n, self.m), dtype=Direction)
        for i in range(self.n):
            for j in range(self.m):
                if votes[i][j][0] >= votes[i][j][1]:
                    assignment[i][j] = Direction.HORIZONTAL
                else:
                    assignment[i][j] = Direction.VERTICAL
        return assignment

    def evaluate_neighborhood(self, action: int, neighborhood: Neighborhood, report: bool = False) -> Tuple[int, bool]:
        """
        Evaluates the neighborhood's traffic performance based on a given action.

        Args:
            action (int): The action index chosen by the agent.
            neighborhood (Neighborhood): The neighborhood to evaluate.
            report (bool): Whether to generate a report on the evaluation.

        Returns:
            Tuple[int, bool]: The reward value and a boolean indicating if all cars have exited the neighborhood,
        """
        # TODO: implement diminishing effect when calculating the reward
        cur_action = action
        done = False
        for i in range(NUM_OF_SIMULATIONS):
            neighborhood.update_neighborhood(self.all_actions[cur_action])
            if i == 0:
                done = neighborhood.active_cars_amount() == 0
                neighborhood = Neighborhood.deep_copy(neighborhood)

            cur_action, _, _ = self.agent.choose_action(neighborhood.get_state())

        total_avg_wait_time = neighborhood.grid.get_total_avg_wait_time()
        not_reaching_cars = neighborhood.active_cars_amount()
        moving_cars_amount = neighborhood.grid.total_car_movements
        total_wait_time_punishment = self.get_wait_time_punishment(neighborhood)

        reward = self.evaluate(1, neighborhood.original_num_of_cars, not_reaching_cars, total_avg_wait_time,
                               moving_cars_amount, total_wait_time_punishment, report)
        reward = 4 if done else reward
        self.reporter.record_generations_best_solutions(reward, self.all_actions[action])

        return reward, done

    def get_wait_time_punishment(self, neighborhood: Neighborhood) -> float:
        wait_times = neighborhood.grid.get_all_junctions_wait_time()
        total_punishment = 0
        for row_wait_times in wait_times:
            for wait_time in row_wait_times:
                total_punishment += self.get_junction_wait_time_punishment(wait_time)

        return total_punishment
