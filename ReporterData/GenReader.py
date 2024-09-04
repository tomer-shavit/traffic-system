import numpy as np
from matplotlib import pyplot as plt

from Model.City import City
from Model.Direction import Direction

m = 8
n = 8
t = 40
num_cars = 350


def process_avg_wait_time(data_avg_wait_time):
    data_avg_wait_time = data_avg_wait_time['avg_wait_time'].flatten()
    return data_avg_wait_time * ((m * n) / num_cars)


def process_moving(data_moving):
    data_moving = data_moving['active_car'].flatten()
    return data_moving / t


def process_punishment(data_wait_punishment):
    data_wait_punishment = data_wait_punishment['wait_punishment'].flatten()
    return data_wait_punishment / (m * n)


def load_data():
    """Load the necessary data from .npy files."""
    data_moving = np.load(f'GAResults/moving_cars_amount.npy').flatten()
    data_not_reaching = np.load(f'GAResults/not_reaching_cars.npy').flatten()
    data_wait_punishment = np.load(f'GAResults/wait_time_punishment.npy').flatten()
    data_avg_wait_time = np.load(f'GAResults/wait_times_check.npy').flatten()
    data_best = np.load(f'GAResults/best_solutions.npy', allow_pickle=True)

    data_moving = process_moving(data_moving)
    data_avg_wait_time = process_avg_wait_time(data_avg_wait_time)
    data_wait_punishment = process_punishment(data_wait_punishment)

    return data_moving, data_not_reaching, data_wait_punishment, data_avg_wait_time, data_best

def plot_data(y_values, color, title, ylabel):
    """Plot a single dataset with baseline value."""
    x_values = range(len(y_values))
    plt.figure()
    plt.plot(x_values, y_values, label='Genetic Algorithm', color=color)
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
    plt.legend()
    plt.title('Best Fitness Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness Score')
    plt.grid(True)
    plt.show()


def main():
    """Main function to load data and generate plots."""
    data_moving, data_not_reaching, data_wait_punishment, data_avg_wait_time, data_best = load_data()
    plot_data(data_moving, 'blue', 'General Traffic Flow', 'Number Of Cars That Moved')
    plot_data(data_not_reaching, 'purple', 'How Many Cars Were Late', 'Number Of Cars')
    plot_data(data_wait_punishment, 'green', 'Car Starvation Punishment', 'Average Car Starvation Punishment')
    plot_data(data_avg_wait_time, 'orange', 'Average Car Wait Time', 'Average Time')
    plot_fitness(data_best)


if __name__ == "__main__":
    main()
