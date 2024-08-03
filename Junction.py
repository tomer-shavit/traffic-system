from dataclasses import field
from typing import Dict, List, Tuple
from TrafficLight import TrafficLight, Direction
from Car import Car


class Junction:
    def __init__(self, traffic_light: TrafficLight):
        self.traffic_light = traffic_light
        self.cars: Dict[str, Car] = dict()
        self.cars_wait_time: Dict[str, int] = dict()

    def add_car(self, car: Car) -> None:
        """Add a single car to the junction."""
        self.cars[car.id] = car
        if car.id not in self.cars_wait_time:
            self.cars_wait_time[car.id] = 0

    def remove_car(self, car: Car) -> None:
        """Remove a single car from the junction."""
        if car.id in self.cars:
            del self.cars[car.id]

    def update_junction(self) -> Tuple[Direction, List[Car]]:
        """
        Update the junction state and return the current traffic light direction
        and the list of cars that can move.
        """
        current_direction = self.traffic_light.get_current_direction()
        cars_to_move = [car for car in self.cars.values() if car.current_direction() == current_direction]

        for car in cars_to_move:
            del self.cars[car.id]

        for car_id, car in self.cars.items():
            self.cars_wait_time[car_id] += 1

        return current_direction, cars_to_move

    def add_cars(self, cars: List[Car]) -> None:
        """Add multiple cars to the junction."""
        for car in cars:
            self.add_car(car)

    def get_avg_wait_time(self) -> float:
        """Calculate and return the average wait time of cars in the junction."""
        if not self.cars:
            return 0.0
        total_wait_time = sum(self.cars_wait_time.values())
        return total_wait_time / len(self.cars_wait_time)

    def get_car(self, car_id: str) -> Car:
        """Get a car by its ID."""
        return self.cars.get(car_id)

    def get_cars(self) -> List[Car]:
        """Get all cars in the junction."""
        return list(self.cars.values())

    def get_car_wait_time(self, car_id: str) -> int:
        """Get the wait time for a specific car."""
        return self.cars_wait_time.get(car_id, 0)

    def clear_junction(self) -> None:
        """Remove all cars from the junction."""
        self.cars.clear()
        self.cars_wait_time.clear()
