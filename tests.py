from City import City
from Coordinate import Coordinate
import numpy as np
from Direction import Direction


def print_path(city: City):
    grid = [['.' for _ in range(city.m)] for _ in range(city.n)]

    for car in city.cars:
        print(f"Car {car.id} source = ({car.source.x},{car.source.y}) dest =  ({car.destination.x},{car.destination.y}) Path:")

        # Reset the grid for each car
        grid = [['.' for _ in range(city.m)] for _ in range(city.n)]

        # Mark the car's path on the grid
        for step, coordinate in enumerate(car.path):
            if step == 0:
                grid[coordinate.x][coordinate.y] = 'S'  # Start point
            elif step == len(car.path) - 1:
                grid[coordinate.x][coordinate.y] = 'D'  # Destination
            else:
                grid[coordinate.x][coordinate.y] = '*'  # Path

        # Print the grid
        for row in grid:
            print(' '.join(row))
        print("\n" + "-" * (2 * city.m - 1) + "\n")




if __name__ == "__main__":
    m = 12
    n = 12
    num_cars = 20

    city = City.generate_city(n, m, num_cars)
    print_path(city)
    print("###### Test 1: ######")
    print(f"m = {m}, n = {n}, num_cars = {num_cars}:\n")
    while 0 != city.driving_cars_amount():
        rand_traffic = np.random.choice(list(Direction), size=(n, m))
        city.update_city(rand_traffic, True)
        print("###### next step: ######")
        print(f"waiting time: {city.get_current_avg_wait_time()}")
    print("\n\n")