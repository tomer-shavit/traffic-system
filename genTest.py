from matplotlib import pyplot as plt

from GeneticSolver import GeneticSolver
from Reporter import Reporter

population_size = 100
n = 10
m = 10
t = 40

mutation_rate = 0.005
generations = 200

num_cities = 10
num_cars = 200
reporter = Reporter()

solver = GeneticSolver(population_size, mutation_rate, generations, n, m, t, reporter)
best_solution = solver.solve(num_cities, num_cars)
solver.plot_best_fitness(reporter.best_solutions['fitness'])


plt.figure(figsize=(10, 6))
plt.plot(reporter.all_cars_arrive_time['time'], marker='o')
plt.title('Time of all cars arrived')
plt.xlabel('Iteration')
plt.ylabel('Time')
plt.grid(True)
plt.show()


