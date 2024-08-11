from GeneticSolver import GeneticSolver
population_size = 100
n = 4
m = 4
t = 15

mutation_rate = 0.005
generations = 1000
num_cities = 10
num_cars = 100

solver = GeneticSolver(population_size, mutation_rate, generations, n, m, t)
solver.solve(num_cities, num_cars)

