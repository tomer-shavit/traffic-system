from typing import List
from TrafficLight import TrafficLight, Direction


class TrafficSystem:
    def __init__(self, traffic_lights: List[List[TrafficLight]]):
        self.traffic_lights = traffic_lights

    def update_traffic_lights(self, assignment: List[List[Direction]]) -> None:
        """
        Update the traffic lights based on the given assignment.

        :param assignment: An NxM binary grid where 0 represents horizontal and 1 represents vertical direction.
        """
        if len(assignment) != len(self.traffic_lights) or len(assignment[0]) != len(self.traffic_lights[0]):
            raise ValueError("Assignment dimensions do not match traffic light grid dimensions")

        for i in range(len(self.traffic_lights)):
            for j in range(len(self.traffic_lights[0])):
                if assignment[i][j] == Direction.HORIZONTAL:
                    self.traffic_lights[i][j].set_direction(Direction.HORIZONTAL)
                elif assignment[i][j] == Direction.VERTICAL:
                    self.traffic_lights[i][j].set_direction(Direction.VERTICAL)
                else:
                    raise ValueError(f"Invalid assignment value at position ({i}, {j}): {assignment[i][j]}")
