import numpy as np
from matplotlib import pyplot as plt
from Direction import Direction

# Load the .npy file
data_moving = np.load('moving_cars_amount494.npy')
data_not_reaching = np.load('not_reaching_cars494.npy')
data_wait_punishment = np.load('wait_time_punishment494.npy')
data_wait_check = np.load('wait_times_check494.npy')
data_best = np.load('best_solutions494.npy', allow_pickle=True)

# Generate x values corresponding to the number of generations (1 to 150)
x_values = range(1, 151)

# Flatten the data arrays, as they contain tuples with one element
data_moving = data_moving.flatten()
data_not_reaching = data_not_reaching.flatten()
data_wait_punishment = data_wait_punishment.flatten()
data_wait_check = data_wait_check.flatten()

# Plot each dataset
plt.figure(figsize=(12, 8))

# Plot for moving cars amount
plt.subplot(2, 2, 1)
plt.plot(x_values, data_moving, label='Moving Cars Amount', color='blue')
plt.xlabel('Generation')
plt.ylabel('Value')
plt.title('Moving Cars Amount')
plt.grid(True)

# Plot for not reaching cars
plt.subplot(2, 2, 2)
plt.plot(x_values, data_not_reaching, label='Not Reaching Cars', color='red')
plt.xlabel('Generation')
plt.ylabel('Value')
plt.title('Not Reaching Cars')
plt.grid(True)

# Plot for wait time punishment
plt.subplot(2, 2, 3)
plt.plot(x_values, data_wait_punishment, label='Wait Time Punishment', color='green')
plt.xlabel('Generation')
plt.ylabel('Value')
plt.title('Wait Time Punishment')
plt.grid(True)

# Plot for wait times check
plt.subplot(2, 2, 4)
plt.plot(x_values, data_wait_check, label='Wait Times Check', color='orange')
plt.xlabel('Generation')
plt.ylabel('Value')
plt.title('Wait Times Check')
plt.grid(True)

# Adjust layout and show the plot
plt.tight_layout()
plt.show()