# Traffic System

Simulates morning rush-hour traffic on a city grid and optimizes traffic light timing using Genetic Algorithms and Proximal Policy Optimization (PPO).

## The Problem

Cars depart from residential zones and commute to industrial zones across a grid of junctions, each controlled by a traffic light (horizontal or vertical). The goal is to find the optimal light configuration at every junction for every time step to minimize average wait times, maximize throughput, and get all cars to their destinations.

## Approach

Three solvers are compared:

| Solver | Strategy | How It Works |
|--------|----------|-------------|
| **Baseline** | Alternating | Switches all lights between horizontal and vertical every tick |
| **Genetic Algorithm** | Evolutionary | Evolves a population of full `(t, n, m)` solutions via tournament selection, crossover, and mutation |
| **PPO (Reinforcement Learning)** | Policy gradient | Trains an actor-critic agent on 3x3 neighborhoods; aggregates local decisions via voting for the global assignment |

### Fitness Function

Solutions are scored on four normalized metrics:
- Cars that reached their destination
- Average wait time across junctions
- Total car movements (throughput)
- Wait time punishment (penalizes long queues quadratically)

## City Model

```
Residential zones (top-left)          Industrial zones (bottom-right)
    [R] -- [R] -- [ ] -- [ ]             [ ] -- [ ] -- [I] -- [I]
     |      |      |      |               |      |      |      |
    [R] -- [R] -- [ ] -- [ ]   . . .     [ ] -- [ ] -- [I] -- [I]
     |      |      |      |               |      |      |      |
    [ ] -- [ ] -- [ ] -- [ ]             [ ] -- [ ] -- [ ] -- [ ]

Each [ ] is a junction with a traffic light (H or V direction).
Cars navigate from R → I using shortest paths.
```

- **Grid**: `n x m` junctions, each with a traffic light
- **Cars**: spawn in residential area with normally distributed departure times, route toward industrial area
- **Traffic lights**: binary state (horizontal or vertical) updated each tick
- **Highways**: some junctions allow only one direction

## Project Structure

```
Model/
├── City.py            # City simulation (grid, cars, neighborhoods)
├── Grid.py            # Junction grid with car movement logic
├── Junction.py        # Single junction with traffic light + queue
├── TrafficLight.py    # Light state (horizontal/vertical)
├── TrafficSystem.py   # Applies light assignments to the grid
├── Car.py             # Car with source, destination, pathfinding
├── Coordinate.py      # (x, y) helper
├── Neighborhood.py    # 3x3 sub-grid for PPO local observation
├── Direction.py       # Enum: HORIZONTAL, VERTICAL
└── Reporter.py        # Metrics recording and serialization

Solvers/
├── Solver.py          # Abstract base with evaluation + normalization
├── BaseLineSolver.py  # Alternating baseline
├── GeneticSolver.py   # Genetic algorithm
└── PPOSolver.py       # PPO with neighborhood-based observations

PPO/
├── Agent.py           # PPO agent (actor-critic, GAE advantages)
├── ActorNetwork.py    # Policy network (PyTorch)
├── CriticNetwork.py   # Value network (PyTorch)
└── PPOMemory.py       # Experience buffer with mini-batch sampling

Tests/
├── BaseLineTest.py    # Run baseline solver
├── GATest.py          # Train genetic algorithm
└── PPOTest.py         # Train PPO agent

ReporterData/
├── GenReader.py       # Plot GA training results
└── PPOReader.py       # Plot PPO training results
```

## Setup

### Prerequisites

- Python 3.10+
- pip

### Install

```bash
pip install -r requirements.txt
```

Key dependencies: **NumPy**, **PyTorch**, **Matplotlib**

## Usage

### Run the Baseline

```bash
python Tests/BaseLineTest.py
```

### Train the Genetic Algorithm

```bash
python Tests/GATest.py
```

Default config: 8x8 grid, 350 cars, 10 cities, 600 population, 200 generations.

### Train PPO

```bash
python Tests/PPOTest.py
```

### Plot Results

```bash
python ReporterData/GenReader.py   # GA graphs
python ReporterData/PPOReader.py   # PPO graphs
```

Results are saved to `ReporterData/`.

## Default Parameters

| Parameter | GA | PPO |
|-----------|-----|-----|
| Grid size | 8x8 | 8x8 |
| Time steps | 40 | 40 |
| Cars | 350 | 350 |
| Population / Cities | 600 / 10 | — / 10 |
| Generations / Epochs | 200 | 5 |
| Mutation rate | 0.025 | — |
| Neighborhood size | — | 3x3 |
| Batch size | — | 20 |
| Learning rate | — | 0.0003 |
| GAE lambda | — | 0.95 |
| Policy clip | — | 0.2 |
