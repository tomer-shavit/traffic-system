import Coordinate


class Reporter:
    def __init__(self):
        # Initialize the data structure to store recorded data
        self.records = []

    def record_vehicle_count(self, junction_id: Coordinate, vertical_count: int, horizontal_count: int) -> None:
        """
        Record the number of vehicles at a specific junction.

        :param junction_id: The Coordinate of the junction.
        :param vertical_count: The number of vehicles waiting in the vertical direction.
        :param horizontal_count: The number of vehicles waiting in the horizontal direction.
        """
        record = {
            "event": "vehicle_count",
            "junction_id": f"{junction_id.x}, {junction_id.y}",
            "vertical_count": vertical_count,
            "horizontal_count": horizontal_count
        }
        self.records.append(record)

    def record_avg_wait_time(self, junction_id: Coordinate, avg_wait_time: float):
        """
        Record the average wait time at a junction.

        :param junction_id: The Coordinate of the junction.
        :param avg_wait_time: The average wait time.
        """
        record = {
            "event": "traffic_light_change",
            "junction_id": f"{junction_id.x}, {junction_id.y}",
            "avg_wait_time": avg_wait_time
        }
        self.records.append(record)

    def record_vehicle_arrival(self, vehicle_id: str, junction_id: Coordinate):
        """
        Record an arrival of a vehicle to its workplace

        :param vehicle_id: The vehicle Id.
        :param junction_id: The Coordinate of the junction.
        """
        record = {
            "event": "traffic_light_change",
            "vehicle_id": vehicle_id,
            "junction_id": f"{junction_id.x}, {junction_id.y}"
        }
        self.records.append(record)

    def get_report(self) -> list:
        """
        Return the current report as a list of recorded events.

        :return: A list of dictionaries representing the recorded events.
        """
        return self.records
