from matplotlib import pyplot as plt

from GeneticSolver import GeneticSolver
from Reporter import Reporter

population_size = 600
n = 8
m = 8
t = 30


mutation_rate = 0.01
generations = 300
temperature = 0.001

num_cities = 10
num_cars = 200
reporter = Reporter()

solver = GeneticSolver(population_size, mutation_rate, generations, n, m, t, reporter, temperature)
best_solution = solver.solve(num_cities, num_cars)
solver.plot_best_fitness(reporter.best_solutions['fitness'])


# plt.figure(figsize=(10, 6))
# plt.plot(reporter.all_cars_arrive_time['time'], marker='o')
# plt.title('Time of all cars arrived')
# plt.xlabel('Iteration')
# plt.ylabel('Time')
# plt.grid(True)
# plt.show()
#
#
