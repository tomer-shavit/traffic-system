from BaseLineSolver import BaseLineSolver
from City import City
from Coordinate import Coordinate
import numpy as np
from Direction import Direction
import matplotlib.pyplot as plt
import numpy as np

from Reporter import Reporter


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

def plot_result():

    # Step 1: Read the data from the .txt file
    file_path = './genetic_result_2'
    generations = []
    fitness_values = []

    with open(file_path, 'r') as file:
        for line in file:
            # Extract the generation number and fitness value
            if line == '\n':
                break
            parts = line.split(': Best fitness = ')
            generation = int(parts[0].split(' ')[1])
            fitness = float(parts[1])

            # Append to the lists
            generations.append(generation)
            fitness_values.append(fitness)

    # Step 2: Plot the data
    max_fitness = max(fitness_values)
    # Step 2: Plot the data with smaller markers
    plt.plot(generations, fitness_values, marker='o', markersize=2, label='Genetic Algorithm')

    # Step 3: Draw a red horizontal line at y = 2.6062604
    baseline_value = 2.6062604
    plt.axhline(y=baseline_value, color='red', linestyle='--', label='Baseline Solution')


    # Optional: Add a legend to explain the red line
    plt.legend()

    # Step 4: Add titles and labels
    plt.title('Best Fitness Over Generations - High Mutation Rate')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness Score')
    plt.grid(True)

    # Show the plot
    plt.show()

def load_data():
    # Load the data from the .npy files
    wait_times = np.load('./ReporterData/wait_times.npy')
    all_cars_arrive_time = np.load('./ReporterData/all_cars_arrive_time.npy')
    not_reaching_cars = np.load('./ReporterData/not_reaching_cars.npy')
    moving_cars_amount = np.load('./ReporterData/moving_cars_amount.npy')
    wait_time_punishment = np.load('./ReporterData/wait_time_punishment.npy')
    best_solutions = np.load('./ReporterData/best_solutions.npy', allow_pickle=True)

    # Example: Accessing and printing the data
    print(wait_times)
    print(all_cars_arrive_time)
    print(not_reaching_cars)
    print(moving_cars_amount)
    print(wait_time_punishment)
    print(best_solutions)

def extract_subgrid(solution: np.ndarray, top_left: Coordinate, bottom_right: Coordinate) -> np.ndarray:
    """
    Extract a subgrid from the given solution matrix based on the neighborhood's coordinates.
    """
    return solution[top_left.x:bottom_right.x + 1, top_left.y:bottom_right.y + 1]

def test_neighborhood():
    n = 5
    m = 5
    num_cars = 10
    t = 10
    reporter = Reporter()
    city = City.generate_city(n, m, num_cars)
    baseline = BaseLineSolver(n, m, t, reporter)
    solution = baseline.solve()
    for _t in range(t):
        city.update_city(solution[_t], True)
        top_left = Coordinate(1,1)
        top_right = Coordinate(1, 3)
        bottom_right = Coordinate(3,3)
        bottom_left = Coordinate(3, 1)
        sub_solution = extract_subgrid(solution[_t], top_left, bottom_right)
        neighborhood = city.get_neighborhood(top_left, top_right, bottom_left)
        neighborhood.print(sub_solution)
        print(neighborhood.get_state())
        if len(neighborhood.cars) > 0:
            print("\n***** start update neighborhood test: ******")
            for i in range(3):
                sub_solution = extract_subgrid(solution[_t+i], top_left, bottom_right)
                city.update_city(solution[_t+i], True)
                neighborhood.update_neighborhood(sub_solution)
                neighborhood.print(sub_solution)
                print(neighborhood.get_state())
            break





if __name__ == "__main__":
    # load_data()
    # plot_result()
    test_neighborhood()
    m = 12
    n = 12
    num_cars = 20

    # city = City.generate_city(n, m, num_cars)
    # print_path(city)
    # print("###### Test 1: ######")
    # print(f"m = {m}, n = {n}, num_cars = {num_cars}:\n")
    # while 0 != city.active_cars_amount():
    #     rand_traffic = np.random.choice(list(Direction), size=(n, m))
    #     city.update_city(rand_traffic, True)
    #     print("###### next step: ######")
    #     print(f"waiting time: {city.get_current_avg_wait_time()}")
    # print("\n\n")