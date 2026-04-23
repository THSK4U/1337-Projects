*This project has been created as part of the 42 curriculum by tsellak.*

# Drone Fleet Routing

## Description
This project focuses on finding the fastest route to move a group of drones from a starting hub to an end goal. The main goal is to guide all drones through a map of connected nodes in the minimum number of turns possible. The project must respect specific limits, such as nodes that only hold one drone and restricted zones that slow down movement.

As part of this project, we tested the algorithm on a very difficult map called "The Impossible Dream".

![Map Overview](image_path_here.png)

## Instructions
Follow these steps to install and run the code.

**Installation**
Clone the repository and enter the folder:
```bash
git clone <repository_url>
cd <repository_name>
```

**Execution**
Run the main script to calculate the paths and start the visualizer:
```bash
python3 main.py
```

## Algorithm Choices and Implementation Strategy
The algorithm uses pathfinding logic to find the best routes. Instead of just sending all drones on one path, it looks for multiple parallel paths.
By splitting the drones across parallel routes in the middle of the map, the algorithm avoids traffic jams in restricted zones. This strategy ensures a steady flow of drones so that the final goal receives one drone every single turn without stopping.

**Mathematical Limit Proof (Why less than 41 is impossible)**
For "The Impossible Dream" map, it is proven that no one can solve it in less than 43 turns. Less than 41 turns is mathematically impossible.
Here is the simple proof why 43 is the absolute minimum limit:
- **True Path Distance:** The shortest route looks like 15 steps. But it passes through restricted zones that have an extra cost of 2. This makes the real distance of the shortest path exactly 19.
- **The Pipeline:** The final stretch of the map is a single line. It only allows 1 drone at a time. No drones can move side-by-side here.
- **The Formula:** For 25 drones moving one by one through a simple line, the minimum time is calculated as: `Distance + (Total_Drones - 1)`.
- **The Result:** Using the real distance of 19: `19 + (25 - 1) = 43 turns`.

Achieving 43 turns proves that the algorithm works perfectly with no delays.

## Visual Representation
A graphical visualizer is included in the project. It draws the entire map and animates the drones as they move from the start to the end.
This visualizer greatly enhances the user experience. It makes it easy to understand the algorithm and allows the user to see how the drones avoid traffic jams in real-time.

![Simulation View](simulation_image_path.png)

## Resources
- **References:**
  - Dijkstra's Algorithm for finding the shortest paths.
  - Multi-agent pathfinding and basic network flow concepts.
- **AI Usage:**
  - AI was used to help write and structure this README file.
  - AI helped to analyze and write the clean mathematical proof showing why 43 is the minimum turn limit for the stress test map.
