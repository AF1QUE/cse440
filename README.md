# Self-Driving AI Car Racing Game

## Overview
This project simulates an AI-powered self-driving car using the **NEAT (NeuroEvolution of Augmenting Topologies)** algorithm in a 2D racing game built with **Pygame**. Through evolution-based neural networks, virtual cars learn to navigate racetracks using five radar-like sensors without any labeled training data or prior driving knowledge.

---

## Features
- Neuroevolution-based learning using NEAT
- Real-time 2D simulation with Pygame
- Sensor-based car control and collision detection
- Configurable racetrack environments
- Visual debugging tools
- Performance tracking and fitness evolution

---

## Table of Contents
- [Installation](#installation)
- [How It Works](#how-it-works)
  - [System Design](#system-design)
  - [Methodology](#methodology)
  - [Experimental Setup](#experimental-setup)
  - [Results](#results)
- [Limitations and Future Work](#limitations-and-future-work)
- [Credits](#credits)
- [References](#references)

---

## Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/yourusername/self-driving-ai-car
   cd self-driving-ai-car
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the simulation:**
   ```bash
   python main.py
   ```

---

## How It Works

### System Design

#### Tools & Libraries
- **Python 3**: Core language
- **Pygame**: Graphics and simulation
- **NEAT-Python**: Evolutionary neural networks
- **NumPy**: Sensor calculations and math

#### Components
- **Car Class**: Handles movement, sensor detection, rendering, and collision.
- **Simulation Loop**: Each generation spawns cars from genome networks.
- **NEAT Configuration**: Controlled via `config.txt`.
- **Fitness Evaluation**: Based on distance traveled without crashing.

#### Car Mechanics
- Cars are rendered sprites with 5 radar-like sensors.
- Sensors detect walls (white pixels), collisions end evaluation.
- Controls are: steer left/right, speed up/down.

---

### Methodology

#### Sensor Input
- 5 radar rays cast at angles from -90° to 90°.
- Sensor outputs form a 5D input vector for the neural network.

#### Neural Network Output
- Output indices:
  0. Steer Left
  1. Steer Right
  2. Decrease Speed
  3. Increase Speed

- Only the action with the highest output is executed per tick.

#### Fitness Function
```math
Fitness = Distance / (CAR_SIZE_X / 2)
```
- Promotes forward movement and penalizes crashes or sharp turns.

#### Evolution Strategy
- After each generation:
  - Top-performing cars are selected
  - Crossover and mutation generate the next population
  - Species grouping maintains diversity

---

### Experimental Setup

#### Environment
- **Map Size**: 1920x1080 pixels
- **Car Size**: 60x60 pixels
- **Max Simulation Time**: ~20 seconds per generation
- **Generations**: Up to 1000

#### NEAT Configuration
- **Population Size**: 30
- **Mutation Rate**: Tuned in `config.txt`
- **Activation**: Sigmoid

#### Tracks
1. Simple ring
2. Curved racetrack
3. Winding maze
4. Chaotic, complex maze (hardest)

---

### Results

#### Basic Track
- Cars complete laps within few generations.
- Simple left-right steering behavior evolves quickly.

#### Intermediate Map
- About 7 generations for cars to complete the track.
- NEAT evolves multiple strategies: fast/risky vs. slow/steady.

#### Complex Map
- Manual tuning required (fixed speed, minimal network complexity).
- Eventually successful completions achieved.

#### Performance Trends
- Early generations show random movement.
- Later generations demonstrate strategic driving.
- Species mechanism preserves innovation.

---

## Limitations and Future Work

### Current Limitations
- Only 2D simulation
- No dynamic obstacles
- CPU-intensive for large populations

### Possible Enhancements
- Introduce traffic or dynamic hazards
- Extend to 3D with physics engines
- Combine with real-world driving datasets
- Integrate attention mechanisms

---

## Credits
- **Cheesy AI** – Original project inspiration
- **NeuralNine** – Codebase optimization and documentation
- **NEAT-Python** – Core algorithm implementation
- **Team Members**:
  - Abdullah Al Afique (2031117642)
  - Israt Asha (1921758042)
  - Tanha Ahmed Nijhum (2031523642)

---

## References
1. Stanley, K. & Miikkulainen, R. (2002). "Evolving Neural Networks through Augmenting Topologies." Evolutionary Computation.
2. NeuralNine. "Self-Driving AI Car Simulation in Python" – YouTube.
3. Cheesy AI. "AI Driving Simulation in Python" – GitHub.
4. NEAT-Python – https://github.com/CodeReclaimers/neat-python
5. Pygame Docs – https://www.pygame.org/docs/
6. Clune, J., et al. (2008). "Evolving Coordinated Quadruped Gaits with the HyperNEAT Generative Encoding."

---

> This simulation project was developed for CSE440 Group 10, Spring 2025.
> University project for educational purposes only.
