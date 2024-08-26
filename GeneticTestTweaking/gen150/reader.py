import numpy as np
from matplotlib import pyplot as plt
m = 8
n = 8
num_cars = 350


def process_avg_wait_time(data_avg_wait_time):
    data_avg_wait_time = data_avg_wait_time['avg_wait_time'].flatten()
    return data_avg_wait_time * ((m * n) / num_cars)


def load_data(number):
    """Load the necessary data from .npy files."""
    data_moving = np.load(f'moving_cars_amount{number}.npy').flatten()
    data_not_reaching = np.load(f'not_reaching_cars{number}.npy').flatten()
    data_wait_punishment = np.load(f'wait_time_punishment{number}.npy').flatten()
    data_avg_wait_time = np.load(f'wait_times_check{number}.npy').flatten()
    data_best = np.load(f'best_solutions{number}.npy', allow_pickle=True)

    data_avg_wait_time = process_avg_wait_time(data_avg_wait_time)

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
    plt.plot(x_values, fitness_values, marker='o', markersize=2, label='Genetic Algorithm')
    plt.axhline(y=2.6062604, color='red', linestyle='--', label='Baseline Solution')
    plt.legend()
    plt.title('Best Fitness Over Generations - High Mutation Rate')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness Score')
    plt.grid(True)
    plt.show()

def main():
    """Main function to load data and generate plots."""
    number = 494
    data_moving, data_not_reaching, data_wait_punishment, data_avg_wait_time, data_best = load_data(number)

    plot_data(data_moving, 'blue', 3718, 'Moving Cars Amount', 'Value')
    plot_data(data_not_reaching, 'red', 128, 'How Many Cars Arrived', 'Number Of Cars')
    plot_data(data_wait_punishment, 'green', 99088, 'Wait Time Punishment', 'Time')
    plot_data(data_avg_wait_time, 'orange', 29.622, 'Average Wait Time', 'Average Time')

    plot_fitness(data_best)

if __name__ == "__main__":
    main()
