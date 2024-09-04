
# Traffic System

## Overview
This project tackles morning traffic congestion by simulating a city with optimized traffic light systems. We use a grid-based matrix to represent traffic lights and apply Genetic Algorithms and Reinforcement Learning to generate and evaluate traffic flow solutions. The goal is to enhance traffic management during peak hours and provide insights applicable to real-world scenarios.

## Prerequisites
- Install the required libraries by `requirements.txt`

## Project Structure

### Step 1: Train the AI Algorithms

1. **BaseLine Algorithm:**
    - **File Path:** `Tests/BaseLineTest.py`
    - **Description:** This script runs the BaseLine algorithm and prints the results.

2. **Genetic Algorithm:**
    - **File Path:** `Tests/GenTest.py`
    - **Description:** This script trains the Genetic Algorithm and saves the results in the designated directory.

3. **PPO Algorithm:**
    - **File Path:** `Tests/PPOTest.py`
    - **Description:** This script trains the PPO (Proximal Policy Optimization) algorithm and saves the results in the designated directory.

### Step 2: Generate Visualizations

1. **Genetic Algorithm Results:**
    - **File Path:** `RepoterData/GenReader.py`
    - **Description:** This script generates graphs from the data saved by the Genetic Algorithm.

2. **PPO Algorithm Results:**
    - **File Path:** `RepoterData/PPOReader.py`
    - **Description:** This script generates graphs from the data saved by the PPO algorithm.

## Directory Structure
- `Model`: All the classes in our City model
- `PPO`: Our implementation of the PPO agents and networks.
- `ReporterData`: A designated directory in which the solvers save their results.
- `Solvers`: All of the different solvers we implemented.
- `Test`: Has a basic test in order to run each solver.
