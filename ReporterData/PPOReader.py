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
    data_moving = np.load(f'PPOResults/moving_cars_amount.npy').flatten()
    data_not_reaching = np.load(f'PPOResults/not_reaching_cars.npy').flatten()
    data_wait_punishment = np.load(f'PPOResults/wait_time_punishment.npy').flatten()
    data_avg_wait_time = np.load(f'PPOResults/wait_times_check.npy').flatten()
    data_best = np.load(f'PPOResults/best_solutions.npy', allow_pickle=True)

    data_moving = process_moving(data_moving)
    data_avg_wait_time = process_avg_wait_time(data_avg_wait_time)
    data_wait_punishment = process_punishment(data_wait_punishment)
    data_not_reaching = data_not_reaching['cars_num']

    return data_moving, data_not_reaching, data_wait_punishment, data_avg_wait_time, data_best

def plot_data(y_values, color, title, ylabel):
    """Plot a single dataset with baseline value and a moving average."""
    x_values = range(len(y_values))

    # Calculate moving average
    moving_avg = np.convolve(y_values, np.ones(50)/50, mode='valid')  # Adjust the window size (10) as needed

    plt.figure()
    plt.plot(x_values, y_values, label='PPO Algorithm', color=color)
    plt.plot(range(len(moving_avg)), moving_avg, label='Average Value', color='black', linestyle='--')
    plt.legend()
    plt.xlabel('Learning Iterations Over Cities')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

def seperation(i, j, last_solution, direction):
    print(f"junction ({i},{j}) {direction}")
    junction_over_time = last_solution[:, i, j]
    horizontal_count = np.sum(junction_over_time == Direction.HORIZONTAL)
    vertical_count = np.sum(junction_over_time == Direction.VERTICAL)
    print(f'horizontal_count = {horizontal_count}')
    print(f'vertical_count = {vertical_count}')


def plot_score(data_moving, data_not_reaching, data_wait_punishment, data_avg_wait_time):
    # Calculate the evaluation score
    evaluation_scores = evaluate_data(data_moving, data_not_reaching, data_wait_punishment, data_avg_wait_time, t, m, n)
    moving_avg = np.convolve(evaluation_scores, np.ones(50)/50, mode='valid')

    # Plotting the evaluation scores
    plt.plot(evaluation_scores, color='#FFB6C1', label='PPO Algorithm')
    plt.plot(range(len(moving_avg)), moving_avg, label='Average Value', color='black', linestyle='--')
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


def main():
    """Main function to load data and generate plots."""
    data_moving, data_not_reaching, data_wait_punishment, data_avg_wait_time, data_best = load_data()

    plot_score(data_moving, data_not_reaching, data_wait_punishment, data_avg_wait_time)
    plot_data(data_moving, '#87CEFA',  'General Traffic Flow', 'Number Of Cars That Moved')
    plot_data(data_not_reaching, '#B2D8D8', 'How Many Cars Were Late', 'Number Of Cars')
    plot_data(data_wait_punishment, '#98FB98', 'Car Starvation Punishment', 'Average Car Starvation Punishment')
    plot_data(data_avg_wait_time, '#FFA07A', 'Average Car Wait Time', 'Average Time')


if __name__ == "__main__":
    main()

