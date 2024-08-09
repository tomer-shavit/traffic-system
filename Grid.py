from typing import List, Tuple, Dict

from Coordinate import Coordinate
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
                direction, moving_cars = junction.resolve_moving_cars()

                for car in moving_cars:
                    if direction == Direction.VERTICAL and j < self.m - 1:
                        cars_to_move.append((car, Coordinate(i, j), Coordinate(i, j + 1)))  # Move Up
                    elif direction == Direction.HORIZONTAL and i < self.n - 1:
                        cars_to_move.append((car, Coordinate(i, j), Coordinate(i + 1, j)))  # Move Right

        # Now move the cars
        for car, old_coordinate, new_coordinate in cars_to_move:
            self.junctions[old_coordinate.x][old_coordinate.y].remove_car(car)
            self.junctions[new_coordinate.x][new_coordinate.y].add_car(car)
            car.update_current_location()

    def get_total_avg_wait_time(self) -> float:
        """Calculate the average wait time across all unique cars in all junctions."""

        return sum([sum([junction.get_avg_wait_time() for junction in junctions]) for junctions in
                    self.junctions]) / (self.m * self.n)

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
