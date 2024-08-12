from GeneticSolver import GeneticSolver
from Reporter import Reporter

population_size = 100
n = 10
m = 10
t = 30


mutation_rate = 0.005
generations = 10000

num_cities = 10
num_cars = 50
reporter = Reporter()

solver = GeneticSolver(population_size, reporter, mutation_rate, generations, n, m, t)
best_solution = solver.solve(num_cities, num_cars)
solver.plot_fitness_history()


