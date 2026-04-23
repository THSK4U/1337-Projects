from parser.parser import status_drone, Connection, Drones, ZoneType
import heapq


class solver:
    def __init__(self, graph) -> None:
        self.graph = graph
        self.connection = graph.connections
        self.path_solve = {}

    def solve(self, path_solve: list) -> list:
        drones = self.graph.drones
        graph = self.graph.hubs

        drone_path = {
            drone: path_solve[i % len(path_solve)]
            for i, drone in enumerate(drones)
        }
        step = {d: 0 for d in drones}
        turns = 0
        final_path = []
        in_transit = {}

        while True:
            turns += 1
            current_mov = {}
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

                # print(zone)
                if zone == "goal":
                    continue

                new_zone = my_path[step[drone] + 1]

                hub = [
                    h
                    for h in graph[zone].neighbors
                    if h.objective.name == new_zone
                ]
                used = current_mov.get(new_zone, 0)
                max_capacity = hub[0].max_capacity if hub else 1

                # print(max_capacity, used)
                if (
                    used < max_capacity
                    and graph[new_zone].current_drones
                    < graph[new_zone].max_drones
                ):
                    current_mov[new_zone] = used + 1

                    if graph[new_zone].type_zone == ZoneType.RESTRICTED:
                        graph[zone].current_drones -= 1
                        drones[drone].status = status_drone.LAZY
                        in_transit[drone] = {"from": zone, "to": new_zone}
                        current_path.append(
                            [drone, zone, new_zone, drones[drone].status]
                        )
                    else:
                        drones[drone].current_hub = graph[new_zone]
                        drones[drone].status = status_drone.MOVING
                        graph[zone].current_drones -= 1
                        graph[new_zone].current_drones += 1
                        step[drone] += 1
                        # print(waiting[drone])
                        current_path.append([drone, zone, new_zone])
                else:
                    drones[drone].status = status_drone.LAZY

            final_path.append(current_path.copy())

            if (
                all(drone_path[d][step[d]] == "goal" for d in drones)
                and not in_transit
            ):
                break

            # print(step)
        print("The Turns :", turns)
        return final_path
        # return step

    def get_path(self, k=2) -> None:
        neighbors: dict[str, list] = {}
        for hub in self.graph.hubs:
            neighbors[hub] = []
            # print("Hub:", hub)

            for nb in self.graph.hubs[hub].neighbors:
                obj = nb.objective

                if nb.objective.type_zone in (
                    ZoneType.PRIORITY,
                    ZoneType.NORMAL,
                    ZoneType.RESTRICTED,
                ):
                    if obj.neighbors or obj.name == "goal":
                        neighbors[hub].append(nb)

        # print(neighbors['start'])

        queue: list[tuple[int, str]] = []
        came_from: dict[str, str] = {}
        cost_hub: dict[str, int] = {}
        all_path = {}
        visited: dict[str, int] = {}
        heapq.heappush(queue, (0, ["start"]))
        cost_hub["start"] = 0

        while queue and len(all_path) < k:
            current_cost, path = heapq.heappop(queue)
            current = path[-1]

            visited[current] = visited.get(current, 0) + 1
            if visited[current] > k:
                continue

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

                cost_zone = 1
                if neighbor.type_zone == ZoneType.RESTRICTED:
                    cost_zone = 2
                elif neighbor.type_zone == ZoneType.PRIORITY:
                    cost_zone = 0.9

                if neighbor.max_drones > 1:
                    cost_zone -= 0.1 * neighbor.max_drones

                # new_cost = (cost_hub[current] + cost_zone) + (1 / nb.max_capacity)

                new_cost = (current_cost + cost_zone) + (1 / nb.max_capacity)
                heapq.heappush(queue, (new_cost, path + [neighbor_name]))
                # print(queue)

                # if neighbor_name not in cost_hub or new_cost < cost_hub[neighbor_name]:
                #     cost_hub[neighbor_name] = new_cost
                #     priority = new_cost

                #     heapq.heappush(queue, (priority, neighbor_name))
                #     came_from[neighbor_name] = current

        # print("CameFrom:", [current for current in came_from if current != 'start'])
        # exit()

        # path_final: list[str] = ['start']
        # while current != 'start':
        #     path_final.insert(1, current)
        #     current = came_from[current]
        return all_path
