from City import City
from Coordinate import Coordinate
import numpy as np
from Direction import Direction

if __name__ == "__main__":
    m = 6
    n = 6
    num_cars = 10

    city = City.generate_city(n, m, num_cars)
    print("###### Test 1: ######")
    print(f"m = {m}, n = {n}, num_cars = {num_cars}:\n")
    while 0 != city.driving_cars_amount():
        rand_traffic = np.random.choice(list(Direction), size=(n, m))
        city.update_city(rand_traffic, True)
        print("###### next step: ######")
        print(f"waiting time: {city.get_current_avg_wait_time()}")
    print("\n\n")