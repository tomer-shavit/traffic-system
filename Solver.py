from abc import abstractmethod, ABC

import numpy as np
from typing import List
from City import City
from Reporter import Reporter

NOT_REACHING_DEST_PENALTY = 10


class Solver(ABC):
    def __init__(self, n: int, m: int, t: int, reporter: Reporter,):
        """
        Initializes the Solver with the necessary grid parameters.

        Parameters:
        - n (int): The number of rows in the city grid.
        - m (int): The number of columns in the city grid.
        - t (int): The number of time steps (ticks) to consider in each solution.
        """
        self.n = n
        self.m = m
        self.t = t
        self.reporter = reporter

    @abstractmethod
    def solve(self, *args, **kwargs):
        """
        Abstract method to be implemented by subclasses for solving the optimization problem.
        """
        pass

    def evaluate_solution(self, solution: np.ndarray, cities: List[City], debug: bool = False) -> float:
        """
        Evaluates a solution by simulating it across multiple city scenarios and calculating the average waiting
        time for cars.

        Parameters:
        - solution (np.ndarray): The solution to be evaluated.
        - cities (List[City]): A list of City objects representing different traffic scenarios.

        Returns:
        - float: The average waiting time for cars, or infinity if not all cars reach their destinations.
        """
        total_avg_wait_time = 0
        waiting_cars_penalty = 0
        for city in cities:
            for t in range(self.t):
                city.update_city(solution[t], debug)

            total_avg_wait_time += city.get_current_avg_wait_time()
            waiting_cars_penalty += city.driving_cars_amount() * NOT_REACHING_DEST_PENALTY

            city.reset_city()

        return self.avg_wait_time(len(cities), total_avg_wait_time) + \
            self.get_driving_penalty_avg(cities, waiting_cars_penalty)

    def get_driving_penalty_avg(self, cities, waiting_cars_penalty):
        return waiting_cars_penalty / len(cities)

    def avg_wait_time(self, cities_amount: int, total_avg_wait_time: float):
        return total_avg_wait_time / cities_amount
