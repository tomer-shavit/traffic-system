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
    # city.grid.print()
    while not city.did_all_cars_arrive():
        rand_traffic = np.random.choice(list(Direction), size=(n, m))
        city.update_city(rand_traffic, True)
        city.grid.update_grid()
        print("###### next step: ######")
        print(rand_traffic)
        # city.grid.print()
        print(f"waiting time: {city.get_current_avg_wait_time()}")
    print("\n\n")

    m = 5
    n = 5
    num_cars = 1
    res_coor = Coordinate(1,1)
    ind_coor = Coordinate(n-1, m-1)
    city = City(n, m, num_cars, [res_coor], [ind_coor])
    print("###### Test 2: ######")
    print(f"m = {m}, n = {n}, num_cars = {num_cars}\n")
    # city.grid.print()

    # while not city.all_cars_arrived():
    #     city.grid.update_grid()
    #     print("###### next step: ######")
    #     city.grid.print()