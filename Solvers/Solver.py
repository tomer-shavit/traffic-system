from abc import abstractmethod, ABC
import numpy as np
from typing import List, Dict
from Model.City import City
from Model.Reporter import Reporter


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
        - report (bool): Whether to record evaluation metrics in the Reporter.

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

            print(f"avg wait time is: {city.get_current_avg_wait_time()}")
            print(f"Num of active cars is: {city.active_cars_amount()}")
            self.reporter.record_all_cars_arrive(city.all_cars_arrived_time)
            city.reset_city()

        return self.evaluate(len(cities),
                             len(cities[0].cars),
                             not_reaching_cars,
                             total_avg_wait_time,
                             moving_cars_amount,
                             total_wait_time_punishment,
                             report)

    def evaluate(self, cities_amount: int,
                 cars_amount: int,
                 not_reaching_cars,
                 total_avg_wait_time,
                 moving_cars_amount,
                 total_wait_time_punishment,
                 report):
        """
        Normalizes and combines the evaluation metrics into a single score.

        Parameters:
        - cities_amount (int): The number of cities evaluated.
        - cars_amount (int): The number of cars per city.
        - not_reaching_cars (int): The total number of cars that did not reach their destination.
        - total_avg_wait_time (float): The total average wait time across all cities.
        - moving_cars_amount (int): The total number of car movements across all cities.
        - total_wait_time_punishment (float): The total punishment score for excessive wait times across all cities.
        - report (bool): Whether to record evaluation metrics in the Reporter.

        Returns:
        - float: The combined evaluation score.
        """
        score_not_reaching = self.normalize_not_reaching_cars(not_reaching_cars,
                                                              cities_amount, cars_amount, report)
        score_avg_wait_time = self.normalize_avg_wait_time(total_avg_wait_time,
                                                           cities_amount, cars_amount, report)
        score_moving_cars = self.normalize_moving_cars_amount(moving_cars_amount,
                                                              cities_amount, cars_amount, report)
        score_wait_time_punishment = self.normalize_wait_time_punishment(total_wait_time_punishment,
                                                                         cities_amount, cars_amount, report)

        return (score_not_reaching +
                score_avg_wait_time +
                score_moving_cars +
                score_wait_time_punishment)

    def get_wait_time_punishment(self, city: City) -> float:
        """
        Calculates the total punishment for excessive wait times across all junctions in a city.

        Parameters:
        - city (City): The city object containing junctions with wait times.

        Returns:
        - float: The total punishment score for the city.
        """
        wait_times = city.get_all_junctions_wait_time()
        total_punishment = 0
        for row_wait_times in wait_times:
            for wait_time in row_wait_times:
                total_punishment += self.get_junction_wait_time_punishment(wait_time)
        return total_punishment

    def get_junction_wait_time_punishment(self, wait_time: Dict[str, int]) -> float:
        """
        Calculates the punishment for wait times at a single junction.

        Parameters:
        - wait_time (Dict[str, int]): A dictionary of wait times for each car at the junction.

        Returns:
        - float: The punishment score for the junction.
        """
        total = 0
        for time in wait_time.values():
            total += time ** 2
        return total

    def normalize_not_reaching_cars(self, not_reaching_cars,
                                    cities_amount: int, cars_amount: int, report: bool) -> float:
        if report:
            self.reporter.record_not_reaching_cars(not_reaching_cars / cities_amount)
        if cars_amount == 0:
            return 1

        max_cars = cars_amount * cities_amount
        normalized_not_reaching_cars = not_reaching_cars / max_cars
        return 1 / (1 + normalized_not_reaching_cars)

    def normalize_avg_wait_time(self, total_avg_wait_time,
                                cities_amount: int, cars_amount: int, report: bool) -> float:
        if report:
            self.reporter.record_avg_wait_time(total_avg_wait_time / cities_amount)
        if cars_amount == 0:
            return 1

        max_waiting_cars = self.t * cars_amount * cities_amount / (self.m * self.n)
        normalized_total_avg_wait_time = total_avg_wait_time / max_waiting_cars
        return 1 / (1 + normalized_total_avg_wait_time)

    def normalize_moving_cars_amount(self, moving_cars_amount,
                                     cities_amount: int, cars_amount: int, report: bool) -> float:
        if report:
            self.reporter.record_moving_cars(moving_cars_amount / cities_amount)
        if cars_amount == 0:
            return 1

        max_moving_cars = cities_amount * cars_amount * self.t
        return moving_cars_amount / max_moving_cars

    def normalize_wait_time_punishment(self, wait_time_punishment,
                                       cities_amount: int, cars_amount: int, report: bool) -> float:
        if report:
            self.reporter.record_wait_punishment(wait_time_punishment / cities_amount)
        if cars_amount == 0:
            return 1

        max_punishment = (self.t * cars_amount * cities_amount) ** 2
        normalized_total_wait_time_punishment = wait_time_punishment / max_punishment
        return 1 / (1 + normalized_total_wait_time_punishment)
