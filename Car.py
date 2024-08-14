from typing import List, Callable

import numpy as np

from Coordinate import Coordinate
from Direction import Direction
import random

NOISE_CAR_PATH = 0.03

class Car:
    def __init__(self, car_id: str, source: Coordinate, destination: Coordinate, start_time: int,
                 allow_directions: Callable[[Coordinate], List[Direction]]):
        self._id: str = car_id
        self._source: Coordinate = source
        self._destination: Coordinate = destination
        self._current_location_index: int = 0
        self._path: List[Coordinate] = []
        self._start_time: int = start_time
        self._did_arrive: bool = False
        self._get_allowed_directions = allow_directions
        self._init_path()

    def current_direction(self) -> Direction:
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
        To represent a realistic city, for each junction we define what direction in allows to move.
        For example, if the set of junctions: {(x,y), (x,y+1), (x,y+2)} allows to drive vertical only,
        it represents a highway.
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
        highway_step = self.get_highway_step(current)
        if self.valid_step(highway_step):
            return highway_step
        return self.get_probabilistic_step(current)

    def update_current_location(self) -> None:
        if self._current_location_index < len(self._path) - 1:
            self._current_location_index += 1

    def reset(self):
        self._did_arrive = False
        self._current_location_index = 0

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

    def _flip_next_step(self, current: Coordinate, next_step: Coordinate) -> Coordinate:
        """
        flip the next step. if the next step is horizontal, so move vertical instead, and vise versa.
        :param current: the current coordinate
        :param next_step: the next coordinate before flipping
        :return: The next step cooredinate after flipping
        """
        if abs(current.x - next_step.x) == 1:
            flipped_coordinate = Coordinate(current.x, current.y + 1)
        else:
            flipped_coordinate = Coordinate(current.x + 1, current.y)
        if flipped_coordinate.x > self._destination.x or flipped_coordinate.y > self._destination.y :
            return next_step
        return flipped_coordinate

    def get_highway_step(self, current: Coordinate) -> Coordinate:
        allowed_directions = self._get_allowed_directions(current)

        if len(allowed_directions) == 1:
            direction = allowed_directions[0]
            if direction == Direction.VERTICAL:
                return Coordinate(current.x + 1, current.y)
            return Coordinate(current.x, current.y + 1)

        return Coordinate(-1, -1)

    def get_probabilistic_step(self, current):
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

    def valid_step(self, highway_step: Coordinate) -> bool:
        if highway_step == Coordinate(-1, -1):
            return False
        if highway_step.x > self._destination.x:
            return False
        if highway_step.y > self._destination.y:
            return False
        return True
