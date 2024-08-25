import numpy as np
from matplotlib import pyplot as plt
from BaseLineSolver import BaseLineSolver
from City import City
from Reporter import Reporter

n = 8
m = 8
t = 40
num_cities = 10
num_cars = 350

reporter = Reporter()
solver = BaseLineSolver(n, m, t, reporter)
solution = solver.solve()

cities = City.generate_cities(n,m, num_cars, num_cities)
print(f"Evaluation for baseline= {solver.evaluate_solution(solution, cities)}")

city = City.generate_city(n, m, num_cars)
for _t in range(t):
    city.update_city(solution[_t])

# Load the .npy file
number = 270
data_moving = np.load(f'Tests/moving_cars_amount{number}.npy')
data_not_reaching = np.load(f'Tests/not_reaching_cars{number}.npy')
data_wait_punishment = np.load(f'Tests/wait_time_punishment{number}.npy')
data_wait_check = np.load(f'Tests/wait_times_check{number}.npy')
data_solution = np.load(f'Tests/best_solutions{number}.npy', allow_pickle=True)
print(data_moving)
print(data_not_reaching)
print(data_wait_check)
print(data_wait_punishment)


#
# plt.figure(figsize=(10, 6))
# plt.plot(reporter.all_cars_arrive_time['time'], marker='o')
# plt.title('Best Fitness Over Generations')
# plt.xlabel('Cities')
# plt.ylabel('Final car arrival time')
# plt.grid(True)
# plt.show()