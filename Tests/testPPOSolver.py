from Solvers.PPOSolver import PPOSolver
from Model.Reporter import Reporter

n = 10  # City width
m = 10  # City height
t = 100  # Max time steps
num_cars = 50  # Number of cars per city
num_training_cities = 50  # Number of cities to train on

reporter = Reporter()

solver = PPOSolver(n, m, t, reporter)

if __name__ == "__main__":
    # Train the solver
    print("Training the solver...")
    solver.train(num_training_cities, num_cars)
    print("Training completed.")