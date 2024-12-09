# Air Pollution Managment Multi-Agent System Stimulation using MESA Python Library

This project demonstrates an intelligent Air Pollution Management System built using Multi-Agent Systems (MAS) principles and the MESA framework for my Multi-Agents System Module provided by the Department of Computational Mathematics, Faculty of IT, University of Moratuwa. It simulates pollution dynamics in an urban environment and employs autonomous agents to monitor, manage, and mitigate pollution effectively. This project showcases the potential of Multi-Agent Systems in solving complex real-world problems like air pollution management. It is a step towards building smarter, adaptive urban ecosystems.
 

## Key Features:
* Problem Addressed: Urban air pollution caused by vehicles, factories, and other sources.
* Dynamic Simulation: A grid-based environment where agents interact, adapt, and respond to pollution levels in real-time.
  
## Multi-Agents:
* Car Agents: Represent mobile pollution sources; autonomously reroute to avoid high-pollution areas.
* Factory Agents: Stationary agents generating pollution and adapting emissions based on environmental needs.
* Tree Agents: Environmental entities that absorb pollution but degrade in highly toxic conditions.
* Pollution Monitoring Agents: Monitor and diffuse pollution dynamically across the grid by communicating.

## Project Overview
* BDI Architecture: Agents leverage the Belief-Desire-Intention model for decision-making and actions.
* Emergent Behavior: Observe complex system dynamics, trees dying as a result of high toxic air pollution, resulting from agent interactions.
* Butterfly Effect: Small changes in agent behavior, such as factory emission spikes, lead to large-scale high air pollution on the system.

## System Overview:
* Inputs: Environment size, agent configurations, initial pollution levels.
* Outputs: Pollution heatmaps, agent communication logs, critical zone identification.
* Visualization: Real-time simulation of agent actions and pollution dynamics using the MESA framework.

![whole-graph](https://github.com/user-attachments/assets/693bc644-f824-4601-a769-bef3f9a1c8a3)

## Highlights:
* Autonomy: Agents operate independently, responding to real-time changes.
* Communication: Inter-agent communication ensures information flow and coordinated actions.
* Adaptability: System adjusts dynamically to changing pollution conditions and stochastic factors.

![Screenshot 2024-12-09 182144](https://github.com/user-attachments/assets/cb0521d4-aae5-4c96-88c0-46cda02f3734)
Terminal window showing agent communication

![initial-state](https://github.com/user-attachments/assets/4f71ac7f-8140-4f8e-b20e-9427bd1439cb)
Initial State - the city is not polluted and it had good air quality

![final-state](https://github.com/user-attachments/assets/1897077d-7f8c-4efc-8acd-eb4163c51c42)
Final State - the smoke from factories and vehicles have increased air pollution

## Technologies Used:
* Framework: MESA (Python-based agent-based modeling framework)
* Architecture: BDI (Belief-Desire-Intention)
* Visualization: Real-time pollution heatmaps and agent interactions

  
