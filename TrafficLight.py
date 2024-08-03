from dataclasses import dataclass
from Direction import Direction


@dataclass
class TrafficLight:
    current_direction: Direction = Direction.HORIZONTAL

    def get_current_direction(self) -> Direction:
        """Get the current direction of the traffic light."""
        return self.current_direction

    def set_direction(self, direction: Direction) -> None:
        """Set the direction of the traffic light."""
        self.current_direction = direction
