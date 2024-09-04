import numpy as np
from typing import List
from numpy import ndarray
from Model.Car import Car
from Model.TrafficLight import TrafficLight
from Model.Grid import Grid
from Model.TrafficSystem import TrafficSystem, Direction
from Model.Coordinate import Coordinate


class Neighborhood:
    def __init__(self, cars: List[Car], grid: Grid, traffic_system: TrafficSystem, shift_x: int, shift_y: int):

        self.original_num_of_cars = len(cars)
        self.cars: List[Car] = cars
        self.traffic_system = traffic_system
        self.grid = grid
        self.cars = cars
        self.shift_x = shift_x
        self.shift_y = shift_y
        self.n = len(self.grid.junctions)
        self.m = len(self.grid.junctions[0])

    @classmethod
    def deep_copy(cls, other: 'Neighborhood') -> 'Neighborhood':
        """
        Deep coy a Neighborhood to another Neighborhood.
        :param other: The Neighborhood to copy.
        :return: The copied Neighborhood.
        """
        copy_cars = [Car.copy_constructor(car) for car in other.cars]
        copy_traffic_lights = [[TrafficLight() for _ in range(other.m)] for _ in range(other.n)]
        copy_grid = Grid.copy(other.grid, copy_traffic_lights)  # with wait times
        copy_traffic_system = TrafficSystem(copy_traffic_lights)
        for car in copy_cars:
            neighborhood_location = (
                Coordinate(car.current_location.x - other.shift_x, car.current_location.y - other.shift_y))
            if neighborhood_location.y < other.m and neighborhood_location.x < other.n:
                copy_grid.add_car_to_junction(car, neighborhood_location)

        return cls(
            copy_cars,
            copy_grid,
            copy_traffic_system,
            other.shift_x,
            other.shift_y
        )

    def get_state(self) -> ndarray:
        """Return the current state of the Neighborhood."""
        rows = len(self.grid.junctions)
        cols = len(self.grid.junctions[0])

        state = np.zeros((rows, cols, 4), dtype=int)
        for i, junctions in enumerate(self.grid.junctions):
            for j, junction in enumerate(junctions):
                is_vertical = 0
                is_horizontal = 0
                if junction.get_is_vertical_highway():
                    is_vertical = 1
                if junction.get_is_horizontal_highway():
                    is_horizontal = 1
                vertical_cars = sum(
                    1 for car in junction.cars.values() if car.current_direction() == Direction.VERTICAL)
                horizontal_cars = sum(
                    1 for car in junction.cars.values() if car.current_direction() == Direction.HORIZONTAL)

                state[i, j] = [vertical_cars, horizontal_cars, is_vertical, is_horizontal]
        return state.flatten()

    def update_neighborhood(self, assignment: np.ndarray) -> None:
        """Forward the neighborhood state by one tick of time"""
        self.traffic_system.update_traffic_lights(assignment)
        self.remove_cars_from_grid()
        self.grid.update_sub_grid()

    def remove_cars_from_grid(self):
        for car in self.cars:
            if self.grid.out_of_grid(car.current_location) and not car.get_did_arrive():
                car.set_did_arrive(True)
            elif car.current_location == car.destination and not car.get_did_arrive():
                self.grid.junctions[car.destination.x][car.destination.y].remove_car(car)

    def active_cars_amount(self) -> int:
        amount = 0
        for junctions in self.grid.junctions:
            for junction in junctions:
                amount += len(junction.cars)

        return amount

    def print(self, assignment: ndarray):
        """Print a visual representation of the City."""
        print("-----------------------------------------------------------------------------")
        print("Neighborhood layout:")
        # ANSI color codes
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        RESET = "\033[0m"

        for i in range(self.n):
            # Print junctions and horizontal connections
            for j in range(self.m):
                junction = self.grid.junctions[i][j]
                light_direction = 'V' if assignment[i, j] == Direction.VERTICAL else 'H'
                vertical_cars = sum(
                    1 for car in junction.cars.values() if car.current_direction() == Direction.VERTICAL)
                horizontal_cars = sum(
                    1 for car in junction.cars.values() if car.current_direction() == Direction.HORIZONTAL)

                # Color the direction only if there are cars in the junction
                total_cars = vertical_cars + horizontal_cars
                if total_cars > 0:
                    direction_color = GREEN if light_direction == 'V' else YELLOW
                else:
                    direction_color = ""

                # Color the car counts, keeping zeros white
                v_color = GREEN if vertical_cars > 0 else ""
                h_color = YELLOW if horizontal_cars > 0 else ""

                # Color coordinates based on type
                coord_color = ""

                print(
                    f"[D:{direction_color}{light_direction}{RESET}, V:{v_color}{vertical_cars:2d}{RESET},"
                    f" H:{h_color}{horizontal_cars:2d}{RESET}, {coord_color}(i:{i},j:{j}){RESET}]",
                    end="")
                if j < self.m - 1:
                    print(" -- ", end="")
            print()

            # Print vertical connections
            if i < self.n - 1:
                for j in range(self.m):
                    print("           |           ", end="")
                    if j < self.m - 1:
                        print("     ", end="")
                print()

