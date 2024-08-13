from typing import List, Tuple, Dict

from Coordinate import Coordinate
from Junction import Junction
from TrafficLight import TrafficLight, Direction
from Car import Car

START_HIGH_WAY = 2
END_REFERENCE_HIGHWAY = 3
GAP_HIGH_WAY = 4

class Grid:
    def __init__(self, traffic_lights: List[List[TrafficLight]]):
        self.n = len(traffic_lights)
        self.m = len(traffic_lights[0])
        self.junctions: List[List[Junction]] = [
            [Junction(traffic_lights[i][j]) for j in range(self.m)] for i in range(self.n)
        ]
        self.vertical_junctions: List[Coordinate] = (self.init_vertical_junctions(
            [START_HIGH_WAY, self.m - END_REFERENCE_HIGHWAY], self.n - GAP_HIGH_WAY))
        self.horizontal_junctions: List[Coordinate] = (self.init_horizontal_junctions(
                [START_HIGH_WAY, self.n - END_REFERENCE_HIGHWAY], self.m - GAP_HIGH_WAY))

    def reset(self):
        for junctions in self.junctions:
            for junction in junctions:
                junction.reset()

    def update_grid(self) -> None:
        """Update the state of all junctions in the grid and move cars."""
        cars_to_move = []  # List to store cars that need to be moved

        # First, update all junctions and collect cars that need to be moved
        for i in range(self.n):
            for j in range(self.m):
                junction = self.junctions[i][j]
                direction, moving_cars = junction.resolve_moving_cars()

                for car in moving_cars:
                    if direction == Direction.VERTICAL and i < self.n - 1:
                        cars_to_move.append((car, Coordinate(i, j), Coordinate(i + 1, j)))  # Move Up
                    elif direction == Direction.HORIZONTAL and j < self.m - 1:
                        cars_to_move.append((car, Coordinate(i, j), Coordinate(i, j + 1)))  # Move Right

        # Now move the cars
        for car, old_coordinate, new_coordinate in cars_to_move:
            self.junctions[old_coordinate.x][old_coordinate.y].remove_car(car)
            self.junctions[new_coordinate.x][new_coordinate.y].add_car(car)
            car.update_current_location()

    def get_total_avg_wait_time(self) -> float:
        """Calculate the average wait time across all unique cars in all junctions."""
        return sum([sum([junction.get_avg_wait_time() for junction in junctions]) for junctions in
                    self.junctions]) / (self.m * self.n)

    def add_car_to_junction(self, car: Car, coordinate: Coordinate) -> None:
        """Add a car to a specific junction."""
        if 0 <= coordinate.x < self.n and 0 <= coordinate.y < self.m:
            self.junctions[coordinate.x][coordinate.y].add_car(car)
        else:
            print(f"Invalid junction coordinates: ({coordinate.x}, {coordinate.y})")

    def get_grid_state(self) -> List[List[Dict]]:
        """Get the current state of all junctions in the grid."""
        pass  # TODO: fill this

    def init_vertical_junctions(self, vertical_highways: List[int], width: int = 1) -> List[Coordinate]:
        """
        Initialize vertical highways by specifying which columns should have vertical highways.
        :param vertical_highways: List of column indices where vertical highways should be placed.
        :param width: The width of each vertical highway (default is 1).
        :return: List of Coordinates for vertical junctions.
        """
        vertical_junctions = []
        start_point = (self.n - width) // 2
        for row in vertical_highways:
            for w in range(width):
                vertical_junctions.append(Coordinate(start_point + w, row))
        return vertical_junctions

    def init_horizontal_junctions(self, horizontal_highways: List[int], width: int = 1) -> List[Coordinate]:
        """
        Initialize horizontal highways by specifying which rows should have horizontal highways.
        :param horizontal_highways: List of row indices where horizontal highways should be placed.
        :param width: The width of each horizontal highway (default is 1).
        :return: List of Coordinates for horizontal junctions.
        """
        horizontal_junctions = []
        start_point = (self.m - width) // 2
        for column in horizontal_highways:
            for w in range(width):
                horizontal_junctions.append(Coordinate(column, start_point + w))
        return horizontal_junctions

    def allow_directions(self, coordinate: Coordinate) -> List[Direction]:
        if coordinate in self.vertical_junctions:
            if coordinate in self.horizontal_junctions:
                return [Direction.VERTICAL, Direction.HORIZONTAL]
            return [Direction.VERTICAL]
        if coordinate in self.horizontal_junctions:
            return [Direction.HORIZONTAL]
        return [Direction.VERTICAL, Direction.HORIZONTAL]

