# Traffic System

## Grid Shape (m, n)

The grid is structured as follows:

- `m` represents the number of columns (indexed by `j`)
- `n` represents the number of rows (indexed by `i`)

## Matrix Representation

Here is a visual representation of the matrix:

|       | **j = 0** | **j = 1** | **...** | **j = m-1** |
|-------|:---------:|:---------:|:-------:|:-----------:|
| **i = 0** | (0, 0)   | (0, 1)   | ...     | (0, m-1)     |
| **i = 1** | (1, 0)   | (1, 1)   | ...     | (1, m-1)     |
| **...**   | ...      | ...      | ...     | ...          |
| **i = n-1** | (n-1, 0) | (n-1, 1) | ...     | (n-1, m-1)   |

- Each cell `(i, j)` in the table corresponds to the grid coordinates.
- The top-left corner of the grid is `(0, 0)`, and the bottom-right corner is `(n-1, m-1)`.

## Assumptions 
1. The size of the city is at least 4X4

## Hyper Parameters
1. size of the city: m, n 
2. Total time for a single run: t
3. Num of cars
4. Num of cities

### Genetic algorithm
1. population_size: The number of solutions in each generation's population.
2. Mutation rate: The probability of a mutation occurring at each gene in a solution.
3. generations: The number of generations to evolve the population.

### PPO
1. Neighborhood Size: The dimensions of the neighborhood grid. A 3x3 neighborhood is small enough to be computationally manageable but still complex enough to model various traffic patterns.
2. BATCH_SIZE: How many experiences are included in each mini-batch during the training process

