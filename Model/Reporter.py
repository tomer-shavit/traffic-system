import random

import numpy as np


class Reporter:
    def __init__(self):
        # Initialize separate data structures for each record type

        self.wait_times = np.empty((0,), dtype=[
            ('avg_wait_time', float)
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

    def record_avg_wait_time(self, avg_wait_time: float):
        record = np.array([(
            avg_wait_time
        )], dtype=self.wait_times.dtype)
        self.wait_times = np.append(self.wait_times, record)

    def record_best_solutions_scores(self, fitness: float, solution: np.ndarray):
        record = np.array([(
            fitness,
            solution
        )], dtype=self.best_solutions.dtype)
        self.best_solutions = np.append(self.best_solutions, record)

    def save_all_data(self, directory, experiment_id):
        # Save each array to a separate file in the specified directory
        np.save(f'{directory}/wait_times_check_{experiment_id}.npy', self.wait_times)
        np.save(f'{directory}/all_cars_arrive_time_{experiment_id}.npy', self.all_cars_arrive_time)
        np.save(f'{directory}/not_reaching_cars_{experiment_id}.npy', self.not_reaching_cars)
        np.save(f'{directory}/moving_cars_amount_{experiment_id}.npy', self.moving_cars_amount)
        np.save(f'{directory}/wait_time_punishment_{experiment_id}.npy', self.wait_time_punishment)
        np.save(f'{directory}/best_solutions_{experiment_id}.npy', self.best_solutions, allow_pickle=True)
