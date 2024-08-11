from typing import List, Tuple, Sequence

from numpy import ndarray

from Car import Car
from TrafficLight import TrafficLight
from Grid import Grid
from TrafficSystem import TrafficSystem, Direction
import random
from Coordinate import Coordinate

INDUSTRIAL_SIZE = 2
RESIDENTIAL_SIZE = 2
MAX_TIME_TO_START = 10
MIN_TIME_TO_START = 0

class City:
    def __init__(self, n: int, m: int, num_cars: int, residential_coords: List[Coordinate],
                 industrial_coords: List[Coordinate]):
        self.cars = None
        self.time = 0
        self.residential_coords = residential_coords
        self.industrial_coords = industrial_coords
        self.traffic_lights = self.init_traffic_lights(n, m)
        self.grid = self.init_grid(self.traffic_lights)
        self.init_cars(num_cars)
        self.traffic_system = self.init_traffic_system(self.traffic_lights)
        self.time = 0
        self.n = n
        self.m = m


    def init_cars(self, amount: int):
        """Initialize a specified number of cars."""
        self.cars = [self.init_car(i) for i in range(amount)]

    def init_car(self, car_num: int) -> Car:
        """Initialize a single car with random source, destination, and departure time."""
        source = self.get_random_location(self.residential_coords)
        dest = self.get_random_location(self.industrial_coords)
        departure_time = self.get_normal_departure_time(MIN_TIME_TO_START, MAX_TIME_TO_START)
        return Car(f"Car_{car_num}", source, dest, departure_time, self.grid.allow_directions)

    def get_normal_departure_time(self, mean: float, std_dev: float) -> int:
        """Generate a normally distributed departure time within 0 to 10 and round to a whole number."""
        departure_time = round(random.normalvariate(mean, std_dev))
        return max(0, min(10, departure_time))

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
        self.traffic_system.update_traffic_lights(assignment)
        if debug:
            self.print(assignment)
        self.remove_cars_from_grid()
        self.grid.update_grid()
        self.add_cars_to_grid_by_time()
        self.time += 1

    def print(self, assignment: ndarray):
        """Print a visual representation of the City."""
        print("Waiting vehicles (V for vertical, H for horizontal):")
        for i in range(self.n):
            for j in range(self.m):
                junction = self.grid.junctions[i][j]
                vertical_cars = sum(
                    1 for car in junction.cars.values() if car.current_direction() == Direction.VERTICAL)
                horizontal_cars = sum(
                    1 for car in junction.cars.values() if car.current_direction() == Direction.HORIZONTAL)
                print(f"[V:{vertical_cars:2d},H:{horizontal_cars:2d}]", end="")
                if j < self.m - 1:
                    print(" -- ", end="")
            print()
            print()

        print("Traffic light directions (V for vertical, H for horizontal):")
        for i in range(self.n):
            for j in range(self.m):
                junction = self.grid.junctions[i][j]
                light_direction = 'V' if assignment[i, j] == Direction.VERTICAL else 'H'
                print(f"[D:{light_direction}]", end="")
                if j < self.m - 1:
                    print(" -- ", end="")
            print()
            print()

    def driving_cars_amount(self) -> int:
        num_of_driving_cars = 0
        for car in self.cars:
            if not car.get_did_arrive():
                num_of_driving_cars += 1
        return num_of_driving_cars

    def generate_state(self) -> Grid:
        """Generate the current state of the city."""
        pass

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
        for car in self.cars:
            if car.start_time == self.time:
                self.grid.add_car_to_junction(car, car.source)

    def remove_cars_from_grid(self):
        for car in self.cars:
            if car.current_location == car.destination:
                self.grid.junctions[car.destination.x][car.destination.y].remove_car(car)
