import random

from Model import Coordinate
import numpy as np


class Reporter:
    def __init__(self):
        # Initialize separate data structures for each record type
        self.vehicle_counts = np.empty((0,), dtype=[
            ('junction_id', 'U20'),
            ('vertical_count', int),
            ('horizontal_count', int)
        ])

        self.wait_times = np.empty((0,), dtype=[
            ('avg_wait_time', float)
        ])

        self.vehicle_arrivals = np.empty((0,), dtype=[
            ('vehicle_id', 'U20'),
            ('junction_id', 'U20')
        ])

        self.all_cars_arrive_time = np.empty((0,), dtype=[
            ('time', float)
        ])

        self.not_reaching_cars = np.empty((0,), dtype=[
            ('cars_num', float)
        ])

        self.moving_cars_amount = np.empty((0,), dtype=[
            ('active_car', float)
        ])

        self.wait_time_punishment = np.empty((0,), dtype=[
            ('wait_punishment', float)
        ])

        self.best_solutions = np.empty((0,), dtype=[
            ('fitness', float),
            ('solution', object)
        ])

    def record_not_reaching_cars(self, cars_num):
        record = np.array([(
            cars_num
        )], dtype=self.not_reaching_cars.dtype)
        self.not_reaching_cars = np.append(self.not_reaching_cars, record)

    def record_wait_punishment(self, wait_punishment):
        record = np.array([(
            wait_punishment
        )], dtype=self.wait_time_punishment.dtype)
        self.wait_time_punishment = np.append(self.wait_time_punishment, record)

    def record_moving_cars(self, active_cars):
        record = np.array([(
            active_cars
        )], dtype=self.moving_cars_amount.dtype)
        self.moving_cars_amount = np.append(self.moving_cars_amount, record)

    def record_all_cars_arrive(self, time: float):
        record = np.array([(
            time
        )], dtype=self.all_cars_arrive_time.dtype)
        self.all_cars_arrive_time = np.append(self.all_cars_arrive_time, record)

    def record_avg_wait_time(self, avg_wait_time: float):
        record = np.array([(
            avg_wait_time
        )], dtype=self.wait_times.dtype)
        self.wait_times = np.append(self.wait_times, record)

    def record_generations_best_solutions(self, fitness: int, solution: np.ndarray):
        record = np.array([(
            fitness,
            solution
        )], dtype=self.best_solutions.dtype)
        self.best_solutions = np.append(self.best_solutions, record)

    def save_all_data(self, directory):
        # Save each array to a separate file in the specified directory
        id = random.randint(0, 1000)
        np.save(f'{directory}/wait_times_check{id}.npy', self.wait_times)
        np.save(f'{directory}/all_cars_arrive_time{id}.npy', self.all_cars_arrive_time)
        np.save(f'{directory}/not_reaching_cars{id}.npy', self.not_reaching_cars)
        np.save(f'{directory}/moving_cars_amount{id}.npy', self.moving_cars_amount)
        np.save(f'{directory}/wait_time_punishment{id}.npy', self.wait_time_punishment)
        np.save(f'{directory}/best_solutions{id}.npy', self.best_solutions, allow_pickle=True)

    def record_vehicle_arrival(self, vehicle_id: str, junction_id: Coordinate):
        record = np.array([(
            vehicle_id,
            f"{junction_id.x}, {junction_id.y}"
        )], dtype=self.vehicle_arrivals.dtype)
        self.vehicle_arrivals = np.append(self.vehicle_arrivals, record)

    def record_vehicle_count(self, junction_id: Coordinate, vertical_count: int, horizontal_count: int) -> None:
        record = np.array([(
            f"{junction_id.x}, {junction_id.y}",
            vertical_count,
            horizontal_count
        )], dtype=self.vehicle_counts.dtype)
        self.vehicle_counts = np.append(self.vehicle_counts, record)

    def report_training_results(self, score_history, best_score):
        pass

