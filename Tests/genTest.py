from Model.City import City
from Solvers.GeneticSolver import GeneticSolver
from Model.Reporter import Reporter

n = 8
m = 8
t = 40
num_cities = 10
num_cars = 350

population_size = 600
mutation_rate = 0.025
generations = 200
temperature = 0.001

reporter = Reporter()

solver = GeneticSolver(population_size, mutation_rate, generations, n, m, t, reporter, temperature)
best_solution = solver.solve(num_cities, num_cars)
solver.plot_best_fitness(reporter.best_solutions['fitness'])
reporter.save_all_data('./ReporterData')

# print the best solution:
city = City.generate_city(n, m, num_cars)
for _t in range(t):
    city.update_city(best_solution[_t], True)


