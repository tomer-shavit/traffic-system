from typing import List, Dict

import numpy as np
from numpy import ndarray
from Model.Car import Car
from Model.TrafficLight import TrafficLight
from Model.Grid import Grid
from Model.TrafficSystem import TrafficSystem, Direction
import random
from Model.Coordinate import Coordinate

INDUSTRIAL_SIZE = 2
RESIDENTIAL_SIZE = 2
MAX_TIME_TO_START = 4
MIN_TIME_TO_START = 0

INF_INT = 10000


class Neighborhood:
    def __init__(self, cars: List[Car], traffic_lights: List[List[TrafficLight]],
                 grid: Grid, traffic_system: TrafficSystem, shift_x: int, shift_y: int):

        self.original_num_of_cars = len(cars)
        self.cars: List[Car] = cars
        self.traffic_lights = traffic_lights
        self.traffic_system = traffic_system
        self.grid = grid
        self.cars = cars
        self.shift_x = shift_x
        self.shift_y = shift_y
        self.num_of_active_cars = len(self.cars)
        self.n = len(self.grid.junctions)
        self.m = len(self.grid.junctions[0])

    def get_state(self) -> ndarray:
        rows = len(self.grid.junctions)
        cols = len(self.grid.junctions[0])

        # The array will have 4 channels: [#V, #H, isV, isH]
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
        self.traffic_system.update_traffic_lights(assignment)
        self.remove_cars_from_grid()
        self.grid.update_sub_grid()

    def remove_cars_from_grid(self):
        for car in self.cars:
            if self.grid.out_of_grid(car.current_location) and not car.get_did_arrive():
                car.set_did_arrive(True)
                self.num_of_active_cars -= 1
            elif car.current_location == car.destination and not car.get_did_arrive():
                self.grid.junctions[car.destination.x][car.destination.y].remove_car(car)
                self.num_of_active_cars -= 1

    def active_cars_amount(self) -> int:
        return self.num_of_active_cars

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


