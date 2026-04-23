*This project has been created as part of the 42 curriculum by tsellak.*

# Fly-in — Drone Routing Simulation

## Description

**Fly-in** is a Python simulation system that routes a fleet of autonomous drones from
a central hub (start zone) to a target location (end zone) through a network of
connected zones, while respecting movement constraints and minimizing the total number
of simulation turns.

Each zone has a type that determines movement cost and accessibility:
| Zone Type | Movement Cost | Notes |
|-----------|--------------|-------|
| `normal` | 1 turn | Default |
| `priority` | 1 turn | Preferred by pathfinder |
| `restricted` | 2 turns | Transit via connection for 1 turn |
| `blocked` | ∞ | Inaccessible |

Zones and connections have capacity limits (`max_drones`, `max_link_capacity`).
The simulation ensures no conflicts occur at any turn.

## Instructions

### Requirements
- Python 3.10 or later
- pip

### Installation

```bash
make install
```

### Running the Simulation

```bash
# Run default map (easy_linear.txt)
make run

# Run a specific map
make run MAP=maps/hard_maze.txt

# With colors disabled
python main.py maps/easy_fork.txt --no-color

# With matplotlib network graph
python main.py maps/medium_loop.txt --graph

# Debug mode (pdb)
make debug MAP=maps/medium_deadend.txt
```

### Linting

```bash
make lint         # flake8 + mypy standard
make lint-strict  # flake8 + mypy --strict
```

### Cleanup

```bash
make clean
```

## Algorithm Choices & Implementation Strategy

### Architecture

The project is split into focused, single-responsibility modules:

| Module | Role |
|--------|------|
| `models.py` | Data classes: `Zone`, `Connection`, `Graph`, `DroneState` |
| `parser.py` | Map file parser with full validation and descriptive errors |
| `pathfinding.py` | Dijkstra-based shortest-path + multi-path discovery |
| `simulation.py` | Two-phase turn engine with capacity and conflict enforcement |
| `visualizer.py` | ANSI terminal colors + optional matplotlib graph |
| `main.py` | CLI entry point |

### Pathfinding

The pathfinder uses **Dijkstra's algorithm** (via a min-heap) that:
- Costs 1 turn for `normal` / `priority` zones, 2 for `restricted`
- Never enters `blocked` zones
- Biases toward `priority` zones when costs are equal
- Generates up to 6 **disjoint candidate paths** by excluding interior nodes of
  already-found paths

Drones are then **distributed round-robin** across candidate paths, with a **staggered
start delay**: each additional drone on the same path launches 1 turn later to avoid
capacity conflicts at the first zone.

### Simulation Engine (Two-Phase Commits)

Each turn uses a **two-phase approach** to prevent race conditions:

1. **Planning phase** — Evaluate each drone's next move against committed capacity
   budgets (without mutating state)
2. **Commit phase** — Apply all valid moves atomically

This ensures "drones moving out free up capacity for that same turn" (spec requirement)
and prevents double-booking of zone capacity.

**Restricted zones** (2-turn moves) are handled by keeping the drone on the connection
name for turn 1, then landing at the destination on turn 2, committing the connection
on arrival.

### Visual Representation

Terminal output uses **ANSI escape codes** to colorize:
- Drone labels (bright magenta)
- Zone names by type (green = priority, red = restricted, yellow = end hub, etc.)
- Colors specified in the map file are supported

An optional **matplotlib network graph** (`--graph` flag) shows the zone topology with
connections labeled by capacity, rendered before the simulation starts.

## Map Files

Sample maps are provided in the `maps/` directory:

| File | Drones | Category | Target |
|------|--------|----------|--------|
| `easy_linear.txt` | 2 | Easy | ≤ 6 turns |
| `easy_fork.txt` | 3 | Easy | ≤ 6 turns |
| `easy_capacity.txt` | 4 | Easy | ≤ 8 turns |
| `medium_deadend.txt` | 5 | Medium | ≤ 15 turns |
| `medium_loop.txt` | 6 | Medium | ≤ 20 turns |
| `hard_maze.txt` | 8 | Hard | ≤ 45 turns |

## Simulation Output Format

Each line represents one turn, listing drones that moved:

```
D1-roof1 D2-corridorA
D1-roof2 D2-tunnelB
D1-goal D2-goal
```

For restricted-zone transit (2-turn moves), the connection name is shown on turn 1:

```
D1-hub-restricted_zone
D1-restricted_zone
```

## Resources

- [Dijkstra's Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [BFS Pathfinding — Red Blob Games](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)
- [mypy — Type Checking for Python](https://mypy.readthedocs.io/en/stable/)
- [flake8 — Python Linting](https://flake8.pycqa.org/en/latest/)

### AI Usage

AI (Antigravity / Google DeepMind) was used to:
- Help design and scaffold the modular architecture
- Generate initial docstrings and type annotations
- Suggest edge cases for the parser (duplicate connections, invalid zone types)
- Review the two-phase commit approach for simulation correctness

All generated code was reviewed, tested, and understood before inclusion.
