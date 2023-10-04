# Mexico City Metro Route Finder using Ant Colony Optimization (ACO)

## Introduction

The Mexico City Metro is one of the largest and busiest transportation systems in the world. With its extensive network of lines and stations, finding the most efficient route between two points can be a challenge. In this project, we explore the application of the Ant Colony Optimization (ACO) algorithm to the Mexico City Metro system with the goal of finding the optimal route between two stations. This work simplifies the metro network by considering only transfers between stations as valid nodes. The ACO optimization technique is inspired by the behavior of ant colonies, where ants find efficient paths between food sources and the nest, leaving a trail of pheromones that other ants can follow.

## Theoretical Framework

The Ant Colony Optimization (ACO) algorithm is an optimization technique inspired by the behavior of ant colonies. It is used to solve combinatorial optimization problems, such as the Traveling Salesman Problem (TSP), where the goal is to find the shortest route that visits a set of cities. ACO is based on the idea that individual ants can find optimal paths to a food source through indirect communication via pheromone trails. Each ant constructs solutions iteratively, choosing moves based on both local information (pheromones deposited on the current edge) and heuristic information (problem-specific information, such as the distance between nodes). Transition probabilities are calculated using a selection rule, such as the roulette wheel rule or the weighted sum rule. The equation for calculating transition probabilities is provided in the project documentation.

## Code Implementation

The code provided in this repository implements the ACO algorithm for finding the optimal route between two metro stations in Mexico City. It includes the following key components:

- Loading of metro network data and initialization of parameters.
- Calculation of the probability of selecting the next link based on pheromone levels and visibility.
- Main algorithm loop for multiple explorations and ant interactions.
- Exploration of ants to find routes from the nest station to the food station.
- Pheromone update based on the paths explored by ants.
- Tracking of the best route found and its minimum distance.

## Usage

To use this code to find the optimal route between two metro stations, follow these steps:

1. Run the Python script provided.
2. Select the origin and destination metro stations from the dropdown menus.
3. Click the "Seleccionar" button to find the optimal route.
4. The result will be displayed in a message box, showing the selected stations, the route, and the total distance in kilometers.

## Metro Station List

The code includes a list of metro stations in Mexico City that can be selected as origin and destination points.

## Dependencies

The code uses the following Python libraries:

- `tkinter`: For creating the graphical user interface.
- `PIL`: For image handling.
- `numpy`: For numerical computations.

## Credits

This project was created by JesusEJuarez and Catherin4.
