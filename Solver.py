from abc import abstractmethod, ABC
import numpy as np
from typing import List, Dict
from City import City
from Reporter import Reporter

NOT_REACHING = 1
ALL_CARS_ARRIVE_TIME = 1
AVG_WAIT_TIME = 1
MOVING_CARS_AMOUNT = 1
WAIT_TIME = 1


class Solver(ABC):
    def __init__(self, n: int, m: int, t: int, reporter: Reporter):
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

    def evaluate_solution(self, solution: np.ndarray, cities: List[City], report: bool = False) -> float:
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
        not_reaching_cars = 0
        moving_cars_amount = 0
        total_wait_time_punishment = 0
        for city in cities:
            for t in range(self.t):
                city.update_city(solution[t], False)

            total_avg_wait_time += city.get_current_avg_wait_time()
            not_reaching_cars += city.active_cars_amount()
            moving_cars_amount += city.get_total_cars_movements()
            total_wait_time_punishment += self.get_wait_time_punishment(city)

            self.reporter.record_all_cars_arrive(city.all_cars_arrived_time)
            city.reset_city()

        score_not_reaching = self.normalize_not_reaching_cars(not_reaching_cars, cities, report)
        score_avg_wait_time = self.normalize_avg_wait_time(total_avg_wait_time, cities, report)
        score_moving_cars = self.normalize_moving_cars_amount(moving_cars_amount, cities, report)
        score_wait_time_punishment = self.normalize_wait_time_punishment(total_wait_time_punishment, cities, report)

        return (score_not_reaching * NOT_REACHING +
                score_avg_wait_time * AVG_WAIT_TIME +
                score_moving_cars * MOVING_CARS_AMOUNT +
                score_wait_time_punishment * WAIT_TIME)

    def get_wait_time_punishment(self, city: City) -> float:
        wait_times = city.get_all_junctions_wait_time()
        total_punishment = 0
        for row_wait_times in wait_times:
            for wait_time in row_wait_times:
                total_punishment += self.get_junction_wait_time_punishment(wait_time)
        return total_punishment

    def get_junction_wait_time_punishment(self, wait_time: Dict[str, int]) -> float:
        total = 0
        for time in wait_time.values():
            total += time ** 2
        return total

    def normalize_not_reaching_cars(self, not_reaching_cars, cities: List[City], report: bool) -> float:
        if report:
            self.reporter.record_not_reaching_cars(not_reaching_cars / len(cities))
        max_cars = len(cities[0].cars) * len(cities)
        normalized_not_reaching_cars = not_reaching_cars / max_cars
        return 1 / (1 + normalized_not_reaching_cars)

    def normalize_avg_wait_time(self, total_avg_wait_time, cities: List[City], report: bool) -> float:
        if report:
            self.reporter.record_avg_wait_time(total_avg_wait_time / len(cities))
        max_waiting_cars = self.t * len(cities[0].cars) * len(cities) / (self.m * self.n)
        normalized_total_avg_wait_time = total_avg_wait_time / max_waiting_cars
        return 1 / (1 + normalized_total_avg_wait_time)

    def normalize_moving_cars_amount(self, moving_cars_amount, cities: List[City], report: bool) -> float:
        if report:
            self.reporter.record_moving_cars(moving_cars_amount / len(cities))
        max_moving_cars = len(cities) * len(cities[0].cars) * self.t
        return moving_cars_amount / max_moving_cars

    def normalize_wait_time_punishment(self, wait_time_punishment, cities: List[City], report: bool) -> float:
        if report:
            self.reporter.record_wait_punishment(wait_time_punishment / len(cities))
        max_punishment = (self.t * len(cities[0].cars) * len(cities)) ** 2
        normalized_total_wait_time_punishment = wait_time_punishment / max_punishment
        return 1 / (1 + normalized_total_wait_time_punishment)
