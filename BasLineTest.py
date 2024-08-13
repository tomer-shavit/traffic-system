from matplotlib import pyplot as plt

from BaseLineSolver import BaseLineSolver
from City import City
from Reporter import Reporter

population_size = 100
n = 10
m = 10
t = 40

num_cities = 10
num_cars = 200
reporter = Reporter()
solver = BaseLineSolver(n, m, t, reporter)
solution = solver.solve()

cities = City.generate_cities(n,m, num_cars, num_cities)
print(f"Evaluation for baseline= {solver.evaluate_solution(solution, cities)}")

#
plt.figure(figsize=(10, 6))
plt.plot(reporter.all_cars_arrive_time['time'], marker='o')
plt.title('Best Fitness Over Generations')
plt.xlabel('Cities')
plt.ylabel('Final car arrival time')
plt.grid(True)
plt.show()