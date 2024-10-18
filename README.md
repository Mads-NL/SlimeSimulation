# Slime Simulation

## Overview
The **Slime Simulation** is an interactive 2D simulation that models the behavior of agents moving through an environment. Inspired by natural phenomena, this simulation visualizes how agents navigate their surroundings, interact with each other, and leave traces in a dynamic environment. The agents sense their surroundings, make decisions based on their environment, and exhibit swarm-like behavior.

## Key Features
- **Agent Movement:** Each agent moves based on its current angle and speed, updating its position in real-time.
- **Sensing Mechanism:** Agents can sense the environment around them, allowing them to adjust their movement based on the values detected.
- **Evaporation and Diffusion:** The environment features an evaporation mechanism to gradually diminish the agents' traces and a diffusion process that simulates spreading effects.
- **Dynamic Visualization:** The simulation is rendered using Manim, allowing for smooth animations and visual feedback on agent behavior.

## How It Works
1. **Initialization:** The simulation initializes a specified number of agents with random positions and angles.
2. **Simulation Loop:** Each agent updates its position and angle based on its surroundings over a series of simulation steps.
3. **Visualization:** The current state of the environment is rendered as an image and displayed in real-time, showing the agents' movements and interactions.

## Example
Here's a short video demonstrating the slime simulation in action:

[![Slime Simulation Example](https://img.youtube.com/vi/oXoff2CrFfA/0.jpg)](https://youtu.be/oXoff2CrFfA)

*Click the image above to watch the video!*

## Acknowledgements
- Inspired by https://uwe-repository.worktribe.com/output/980579