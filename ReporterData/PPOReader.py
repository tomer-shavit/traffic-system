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


def load_data(number):
    """Load the necessary data from .npy files."""
    data_moving = np.load(f'PPO/moving_cars_amount{number}.npy').flatten()
    data_not_reaching = np.load(f'PPO/not_reaching_cars{number}.npy').flatten()
    data_wait_punishment = np.load(f'PPO/wait_time_punishment{number}.npy').flatten()
    data_avg_wait_time = np.load(f'PPO/wait_times_check{number}.npy').flatten()
    data_best = np.load(f'PPO/best_solutions{number}.npy', allow_pickle=True)

    data_moving = process_moving(data_moving)
    data_avg_wait_time = process_avg_wait_time(data_avg_wait_time)
    data_wait_punishment = process_punishment(data_wait_punishment)
    data_not_reaching = data_not_reaching['cars_num']

    return data_moving, data_not_reaching, data_wait_punishment, data_avg_wait_time, data_best

def plot_data(y_values, color, baseline_value, title, ylabel):
    """Plot a single dataset with baseline value and a moving average."""
    x_values = range(len(y_values))

    # Calculate moving average
    moving_avg = np.convolve(y_values, np.ones(50)/50, mode='valid')  # Adjust the window size (10) as needed

    plt.figure()
    plt.plot(x_values, y_values, label='PPO Algorithm', color=color)
    plt.plot(range(len(moving_avg)), moving_avg, label='Average Value', color='black', linestyle='--')
    plt.axhline(y=baseline_value, color='red', linestyle='--', label='Baseline Solution')
    plt.legend()
    plt.xlabel('Learning Iterations Over Cities')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

def highway_analyzing(data_best):
    solutions = data_best['solution']
    for a in range(500):
        if solutions[-a].shape == (40, 8, 8):
            print(f'\na = {a}:')
            last_solution = solutions[-a]
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

def plot_score(data_moving, data_not_reaching, data_wait_punishment, data_avg_wait_time):
    n, m, t = 8, 8, 40

    # Calculate the evaluation score
    evaluation_scores = evaluate_data(data_moving, data_not_reaching, data_wait_punishment, data_avg_wait_time, t, m, n)
    moving_avg = np.convolve(evaluation_scores, np.ones(50)/50, mode='valid')

    # Plotting the evaluation scores
    plt.plot(evaluation_scores, color='#FFB6C1', label='PPO Algorithm')
    plt.plot(range(len(moving_avg)), moving_avg, label='Average Value', color='black', linestyle='--')
    plt.axhline(y=2.6062604, color='red', linestyle='--', label='Baseline Solution')
    plt.legend()
    plt.xlabel('Learning Iterations Over Cities')
    plt.ylabel('Score')
    plt.title('Evaluation Score Over Time')
    plt.legend()
    plt.show()

def evaluate_data(data_moving, data_not_reaching, data_wait_punishment, data_avg_wait_time, t, m, n):
    cars_amount = 350
    score_not_reaching = normalize_not_reaching_cars(data_not_reaching, cars_amount)
    score_avg_wait_time = normalize_avg_wait_time(data_avg_wait_time, cars_amount, t, m, n)
    score_moving_cars = normalize_moving_cars_amount(data_moving, cars_amount, t)
    score_wait_time_punishment = normalize_wait_time_punishment(data_wait_punishment, cars_amount, t)

    return (score_not_reaching + score_avg_wait_time + score_moving_cars + score_wait_time_punishment)

def normalize_not_reaching_cars(not_reaching_cars, cars_amount):
    max_cars = cars_amount
    normalized_not_reaching_cars = not_reaching_cars / max_cars
    return 1 / (1 + normalized_not_reaching_cars)

def normalize_avg_wait_time(total_avg_wait_time, cars_amount, t, m, n):
    max_waiting_cars = t * cars_amount / (m * n)
    normalized_total_avg_wait_time = total_avg_wait_time / max_waiting_cars
    return 1 / (1 + normalized_total_avg_wait_time)

def normalize_moving_cars_amount(moving_cars_amount, cars_amount, t):
    max_moving_cars =  cars_amount * t
    return moving_cars_amount / max_moving_cars

def normalize_wait_time_punishment(wait_time_punishment, cars_amount, t):
    max_punishment = (t * cars_amount ) ** 2
    normalized_total_wait_time_punishment = wait_time_punishment / max_punishment
    return 1 / (1 + normalized_total_wait_time_punishment)


def plot_direction_counts(junction_data, x_label):
    """
    Plots a bar chart showing the counts of horizontal and vertical directions
    at each junction.

    :param junction_data: List of tuples containing junction coordinates and their direction counts.
                          Example: [((i, j), horizontal_count, vertical_count), ...]
    """
    junctions = [name for name, _, _ in junction_data]
    horizontal_counts = [horizontal for _, horizontal, _ in junction_data]
    vertical_counts = [vertical for _, _, vertical in junction_data]

    x = np.arange(len(junctions))  # Label locations
    width = 0.35  # Bar width

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, horizontal_counts, width, label='Horizontal')
    bars2 = ax.bar(x + width/2, vertical_counts, width, label='Vertical')

    ax.set_xlabel(x_label)
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


def main():
    """Main function to load data and generate plots."""
    number = 555
    data_moving, data_not_reaching, data_wait_punishment, data_avg_wait_time, data_best = load_data(number)
    highway_analyzing(data_best)
    junction_data = [('GA', 32, 8), ('PPO', 31, 9), ('Baseline', 20, 20)]
    plot_direction_counts(junction_data, 'Junction (2,3) An Horizontal Highway Junction')

    junction_data = [('GA', 20, 20), ('PPO', 15, 25), ('Baseline', 20, 20)]
    plot_direction_counts(junction_data, 'Junction (4,5) A Vertical Highway Junction')

    plot_score(data_moving, data_not_reaching, data_wait_punishment, data_avg_wait_time)

    plot_data(data_moving, '#87CEFA', 92.95, 'General Traffic Flow', 'Number Of Cars That Moved')
    plot_data(data_not_reaching, '#B2D8D8', 128, 'How Many Cars Were Late', 'Number Of Cars')
    plot_data(data_wait_punishment, '#98FB98', 1548.25, 'Car Starvation Punishment', 'Average Car Starvation Punishment')
    plot_data(data_avg_wait_time, '#FFA07A', 29.622, 'Average Car Wait Time', 'Average Time')


if __name__ == "__main__":
    main()

