from parser.parser import status_drone, ZoneType, Graph
import heapq


class solver:
    """Simulation engine and pathfinding solver for the drone routing."""

    def __init__(self, graph: Graph) -> None:
        """Initializes the solver engine with the given network graph.

        Args:
            graph (Graph): The loaded environmental map graph.
        """
        self.graph = graph
        self.path_solve: dict[float, list[list[str]]] = {}

    def solve(self, path_solve: list) -> list:
        """Simulates the drone movements over multiple turns across paths.

        Args:
            path_solve (list): A predefined selection of optimal paths that
                the drones will split between evenly.

        Returns:
            list: A structured list describing drone movements per discrete
                simulation turn, used by the visualizer.
        """
        if not self.graph.drones:
            raise ValueError("No drones available to simulate.")
        if not path_solve:
            raise ValueError("No solution paths provided.")

        try:
            drones = self.graph.drones
            graph = self.graph.hubs

            drone_path = {
                drone: path_solve[i % len(path_solve)]
                for i, drone in enumerate(drones)
            }
            step = {d: 0 for d in drones}
            turns = 0
            final_path = []
            in_transit: dict[str, dict[str, str]] = {}
            print("\n")

            while True:
                turns += 1
                current_mov: dict[str, int] = {}
                current_path = []
                arrived_this_turn = set()

                for drone in list(in_transit.keys()):
                    info = in_transit[drone]
                    new_zone = info["to"]
                    graph[new_zone].current_drones += 1
                    drones[drone].current_hub = graph[new_zone]
                    drones[drone].status = status_drone.MOVING
                    step[drone] += 1
                    arrived_this_turn.add(drone)
                    current_path.append(
                        [drone, info["from"], new_zone, drones[drone].status]
                    )
                    del in_transit[drone]

                for drone in drones:
                    if drone in arrived_this_turn:
                        continue

                    my_path = drone_path[drone]
                    zone = my_path[step[drone]]

                    if zone == "goal":
                        continue

                    new_zone = my_path[step[drone] + 1]

                    c = [
                        h
                        for h in graph[zone].neighbors
                        if h.objective.name == new_zone
                    ]
                    used = current_mov.get(new_zone, 0)
                    max_capacity = c[0].max_capacity if c else 1

                    if (
                        used < max_capacity
                        and graph[new_zone].current_drones
                        < graph[new_zone].max_drones
                    ):
                        current_mov[new_zone] = used + 1

                        id_drone = drones[drone].id_drone
                        if graph[new_zone].type_zone == ZoneType.RESTRICTED:
                            graph[zone].current_drones -= 1
                            drones[drone].status = status_drone.LAZY
                            in_transit[drone] = {"from": zone, "to": new_zone}
                            current_path.append(
                                [drone, zone, new_zone, drones[drone].status]
                            )
                            print(
                                f"{id_drone}-C{graph[new_zone].name}",
                                end=" ",
                            )
                        else:
                            drones[drone].current_hub = graph[new_zone]
                            drones[drone].status = status_drone.MOVING
                            graph[zone].current_drones -= 1
                            graph[new_zone].current_drones += 1
                            step[drone] += 1
                            current_path.append([drone, zone, new_zone])
                            print(
                                f"{id_drone}-{graph[new_zone].name}",
                                end=" ",
                            )
                    else:
                        drones[drone].status = status_drone.LAZY
                print(end="\n")
                final_path.append(current_path.copy())

                if (
                    all(drone_path[d][step[d]] == "goal" for d in drones)
                    and not in_transit
                ):
                    break

            print("The Turns :", turns)
            return final_path
        except Exception as e:
            raise ValueError(f"Simulation failed: {e}")

    def get_path(self, k: int = 2) -> dict[float, list[list[str]]]:
        """Calculates 'K' shortest constrained paths from start to goal.

        Args:
            k (int): The maximum iterations of alternate shortest paths to
                search for and assemble.

        Returns:
            dict[float, list[list[str]]]: A dictionary where keys represent
                the cost of pathways, and values contain grouped route nodes.
        """
        if "start" not in self.graph.hubs:
            raise ValueError("Start hub is missing.")
        if "goal" not in self.graph.hubs:
            raise ValueError("Goal hub is missing.")

        try:
            neighbors: dict[str, list] = {}
            for hub in self.graph.hubs:
                neighbors[hub] = []

                for nb in self.graph.hubs[hub].neighbors:
                    obj = nb.objective

                    if nb.objective.type_zone in (
                        ZoneType.PRIORITY,
                        ZoneType.NORMAL,
                        ZoneType.RESTRICTED,
                    ):
                        if obj.neighbors or obj.name == "goal":
                            neighbors[hub].append(nb)

            queue: list[tuple[float, list[str]]] = []
            all_path: dict[float, list[list[str]]] = {}
            heapq.heappush(queue, (0.0, ["start"]))

            while queue and len(all_path) < k:
                current_cost, path = heapq.heappop(queue)
                current = path[-1]

                if current == "goal":
                    if current_cost in all_path:
                        all_path[current_cost] += [path]
                    else:
                        all_path[current_cost] = [path]
                    continue

                for nb in neighbors.get(current, []):
                    neighbor = nb.objective
                    neighbor_name = neighbor.name

                    if neighbor.max_drones == 0 or neighbor_name in path:
                        continue

                    cost_zone: float = 1.0
                    if neighbor.type_zone == ZoneType.RESTRICTED:
                        cost_zone = 2
                    elif neighbor.type_zone == ZoneType.PRIORITY:
                        cost_zone = 0.9

                    if neighbor.max_drones > 1:
                        cost_zone -= 0.1 * neighbor.max_drones

                    new_cost = (current_cost + cost_zone) + (
                        1 / nb.max_capacity
                    )

                    heapq.heappush(queue, (new_cost, path + [neighbor_name]))

            return all_path
        except Exception as e:
            raise ValueError(f"Pathfinding failed: {e}")
