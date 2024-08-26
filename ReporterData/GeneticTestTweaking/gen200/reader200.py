import numpy as np
from matplotlib import pyplot as plt

# Load the .npy file
number = 669
data_moving = np.load(f'moving_cars_amount{number}.npy')
data_not_reaching = np.load(f'not_reaching_cars{number}.npy')
data_wait_punishment = np.load(f'wait_time_punishment{number}.npy')
data_wait_check = np.load(f'wait_times_check{number}.npy')
data_best = np.load(f'best_solutions{number}.npy', allow_pickle=True)

# # Generate x values corresponding to the number of generations (1 to 150)
x_values = range(1, 201)
#
# Flatten the data arrays, as they contain tuples with one element
data_moving = data_moving.flatten()
data_not_reaching = data_not_reaching.flatten()
data_wait_punishment = data_wait_punishment.flatten()
data_wait_check = data_wait_check.flatten()

# Plot each dataset
plt.figure()
plt.plot(x_values, data_moving, label='Moving Cars Amount', color='blue')
baseline_value = 3718
plt.axhline(y=baseline_value, color='red', linestyle='--', label='Baseline Solution')
plt.legend()
plt.xlabel('Generation')
plt.ylabel('Value')
plt.title('Moving Cars Amount')
plt.grid(True)
plt.show()

plt.figure()
plt.plot(x_values, data_not_reaching, label='Not Reaching Cars', color='red')
baseline_value = 128
plt.axhline(y=baseline_value, color='red', linestyle='--', label='Baseline Solution')
plt.legend()
plt.xlabel('Generation')
plt.ylabel('Value')
plt.title('Not Reaching Cars')
plt.grid(True)
plt.show()

plt.figure()
plt.plot(x_values, data_wait_punishment, label='Wait Time Punishment', color='green')
baseline_value = 99088
plt.axhline(y=baseline_value, color='red', linestyle='--', label='Baseline Solution')
plt.legend()
plt.xlabel('Generation')
plt.ylabel('Value')
plt.title('Wait Time Punishment')
plt.grid(True)
plt.show()

plt.figure()
plt.plot(x_values, data_wait_check, label='Average wait time', color='orange')
baseline_value = 162
plt.axhline(y=baseline_value, color='red', linestyle='--', label='Baseline Solution')
plt.legend()
plt.xlabel('Generation')
plt.ylabel('Value')
plt.title('Average Wait Time')
plt.grid(True)
plt.show()


x_values = range(1, 202)
fitness_values = data_best['fitness'].flatten()
plt.figure()
plt.plot(x_values, fitness_values, marker='o', markersize=2, label='Genetic Algorithm')
baseline_value = 2.6062604
plt.axhline(y=baseline_value, color='red', linestyle='--', label='Baseline Solution')
plt.legend()
plt.title('Best Fitness Over Generations - High Mutation Rate')
plt.xlabel('Generation')
plt.ylabel('Best Fitness Score')
plt.grid(True)
plt.show()