class City:
    def __init__(self, n: int, m: int, num_cars: int, residential_coords: List[Coordinate],
                 industrial_coords: List[Coordinate]):
        self.cars: List[Car] = []
        self.time = 0
        self.residential_coords = residential_coords
        self.industrial_coords = industrial_coords
        self.traffic_lights = self.init_traffic_lights(n, m)
        self.grid = self.init_grid(self.traffic_lights)
        self.init_cars(num_cars)
        self.traffic_system = self.init_traffic_system(self.traffic_lights)
        self.n = n
        self.m = m
        self.num_of_active_cars = len(self.cars)
        self.all_cars_arrived_time: int = INF_INT

    def init_cars(self, amount: int):
        """Initialize a specified number of cars."""
        self.cars = [self.init_car(i) for i in range(amount)]

    def init_car(self, car_num: int) -> Car:
        """Initialize a single car with random source, destination, and departure time."""
        source = self.get_random_location(self.residential_coords)
        dest = self.get_random_location(self.industrial_coords)
        departure_time = self.get_normal_departure_time(MAX_TIME_TO_START / 2, MAX_TIME_TO_START / 2)
        return Car(f"Car_{car_num}", source, dest, departure_time, self.grid.check_highway_direction)

    def get_normal_departure_time(self, mean: float, std_dev: float) -> int:
        """Generate a normally distributed departure time."""
        departure_time = round(random.normalvariate(mean, std_dev))
        return max(0, min(MAX_TIME_TO_START, departure_time))

    def get_random_location(self, coords: List[Coordinate]) -> Coordinate:
        """Select a location based on a normal distribution among all locations."""
        index = round(random.normalvariate(len(coords) / 2, len(coords) / 6))
        index = max(0, min(len(coords) - 1, index))
        return coords[index]

    def init_traffic_lights(self, n: int, m: int) -> List[List[TrafficLight]]:
        """Initialize traffic lights for an n x m grid."""
        return [[TrafficLight() for _ in range(m)] for _ in range(n)]

    def init_grid(self, traffic_lights: List[List[TrafficLight]]) -> Grid:
        """Initialize the city grid."""
        grid = Grid(traffic_lights)
        return grid

    def init_traffic_system(self, traffic_lights: list[list[TrafficLight]]) -> TrafficSystem:
        """Initialize the traffic system."""
        return TrafficSystem(traffic_lights)

    def get_current_avg_wait_time(self):
        return self.grid.get_total_avg_wait_time()

    def update_city(self, assignment: ndarray, debug: bool = False):
        """Forward the city state by one tick of time"""
        self.traffic_system.update_traffic_lights(assignment)
        if debug:
            self.print(assignment)
        self.remove_cars_from_grid()
        self.grid.update_grid()
        self.add_cars_to_grid_by_time()
        self.update_cars_arrival_time()
        self.time += 1

    def print(self, assignment: ndarray):
        """Print a visual representation of the City."""
        print("-----------------------------------------------------------------------------")
        print("City layout:")
        # ANSI color codes
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        RESET = "\033[0m"
        BLUE = "\033[34m"
        PURPLE = "\033[35m"

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
                if any(coord.x == i and coord.y == j for coord in self.residential_coords):
                    coord_color = BLUE
                elif any(coord.x == i and coord.y == j for coord in self.industrial_coords):
                    coord_color = PURPLE

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

    def active_cars_amount(self) -> int:
        return self.num_of_active_cars

    @classmethod
    def generate_city(cls, n: int, m: int, num_cars: int) -> 'City':
        """
        Generates a city with the specified parameters.
        Residential coordinates are a subset of {(0,0), (0,1), (1,0), (1,1)}.
        Industrial coordinates are a subset of {(n,m), (n-1,m), (n,m-1), (n-1,m-1)}.

        Parameters:
        - n (int): Number of rows in the city grid.
        - m (int): Number of columns in the city grid.
        - num_cars (int): Number of cars to generate in the city.

        Returns:
        - City: A generated City object.
        """

        possible_residential = []
        for i in range(RESIDENTIAL_SIZE):
            for j in range(RESIDENTIAL_SIZE):
                possible_residential.append(Coordinate(0 + i, 0 + j))

        possible_industrial = []
        for i in range(INDUSTRIAL_SIZE):
            for j in range(INDUSTRIAL_SIZE):
                possible_industrial.append(Coordinate(n - 1 - i, m - 1 - j))

        # Ensure at least one residential and one industrial coordinate
        num_residential = random.randint(1, len(possible_residential))
        num_industrial = random.randint(1, len(possible_industrial))

        residential_coords = random.sample(possible_residential, num_residential)
        industrial_coords = random.sample(possible_industrial, num_industrial)

        return cls(n, m, num_cars, residential_coords, industrial_coords)

    @classmethod
    def generate_cities(cls, n: int, m: int, num_cars: int, num_cities) -> List['City']:
        return [City.generate_city(n, m, num_cars) for _ in range(num_cities)]

    def add_cars_to_grid_by_time(self):
        """Add all cars that need to depart in the current time to the grid"""
        for car in self.cars:
            if car.start_time == self.time:
                self.grid.add_car_to_junction(car, car.source)

    def reset_city(self) -> None:
        self.reset_cars()
        self.grid.reset()
        self.time = 0
        self.all_cars_arrived_time = INF_INT
        self.num_of_active_cars = len(self.cars)

    def remove_cars_from_grid(self):
        """Remove all cars that arrived to their destination to the grid"""
        for car in self.cars:
            if car.current_location == car.destination and not car.get_did_arrive():
                self.grid.junctions[car.destination.x][car.destination.y].remove_car(car)
                self.num_of_active_cars -= 1

    def reset_cars(self) -> None:
        for car in self.cars:
            car.reset()

    def update_cars_arrival_time(self):
        if self.num_of_active_cars == 0 and self.all_cars_arrived_time > self.time:
            self.all_cars_arrived_time = self.time

    def get_total_cars_movements(self):
        return self.grid.total_car_movements

    def get_all_junctions_wait_time(self) -> List[List[Dict[str, int]]]:
        return self.grid.get_all_junctions_wait_time()

    def get_neighborhood(self, top_left: Coordinate, top_right: Coordinate, bottom_left: Coordinate) -> Neighborhood:
        rows = bottom_left.x - top_left.x + 1
        cols = top_right.y - top_left.y + 1
        copy_traffic_lights = [[TrafficLight() for _ in range(cols)] for _ in range(rows)]
        horizontal_highway_junctions, vertical_highway_junctions = self.get_highway_coordinates(bottom_left,
                                                                                                copy_traffic_lights,
                                                                                                top_left, top_right)

        copy_grid = Grid(copy_traffic_lights, vertical_highway_junctions, horizontal_highway_junctions)
        copy_traffic_system = TrafficSystem(copy_traffic_lights)

        copy_cars = self.get_copy_cars(bottom_left, copy_grid, top_left, top_right)
        return Neighborhood(copy_cars, copy_traffic_lights, copy_grid, copy_traffic_system, top_left.x, top_left.y)

    def get_copy_cars(self, bottom_left, copy_grid, top_left, top_right):
        copy_cars = []
        for i in range(top_left.x, bottom_left.x + 1):
            for j in range(top_left.y, top_right.y + 1):
                for real_car in self.grid.junctions[i][j].cars.values():
                    copy_car = Car.copy_constructor(real_car)
                    neighborhood_location = (
                        Coordinate(copy_car.current_location.x - top_left.x, copy_car.current_location.y - top_left.y))
                    copy_grid.add_car_to_junction(copy_car, neighborhood_location)
                    copy_cars.append(copy_car)
        return copy_cars

    def get_highway_coordinates(self, bottom_left, copy_traffic_lights, top_left, top_right):
        horizontal_highway_junctions = []
        vertical_highway_junctions = []
        shift_x = top_left.x
        shift_y = top_left.y
        for i in range(top_left.x, bottom_left.x + 1):
            for j in range(top_left.y, top_right.y + 1):
                junction = self.grid.junctions[i][j]
                copy_traffic_lights[i - shift_x][j - shift_y].set_direction(
                    self.traffic_lights[i][j].get_current_direction())
                if junction.get_is_vertical_highway():
                    vertical_highway_junctions.append(Coordinate(i - shift_x, j - shift_y))
                if junction.get_is_horizontal_highway():
                    horizontal_highway_junctions.append(Coordinate(i - shift_x, j - shift_y))
        return horizontal_highway_junctions, vertical_highway_junctions
