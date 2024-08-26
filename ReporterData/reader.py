import numpy as np
from matplotlib import pyplot as plt

from Model.City import City
from Model.Direction import Direction

m = 8
n = 8
t = 40
num_cars = 350

def plot_direction_counts(junction_data):
    """
    Plots a bar chart showing the counts of horizontal and vertical directions
    at each junction.

    :param junction_data: List of tuples containing junction coordinates and their direction counts.
                          Example: [((i, j), horizontal_count, vertical_count), ...]
    """
    junctions = [f"({i},{j})" for (i, j), _, _ in junction_data]
    horizontal_counts = [horizontal for _, horizontal, _ in junction_data]
    vertical_counts = [vertical for _, _, vertical in junction_data]

    x = np.arange(len(junctions))  # Label locations
    width = 0.35  # Bar width

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, horizontal_counts, width, label='Horizontal')
    bars2 = ax.bar(x + width/2, vertical_counts, width, label='Vertical')

    ax.set_xlabel('Junction (i,j)')
    ax.set_ylabel('Count')
    ax.set_title('Traffic Direction Counts at Highway Junctions')
    ax.set_xticks(x)
    ax.set_xticklabels(junctions)
    ax.legend()

    # Add counts on top of bars
    ax.bar_label(bars1, padding=3)
    ax.bar_label(bars2, padding=3)

    fig.tight_layout()
    plt.show()


def highway_analyzing(data_best):
    for a in range(3):
        print(f'\na = {a}:')
        last_solution = data_best['solution'][-a]
        city = City.generate_city(n, m, num_cars)
        for i, junctions in enumerate(city.grid.junctions):
            for j, junction in enumerate(junctions):
                if junction.get_is_vertical_highway():
                    seperation(i, j, last_solution, 'vertical')
                if junction.get_is_horizontal_highway():
                    seperation(i, j, last_solution, 'horizontal')


def seperation(i, j, last_solution, direction):
    print(f"junction ({i},{j}) {direction}")
    junction_over_time = last_solution[:, i, j]
    horizontal_count = np.sum(junction_over_time == Direction.HORIZONTAL)
    vertical_count = np.sum(junction_over_time == Direction.VERTICAL)
    print(f'horizontal_count = {horizontal_count}')
    print(f'vertical_count = {vertical_count}')


def process_avg_wait_time(data_avg_wait_time):
    data_avg_wait_time = data_avg_wait_time['avg_wait_time'].flatten()
    return data_avg_wait_time * ((m * n) / num_cars)


def process_moving(data_moving):
    data_moving = data_moving['active_car'].flatten()
    return data_moving / t


def process_punishment(data_wait_punishment):
    data_wait_punishment = data_wait_punishment['wait_punishment'].flatten()
    return data_wait_punishment / (m * n)


def load_data(number):
    """Load the necessary data from .npy files."""
    data_moving = np.load(f'moving_cars_amount{number}.npy').flatten()
    data_not_reaching = np.load(f'not_reaching_cars{number}.npy').flatten()
    data_wait_punishment = np.load(f'wait_time_punishment{number}.npy').flatten()
    data_avg_wait_time = np.load(f'wait_times_check{number}.npy').flatten()
    data_best = np.load(f'best_solutions{number}.npy', allow_pickle=True)

    data_moving = process_moving(data_moving)
    data_avg_wait_time = process_avg_wait_time(data_avg_wait_time)
    data_wait_punishment = process_punishment(data_wait_punishment)

    return data_moving, data_not_reaching, data_wait_punishment, data_avg_wait_time, data_best

def plot_data(y_values, color, baseline_value, title, ylabel):
    """Plot a single dataset with baseline value."""
    x_values = range(len(y_values))
    plt.figure()
    plt.plot(x_values, y_values, label='Genetic Algorithm', color=color)
    plt.axhline(y=baseline_value, color='red', linestyle='--', label='Baseline Solution')
    plt.legend()
    plt.xlabel('Generation')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

def plot_fitness(data_best):
    """Plot the best fitness values over generations."""
    x_values = range(len(data_best))
    fitness_values = data_best['fitness'].flatten()
    plt.figure()
    plt.plot(x_values, fitness_values, label='Genetic Algorithm')
    plt.axhline(y=2.6062604, color='red', linestyle='--', label='Baseline Solution')
    plt.legend()
    plt.title('Best Fitness Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness Score')
    plt.grid(True)
    plt.show()

def main():
    """Main function to load data and generate plots."""
    number = 90
    data_moving, data_not_reaching, data_wait_punishment, data_avg_wait_time, data_best = load_data(number)

    plot_data(data_moving, 'blue', 92.95, 'General Traffic Flow', 'Number Of Cars That Moved')
    plot_data(data_not_reaching, 'purple', 128, 'How Many Cars Were Late', 'Number Of Cars')
    plot_data(data_wait_punishment, 'green', 1548.25, 'Car Starvation Punishment', 'Average Car Starvation Punishment')
    plot_data(data_avg_wait_time, 'orange', 29.622, 'Average Car Wait Time', 'Average Time')

    # plot_fitness(data_best)
    highway_analyzing(data_best)
    # 3 random highway
    junction_data = [((2, 3), 32, 8), ((2, 4), 31, 9), ((3, 5), 18, 22)]
    plot_direction_counts(junction_data)

if __name__ == "__main__":
    main()
