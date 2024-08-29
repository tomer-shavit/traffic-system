import numpy as np
from typing import List
import matplotlib.pyplot as plt
from Model.City import City
from Model.Direction import Direction
from Model.Reporter import Reporter
from Solvers.Solver import Solver


class GeneticSolver(Solver):
    """
    GeneticSolver is a class that implements a genetic algorithm to optimize traffic light configurations in a city grid.
    The goal is to minimize the average waiting time for cars across multiple city scenarios.
    """

    def __init__(self, population_size: int, mutation_rate: float, generations: int, n: int, m: int, t: int,
                 reporter: Reporter):
        """
        Initializes the GeneticSolver with the necessary parameters.
        - population_size (int): The number of solutions in each generation's population.
        - mutation_rate (float): The probability of a mutation occurring at each gene in a solution.
        - generations (int): The number of generations to evolve the population.
        """
        super().__init__(n, m, t, reporter)
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations

    def generate_random_solution(self) -> np.ndarray:
        """
        Generates a random solution, which is a 3D array representing the traffic light directions
        (Horizontal or Vertical) for each junction at each time step.

        Returns:
        - np.ndarray: A (t, n, m) array where each element is either Direction.HORIZONTAL or Direction.VERTICAL.
        """
        return np.random.choice([Direction.HORIZONTAL, Direction.VERTICAL], size=(self.t, self.n, self.m))

    def uniform_crossover(self, parent1: np.ndarray, parent2: np.ndarray) -> np.ndarray:
        """
        Performs uniform crossover between two parent solutions to produce a child solution.

        Parameters:
        - parent1 (np.ndarray): The first parent solution.
        - parent2 (np.ndarray): The second parent solution.

        Returns:
        - np.ndarray: A new child solution generated by combining parts of parent1 and parent2.
        """
        mask = np.random.rand(*parent1.shape) < 0.5  # Create a mask with 50% chance for each gene
        child = np.where(mask, parent1, parent2)  # Choose genes from parent1 or parent2 based on mask
        return child

    def mutate(self, solution: np.ndarray) -> np.ndarray:
        """
        Mutates a given solution by flipping the direction of traffic lights at random locations based on the
        mutation rate.

        Parameters:
        - solution (np.ndarray): The solution to be mutated.

        Returns:
        - np.ndarray: The mutated solution.
        """
        mutation_mask = np.random.random(solution.shape) < self.mutation_rate
        # Directly flip the directions using boolean indexing
        solution[mutation_mask & (solution == Direction.HORIZONTAL)] = Direction.VERTICAL
        solution[mutation_mask & (solution == Direction.VERTICAL)] = Direction.HORIZONTAL
        return solution

    def create_children(self, parents: np.ndarray) -> np.ndarray:
        """
        Creates a new population of offspring by performing crossover and mutation on the parent solutions.

        Parameters:
        - parents (np.ndarray): The parent solutions selected for reproduction.

        Returns:
        - np.ndarray: A new population of offspring solutions.
        """
        children = np.empty((self.population_size, self.t, self.n, self.m), dtype=object)
        for i in range(0, self.population_size, 2):
            parent1, parent2 = np.random.choice(len(parents), 2, replace=False)
            child1 = self.uniform_crossover(parents[parent1], parents[parent2])
            child2 = self.uniform_crossover(parents[parent2], parents[parent1])
            children[i, :, :, :] = self.mutate(child1)
            children[i + 1, :, :, :] = self.mutate(child2)

        return children

    def tournament_selection(self, population: np.ndarray, fitness_scores: np.ndarray,
                             tournament_size: int = 50) -> np.ndarray:
        """
        Selects parents using tournament selection.

        Parameters:
        - population (np.ndarray): The current population of solutions.
        - fitness_scores (np.ndarray): The fitness scores of the current population.
        - tournament_size (int): The number of individuals in each tournament.

        Returns:
        - np.ndarray: The selected parent solutions.
        """
        selected_parents = []
        for _ in range(self.population_size):
            tournament_indices = np.random.choice(len(population), size=tournament_size, replace=False)
            tournament_fitness = fitness_scores[tournament_indices]
            best_index = tournament_indices[np.argmax(tournament_fitness)]
            selected_parents.append(population[best_index])

        return np.array(selected_parents)

    def solve(self, num_cities: int, num_cars: int) -> np.ndarray:
        """
        Runs the genetic algorithm to find the optimal traffic light configuration that minimizes average car waiting times.
        For each generation, it creates new random cities to evaluate the solutions.

        Parameters:
        - num_cities (int): The number of cities to generate and evaluate for each generation.
        - num_cars (int): The number of cars to simulate in each city.

        Returns:
        - np.ndarray: The best solution found after all generations.
        """
        population = self.initialize_population()
        cities = self.generate_cities_for_generation(num_cities, num_cars)
        for generation in range(self.generations):
            fitness_scores = self.evaluate_population(population, cities)
            best_solution, best_fitness = self.find_best_solution(population, fitness_scores)

            print(f"Generation {generation + 1}: Best fitness = {best_fitness}")

            parents = self.tournament_selection(population, fitness_scores)
            children = self.create_children(parents)
            population = self.add_best_to_children(children, best_solution)
            self.report_best_solution(best_solution, cities)
            self.reporter.record_generations_best_solutions(best_fitness, best_solution)

        best_final_solution, best_final_fitness = self.find_best_solution(population, fitness_scores)
        self.reporter.record_generations_best_solutions(best_final_fitness, best_final_solution)

        print(f"Final Best Fitness: {best_final_fitness}")

        return best_final_solution

    def report_best_solution(self, best_solution, cities):
        self.evaluate_solution(best_solution, cities, report=True)

    def initialize_population(self) -> np.ndarray:
        """Initializes the population with random solutions."""
        return np.array([self.generate_random_solution() for _ in range(self.population_size)])

    def generate_cities_for_generation(self, num_cities: int, num_cars: int) -> list:
        """Generates a new set of random cities for this generation."""
        return City.generate_cities(self.n, self.m, num_cars, num_cities)

    def evaluate_population(self, population: np.ndarray, cities: List[City]) -> np.ndarray:
        """Evaluates the fitness of each solution in the population."""
        return np.array([self.evaluate_solution(solution, cities) for solution in population])

    def find_best_solution(self, population: np.ndarray, fitness_scores: np.ndarray) -> tuple:
        """Finds the best solution and its fitness in the current population."""
        best_index = np.argmax(fitness_scores)
        return population[best_index], fitness_scores[best_index]

    def add_best_to_children(self, children: np.ndarray, best_solution: np.ndarray) -> np.ndarray:
        """replace a random children with the best solution."""
        random_index = np.random.randint(0, len(children))
        return np.concatenate(
            (children[:random_index], children[random_index + 1:], best_solution.reshape(1, self.t, self.n, self.m)))

    def plot_best_fitness(self, fitness_values):
        """
        Plots the best fitness value in each generation.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(fitness_values, marker='o')
        plt.title('Best Fitness Over Generations')
        plt.xlabel('Generation')
        plt.ylabel('Fitness (lower is better)')
        plt.grid(True)
        plt.show()
