from City import City
from Coordinate import Coordinate
import numpy as np
from Direction import Direction

if __name__ == "__main__":
    m = 3
    n = 4
    num_cars = 2
    res_coor = Coordinate(0,0)
    ind_coor = Coordinate(n-1, m-1)
    city = City(n,m,num_cars, [res_coor], [ind_coor])
    print("###### Test 1: ######")
    print(f"m = {m}, n = {n}, num_cars = {num_cars}:\n")
    while not city.did_all_cars_arrive():
        rand_traffic = np.random.choice(list(Direction), size=(n, m))
        city.update_city(rand_traffic, True)
        print("###### next step: ######")
        print(rand_traffic)
        print(f"waiting time: {city.get_current_avg_wait_time()}")
    print("\n\n")