from typing import List, Tuple, Sequence
from Car import Car
from TrafficLight import TrafficLight
from Grid import Grid
from TrafficSystem import TrafficSystem
import random
from Coordinate import Coordinate


class City:
    def __init__(self, n: int, m: int, num_cars: int, residential_coords: List[Coordinate],
                 industrial_coords: List[Coordinate]):
        self.residential_coords = residential_coords
        self.industrial_coords = industrial_coords
        self.cars = self.init_cars(num_cars)
        self.traffic_lights = self.init_traffic_lights(n, m)
        self.grid = self.init_grid(n, m, self.cars, self.traffic_lights)
        self.traffic_system = self.init_traffic_system(self.traffic_lights)
        self.counter = 0

    def init_cars(self, amount: int) -> List[Car]:
        """Initialize a specified number of cars."""
        return [self.init_car() for _ in range(amount)]

    def init_car(self) -> Car:
        """Initialize a single car with random source, destination, and departure time."""
        source = self.get_random_location(self.residential_coords)
        dest = self.get_random_location(self.industrial_coords)
        departure_time = self.get_normal_departure_time(0, 10)
        return Car(f"Car_{self.counter}", source, dest, departure_time)

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

    def init_grid(self, n: int, m: int, cars: List[Car], traffic_lights: List[List[TrafficLight]]) -> Grid:
        """Initialize the city grid."""
        grid = Grid(traffic_lights)
        for car in cars:
            i, j = car.source
            grid.add_car_to_junction(car, i, j)
        return grid

    def init_traffic_system(self, traffic_lights: list[list[TrafficLight]]) -> TrafficSystem:
        """Initialize the traffic system."""
        return TrafficSystem(traffic_lights)

    def init_counter(self) -> None:
        """Initialize or reset the counter."""
        self.counter = 0

    def generate_state(self) -> Grid:
        """Generate the current state of the city."""
        pass
