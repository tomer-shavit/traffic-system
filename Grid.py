from typing import List, Tuple, Dict
from Junction import Junction
from TrafficLight import TrafficLight, Direction
from Car import Car


class Grid:
    def __init__(self, traffic_lights: List[List[TrafficLight]]):
        self.n = len(traffic_lights)
        self.m = len(traffic_lights[0])
        self.junctions: List[List[Junction]] = [
            [Junction(traffic_lights[i][j]) for j in range(self.m)] for i in range(self.n)
        ]

    def print(self) -> None:
        """Print a visual representation of the grid."""
        for i in range(self.n):
            # Print horizontal junctions
            for j in range(self.m):
                junction = self.junctions[i][j]
                vertical_cars = sum(
                    1 for car in junction.cars.values() if car.current_direction() == Direction.VERTICAL)
                horizontal_cars = sum(
                    1 for car in junction.cars.values() if car.current_direction() == Direction.HORIZONTAL)
                light_direction = 'V' if junction.traffic_light.get_current_direction() == Direction.VERTICAL else 'H'
                print(f"[D:{light_direction},V:{vertical_cars:2d},H:{horizontal_cars:2d}]", end="")
                if j < self.m - 1:
                    print(" -- ", end="")
            print()  # New line after each row of junctions

            # Print vertical connections, if not the last row
            if i < self.n - 1:
                for j in range(self.m):
                    print("        |         ", end="")
                    if j < self.m - 1:
                        print("    ", end="")
                print()  # New line after vertical connections

    def update_grid(self) -> None:
        """Update the state of all junctions in the grid and move cars."""
        cars_to_move = []  # List to store cars that need to be moved

        # First, update all junctions and collect cars that need to be moved
        for i in range(self.n):
            for j in range(self.m):
                junction = self.junctions[i][j]
                direction, moving_cars = junction.update_junction()

                for car in moving_cars:
                    if direction == Direction.VERTICAL and i < self.n - 1:
                        cars_to_move.append((car, i, j, i + 1, j))  # Move down
                    elif direction == Direction.HORIZONTAL and j < self.m - 1:
                        cars_to_move.append((car, i, j, i, j + 1))  # Move right

        # Now move the cars
        for car, old_i, old_j, new_i, new_j in cars_to_move:
            self.junctions[old_i][old_j].remove_car(car)
            self.junctions[new_i][new_j].add_car(car)

    def get_total_avg_wait_time(self) -> float:
        """Calculate the average wait time across all unique cars in all junctions."""
        total_wait_time = 0
        unique_cars = set()

        for row in self.junctions:
            for junction in row:
                total_wait_time += sum(junction.cars_wait_time.values())
                unique_cars.update(junction.cars_wait_time.keys())

        if not unique_cars:
            return 0.0

        return total_wait_time / len(unique_cars)

    def add_car_to_junction(self, car: Car, i: int, j: int) -> None:
        """Add a car to a specific junction."""
        if 0 <= i < self.n and 0 <= j < self.m:
            self.junctions[i][j].add_car(car)
        else:
            print(f"Invalid junction coordinates: ({i}, {j})")

    def get_junction(self, i: int, j: int) -> Junction:
        """Get a specific junction from the grid."""
        if 0 <= i < self.n and 0 <= j < self.m:
            return self.junctions[i][j]
        else:
            raise IndexError(f"Junction coordinates out of range: ({i}, {j})")

    def get_grid_state(self) -> List[List[Dict]]:
        """Get the current state of all junctions in the grid."""
        pass  # TODO: fill this
