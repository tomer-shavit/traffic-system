from matplotlib import pyplot as plt

from City import City
from GeneticSolver import GeneticSolver
from Reporter import Reporter

population_size = 600
n = 8
m = 8
t = 40


mutation_rate = 0.01
generations = 200
temperature = 0.001

num_cities = 10
num_cars = 200
reporter = Reporter()

solver = GeneticSolver(population_size, mutation_rate, generations, n, m, t, reporter, temperature)
best_solution = solver.solve(num_cities, num_cars)
solver.plot_best_fitness(reporter.best_solutions['fitness'])
reporter.save_all_data('./ReporterData')

# print the best solution:
city = City.generate_city(n, m, num_cars)
for _t in range(t):
    city.update_city(best_solution[_t], True)

print("!!! Neta, Ido and Tomer!!! Don't Forget to change the name of the files in ReopterData directory!!!!!")


