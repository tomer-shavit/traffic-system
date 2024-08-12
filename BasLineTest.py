from BaseLineSolver import BaseLineSolver
from City import City


population_size = 100
n = 10
m = 10
t = 30


mutation_rate = 0.005
generations = 10000

num_cities = 10
num_cars = 50

solver = BaseLineSolver(n, m, t)
solution = solver.solve()

cities = City.generate_cities(n,m, num_cars, num_cities)
print(f"Evaluation for baseline= {solver.evaluate_solution(solution, cities)}")

