from Solvers.BaseLineSolver import BaseLineSolver
from Model.City import City
from Model.Reporter import Reporter

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