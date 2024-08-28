from Solvers.PPOSolver import PPOSolver
from Model.Reporter import Reporter


n = 8  # City width
m = 8  # City height
t = 40  # Max time steps
num_cars = 350  # Number of cars per city
num_training_cities = 100  # Number of cities to train on

reporter = Reporter()

solver = PPOSolver(n, m, t, reporter)

if __name__ == "__main__":
    # Train the solver
    print("Training the solver...")
    solver.train(num_training_cities, num_cars)
    print("Training completed.")