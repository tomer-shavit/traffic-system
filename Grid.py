from typing import List, Dict

from Coordinate import Coordinate
from Junction import Junction
from TrafficLight import TrafficLight, Direction
from Car import Car

START_HIGH_WAY = 2
END_REFERENCE_HIGHWAY = 3
GAP_HIGH_WAY = 4


class Grid:
    def __init__(self, traffic_lights: List[List[TrafficLight]],
                 vertical_highway_junctions: List[Coordinate] = None,
                 horizontal_highway_junctions: List[Coordinate] = None):
        self.n = len(traffic_lights)
        self.m = len(traffic_lights[0])
        if vertical_highway_junctions:
            self.vertical_highway_junctions: List[Coordinate] = vertical_highway_junctions
        else:
            self.vertical_highway_junctions: List[Coordinate] = (self.init_vertical_highway_junctions(
                [START_HIGH_WAY, self.m - END_REFERENCE_HIGHWAY], self.n - GAP_HIGH_WAY))
        if horizontal_highway_junctions:
            self.horizontal_highway_junctions: List[Coordinate] = horizontal_highway_junctions
        else:
            self.horizontal_highway_junctions: List[Coordinate] = (self.init_horizontal_highway_junctions(
                [START_HIGH_WAY, self.n - END_REFERENCE_HIGHWAY], self.m - GAP_HIGH_WAY))
        self.junctions: List[List[Junction]] = self.init_junctions(traffic_lights)
        self.total_car_movements = 0

    def init_junctions(self, traffic_lights) -> List[List[Junction]]:
        """
        Initialize a 2D array of Junctions by the given traffic light configuration.
        :param traffic_lights: A 2D array of traffic lights configuration.
        :return: A 2d array of Junctions.
        """
        return [
            [
                Junction(
                    traffic_lights[i][j],
                    Coordinate(i, j) in self.horizontal_highway_junctions,
                    Coordinate(i, j) in self.vertical_highway_junctions
                )
                for j in range(self.m)
            ]
            for i in range(self.n)
        ]

    def reset(self) -> None:
        for junctions in self.junctions:
            for junction in junctions:
                junction.reset()
        self.total_car_movements = 0

    def update_grid(self) -> None:
        """Update the state of all junctions in the grid and move cars."""
        cars_to_move = self.get_cars_to_move()
        # Now move the cars
        for car, old_coordinate, new_coordinate in cars_to_move:
            self.junctions[old_coordinate.x][old_coordinate.y].remove_car(car)
            self.junctions[new_coordinate.x][new_coordinate.y].add_car(car)
            car.update_current_location()

    def update_sub_grid(self) -> None:
        cars_to_move = self.get_cars_to_move()
        for car, old_coordinate, new_coordinate in cars_to_move:
            self.junctions[old_coordinate.x][old_coordinate.y].remove_car(car)
            if self.out_of_grid(new_coordinate):
                pass
            else:
                self.junctions[new_coordinate.x][new_coordinate.y].add_car(car)
            car.update_current_location()

    def out_of_grid(self, coordinate: Coordinate) -> bool:
        """
        Checks if a coordinate is out of the grid bounds.
        :param coordinate: The coordinate to check.
        :return: True if coordinate is out of bounds.
        """
        if coordinate.x >= self.n or coordinate.y >= self.m:
            return True
        return False

    def get_cars_to_move(self) -> list[tuple[Car, Coordinate, Coordinate]]:
        """Return a list of all the cars that will move in the next tick ot time and where they
        will move"""
        cars_to_move = []
        # First, update all junctions and collect cars that need to be moved
        for i in range(self.n):
            for j in range(self.m):
                junction = self.junctions[i][j]
                direction, moving_cars = junction.resolve_moving_cars()
                self.total_car_movements += len(moving_cars)

                for car in moving_cars:
                    if direction == Direction.VERTICAL and i < self.n - 1:
                        cars_to_move.append((car, Coordinate(i, j), Coordinate(i + 1, j)))  # Move Up
                    elif direction == Direction.HORIZONTAL and j < self.m - 1:
                        cars_to_move.append((car, Coordinate(i, j), Coordinate(i, j + 1)))  # Move Right
        return cars_to_move

    def get_all_junctions_wait_time(self) -> List[List[Dict[str, int]]]:
        return [[junction.get_cars_wait_time() for junction in junctions] for junctions in self.junctions]

    def get_total_avg_wait_time(self) -> float:
        """Calculate the average wait time across all unique cars in all junctions."""
        all_junctions_avg_wait_time = sum([sum([junction.get_avg_wait_time() for junction in junctions]) for junctions in
                                           self.junctions])
        return all_junctions_avg_wait_time / (self.m * self.n)

    def add_car_to_junction(self, car: Car, coordinate: Coordinate) -> None:
        """Add a car to a specific junction."""
        if 0 <= coordinate.x < self.n and 0 <= coordinate.y < self.m:
            self.junctions[coordinate.x][coordinate.y].add_car(car)
        else:
            print(f"Invalid junction coordinates: ({coordinate.x}, {coordinate.y})")

    def init_vertical_highway_junctions(self, vertical_highways: List[int], width: int = 1) -> List[Coordinate]:
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

    def init_horizontal_highway_junctions(self, horizontal_highways: List[int], width: int = 1) -> List[Coordinate]:
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

    def check_highway_direction(self, coordinate: Coordinate) -> List[Direction]:
        """If coordinate is on a highway, return the highway preferred direction"""
        if coordinate in self.vertical_highway_junctions:
            if coordinate in self.horizontal_highway_junctions:
                return [Direction.VERTICAL, Direction.HORIZONTAL]
            return [Direction.VERTICAL]
        if coordinate in self.horizontal_highway_junctions:
            return [Direction.HORIZONTAL]
        return [Direction.VERTICAL, Direction.HORIZONTAL]
