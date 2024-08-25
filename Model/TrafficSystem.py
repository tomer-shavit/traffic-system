from typing import List
from Model.TrafficLight import TrafficLight
from Model.Direction import Direction
import numpy as np

class TrafficSystem:
    def __init__(self, traffic_lights: List[List[TrafficLight]]):
        self.traffic_lights = traffic_lights

    def update_traffic_lights(self, assignment: np.ndarray) -> None:
        """
        Update the traffic lights based on the given assignment.

        :param assignment: An NxM numpy array where each element is either Direction.HORIZONTAL or Direction.VERTICAL.
        """
        if assignment.shape != (len(self.traffic_lights), len(self.traffic_lights[0])):
            raise ValueError("Assignment dimensions do not match traffic light grid dimensions")

        if not np.all(np.isin(assignment, [Direction.HORIZONTAL, Direction.VERTICAL])):
            raise ValueError("Assignment contains invalid direction values")

        for i in range(len(self.traffic_lights)):
            for j in range(len(self.traffic_lights[0])):
                self.traffic_lights[i][j].set_direction(assignment[i, j])
