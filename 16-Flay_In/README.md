*This project has been created as part of the 42 curriculum by tsellak.*

# FLY IN

## Description
This project focuses on finding the fastest route to move a fleet of drones from a starting base to an end goal. The main objective is to guide all drones through a map of connected zones in the minimum number of turns possible. The project respects all movement rules, including zone capacities, restricted zones, and turn mechanics.

As part of this project, we took on the optional challenge "The Impossible Dream" map (25 drones) and successfully beat the reference record of 45 turns.

## Instructions
Follow these steps to install the dependencies and run the project. A `Makefile` is provided to automate these tasks.

**Installation**
Clone the repository and install the dependencies:
```bash
git clone <repository_url>
cd <repository_name>
make install
or
make
```

**Execution**
Run the main script to calculate the paths and start the visualizer:
```bash
make run
or
make
```
*(Alternatively, you can run `uv run python3 -m main` directly).*

## Algorithm Choices and Implementation Strategy
The algorithm uses a **modified Yen's K-Shortest Paths** approach. Instead of sending all drones on a single path, it simultaneously calculates multiple disjoint parallel paths based on the turn costs of each zone.

By splitting the drones across different routes in the middle of the map, the algorithm avoids traffic jams in restricted areas. This strategy ensures a steady flow of drones so that the final goal receives one drone every single turn without stopping.

**Why 43 Turns is the Minimum for the Challenger Map:**
For "The Impossible Dream" map, our simulation achieved the optimal time of exactly 43 turns.
Here is a simple explanation of why achieving less than 43 turns is mathematically impossible:
- **True Path Distance:** The shortest route appears to be 15 steps. However, it passes through restricted zones that take 2 turns to cross, making the true shortest distance exactly 19.
- **The Bottleneck:** The final part of the map is a single tight path where only 1 drone can pass at a time.
- **The Formula:** For 25 drones passing one by one through this path, the optimal time formula is: `Distance + (Total_Drones - 1)`.
- **The Calculation:** `19 + (25 - 1) = 43 turns`.

By achieving exactly 43 turns, we prove that the algorithm works perfectly with absolute maximum efficiency and zero delays.

## Visual Representation
A graphical visualizer is included in the project, built using the **Python Arcade** library. It draws the entire network of zones and smoothly animates the drones as they move from the start hub to the end goal.

The visualizer enhances the user experience by making it easy to understand the decisions made by the algorithm. Users can clearly watch the drones split into parallel paths and avoid bottlenecks in real-time, making the routing logic intuitive.

## Resources
- **References:**
  - Python **Arcade** library documentation for 2D visualization graphics.
  - **Yen's K-Shortest Paths** algorithm for multi-path routing.
  - Basic concepts of multi-agent pathfinding and network flow.
- **AI Usage:**
  - AI was used to help write and structure this README file to ensure clear and proper English.
  - AI helped to analyze and formulate the clean mathematical proof showing why 43 is the minimum possible turn limit for the challenge map.
