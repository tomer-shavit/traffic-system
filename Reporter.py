import Coordinate
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
            ('junction_id', 'U20'),
            ('avg_wait_time', float)
        ])

        self.vehicle_arrivals = np.empty((0,), dtype=[
            ('vehicle_id', 'U20'),
            ('junction_id', 'U20')
        ])

        self.all_cars_arrive_time = np.empty((0,), dtype=[
            ('time', float)
        ])

        self.best_solutions = np.empty((0,), dtype=[
            ('fitness', float),
            ('solution', object)
        ])

    def record_vehicle_count(self, junction_id: Coordinate, vertical_count: int, horizontal_count: int) -> None:
        record = np.array([(
            f"{junction_id.x}, {junction_id.y}",
            vertical_count,
            horizontal_count
        )], dtype=self.vehicle_counts.dtype)
        self.vehicle_counts = np.append(self.vehicle_counts, record)

    def record_all_cars_arrive(self, time: float):
        record = np.array([(
            time
        )], dtype=self.all_cars_arrive_time.dtype)
        self.all_cars_arrive_time = np.append(self.all_cars_arrive_time, record)

    def record_avg_wait_time(self, junction_id: Coordinate, avg_wait_time: float):
        record = np.array([(
            f"{junction_id.x}, {junction_id.y}",
            avg_wait_time
        )], dtype=self.wait_times.dtype)
        self.wait_times = np.append(self.wait_times, record)

    def record_vehicle_arrival(self, vehicle_id: str, junction_id: Coordinate):
        record = np.array([(
            vehicle_id,
            f"{junction_id.x}, {junction_id.y}"
        )], dtype=self.vehicle_arrivals.dtype)
        self.vehicle_arrivals = np.append(self.vehicle_arrivals, record)

    def record_generations_best_solutions(self, fitness: int, solution: np.ndarray):
        record = np.array([(
            fitness,
            solution
        )], dtype=self.best_solutions.dtype)
        self.best_solutions = np.append(self.best_solutions, record)

    # Getters for each record type
    def get_vehicle_counts(self) -> np.ndarray:
        return self.vehicle_counts

    def get_wait_times(self) -> np.ndarray:
        return self.wait_times

    def get_vehicle_arrivals(self) -> np.ndarray:
        return self.vehicle_arrivals

    def get_best_solutions(self) -> np.ndarray:
        return self.best_solutions

    def get_arrival_times(self) -> np.ndarray:
        return self.all_cars_arrive_time
