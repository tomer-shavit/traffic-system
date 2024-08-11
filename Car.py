from typing import List

import numpy as np

from Coordinate import Coordinate
from Direction import Direction
import random

NOISE_CAR_PATH = 0.1

class Car:
    def __init__(self, car_id: str, source: Coordinate, destination: Coordinate, start_time: int, allow_directions):
        self._id: str = car_id
        self._source: Coordinate = source
        self._destination: Coordinate = destination
        self._current_location_index: int = 0
        self._path: List[Coordinate] = []
        self._start_time: int = start_time
        self._did_arrive: bool = False
        self._allow_directions_foo = allow_directions
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
        # When just one direction is allowed:
        # if len(self._allow_directions_foo(current)) == 1:
        #     direction = self._allow_directions_foo(current)[0]
        #     if direction == Direction.VERTICAL:
        #         return Coordinate(current.x, current.y + 1)
        #     return Coordinate(current.x + 1, current.y)

        # When both of the directions are allowed
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

    def update_current_location(self) -> None:
        if self._current_location_index < len(self._path) - 1:
            self._current_location_index += 1

        if self._current_location_index == len(self._path) - 1:
            self._did_arrive = True

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

    def _flip_next_step(self, current: Coordinate, next_step: Coordinate) -> Coordinate:
        """
        flip the next step. if the next step is horizontal, so move vertical instead, and vise versa.
        :param current: the current coordinate
        :param next_step: the next coordinate before flipping
        :return: The next step cooredinate after flipping
        """
        if abs(current.x - next_step.x) == 1:
            return Coordinate(current.x, current.y + 1)
        return Coordinate(current.x + 1, current.y)

