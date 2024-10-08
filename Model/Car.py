import numpy as np
import random
from typing import List, Callable
from Model.Coordinate import Coordinate
from Model.Direction import Direction

NOISE_CAR_PATH = 0.03


class Car:
    def __init__(self, car_id: str, source: Coordinate, destination: Coordinate, start_time: int,
                 get_highway_direction: Callable[[Coordinate], List[Direction]]):
        self._id: str = car_id
        self._source: Coordinate = source
        self._destination: Coordinate = destination
        self._current_location_index: int = 0
        self._path: List[Coordinate] = []
        self._start_time: int = start_time
        self._did_arrive: bool = False
        self._get_highway_direction = get_highway_direction
        self._init_path()

    @classmethod
    def copy_constructor(cls, other_car: 'Car') -> 'Car':
        new_car = cls(
            car_id=other_car._id,
            source=Coordinate(other_car._source.x, other_car._source.y),
            destination=Coordinate(other_car._destination.x, other_car._destination.y),
            start_time=other_car._start_time,
            get_highway_direction=other_car._get_highway_direction
        )
        new_car._path = list(other_car._path)
        new_car._current_location_index = other_car._current_location_index
        new_car._did_arrive = other_car._did_arrive
        return new_car

    @property
    def id(self) -> str:
        return self._id

    @property
    def source(self) -> Coordinate:
        return self._source

    @property
    def destination(self) -> Coordinate:
        return self._destination

    @property
    def current_location(self) -> Coordinate:
        return self._path[self._current_location_index]

    @property
    def start_time(self) -> int:
        return self._start_time

    @property
    def path(self) -> List[Coordinate]:
        return self._path

    def current_direction(self) -> Direction:
        """
        Returns the cars current direction
        :return:
        """
        if self._current_location_index >= len(self._path) - 1:
            return Direction.HORIZONTAL  # Default direction if path is complete

        current_location = self._path[self._current_location_index]
        next_location = self._path[self._current_location_index + 1]

        if current_location.x == next_location.x:
            return Direction.HORIZONTAL
        else:
            return Direction.VERTICAL

    def get_did_arrive(self) -> bool:
        return self._did_arrive

    def set_did_arrive(self, arrive: bool):
        self._did_arrive = arrive

    def _init_path(self) -> None:
        """
        Choose a path from the source coordinate to the destination coordinate.
        """
        self._path = [self._source]
        current = self._source

        while current != self._destination:
            next_step = self._choose_next_step(current)
            if np.random.random(1)[0] < NOISE_CAR_PATH:
                next_step = self._flip_next_step(current, next_step)
            self._path.append(next_step)
            current = next_step

    def _choose_next_step(self, current: Coordinate) -> Coordinate:
        """
        Choose the car next step on the path.
        :param current: Current location.
        :return: The next step.
        """
        highway_next_step = self.get_highway_next_step(current)
        if self.valid_step(highway_next_step):
            return highway_next_step
        return self.get_probabilistic_step(current)

    def update_current_location(self) -> None:
        if self._current_location_index < len(self._path) - 1:
            self._current_location_index += 1

    def reset(self):
        self._did_arrive = False
        self._current_location_index = 0

    def _flip_next_step(self, current: Coordinate, next_step: Coordinate) -> Coordinate:
        """
        flip the next step. if the next step is horizontal, so move vertical instead, and vise versa.
        :param current: the current coordinate
        :param next_step: the next coordinate before flipping
        :return: The next step coordinate after flipping
        """
        if abs(current.x - next_step.x) == 1:
            flipped_coordinate = Coordinate(current.x, current.y + 1)
        else:
            flipped_coordinate = Coordinate(current.x + 1, current.y)
        if flipped_coordinate.x > self._destination.x or flipped_coordinate.y > self._destination.y:
            return next_step
        return flipped_coordinate

    def get_highway_next_step(self, current: Coordinate) -> Coordinate:
        """Return the direction flow of the highway, if current coordinate is on a highway"""
        allowed_directions = self._get_highway_direction(current)

        if len(allowed_directions) == 1:
            direction = allowed_directions[0]
            if direction == Direction.VERTICAL:
                return Coordinate(current.x + 1, current.y)
            return Coordinate(current.x, current.y + 1)

        return Coordinate(-1, -1)

    def get_probabilistic_step(self, current):
        """Uniformly choose the car next step to the destination"""
        steps_x = self._destination.x - current.x
        steps_y = self._destination.y - current.y
        total_steps = abs(steps_x) + abs(steps_y)
        if total_steps == 0:
            return current

        prob_x = abs(steps_x) / total_steps

        if random.random() < prob_x:
            new_x = current.x + (1 if steps_x > 0 else -1)
            return Coordinate(new_x, current.y)
        else:
            new_y = current.y + (1 if steps_y > 0 else -1)
            return Coordinate(current.x, new_y)

    def valid_step(self, coordinate: Coordinate) -> bool:
        """Check if the car current location is valid"""
        if coordinate == Coordinate(-1, -1):
            return False
        if coordinate.x > self._destination.x:
            return False
        if coordinate.y > self._destination.y:
            return False
        return True
