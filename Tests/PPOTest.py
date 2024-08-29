from Solvers.PPOSolver import PPOSolver
from Model.Reporter import Reporter


n = 8
m = 8
t = 40
num_cars = 350
num_training_cities = 1000

reporter = Reporter()

solver = PPOSolver(n, m, t, reporter)

if __name__ == "__main__":
    print("Training the solver...")
    solver.train(num_training_cities, num_cars)
    reporter.save_all_data('../ReporterData/PPO', 'PPO')
    print("Training completed.")
