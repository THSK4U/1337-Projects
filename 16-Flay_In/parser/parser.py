from pydantic import BaseModel, Field
from .map import read_map
from enum import Enum


class ZoneType(Enum):
    """Enumeration representing the different types of zones in the map."""
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Connection(BaseModel):
    """Represents a directional path from one hub to another."""
    objective: "Hub"
    max_capacity: int = Field(default=1)


class Hub(BaseModel):
    """Represents a node or zone within the drone network."""
    name: str
    type_zone: ZoneType = Field(default=ZoneType.NORMAL)
    max_drones: int
    current_drones: int = Field(default=0)
    color: str
    x: int
    y: int
    neighbors: list[Connection] = Field(default_factory=list)


class status_drone(Enum):
    """Enumeration representing the current physical status of a drone."""
    LAZY = "lazy"
    MOVING = "moving"


class Drones(BaseModel):
    """Represents an individual drone entity in the simulation."""
    id_drone: str
    current_hub: Hub
    status: status_drone


class Graph:
    """Parses and constructs the network graph from a map string input."""

    def __init__(self, path_file: str):
        """Initializes the Graph by parsing the given map file.

        Args:
            path_file (str): The path to the textual map file.
        """
        try:
            self.data = path_file
            self.drones: dict[str, Drones] = {}
            self.hubs: dict[str, Hub] = {}
            self.connections: dict[str, list[Connection]] = {}
            self.start_name: str = ""
            self.end_name: str = ""

            read = read_map(self.data)

            if int(read["nb_drones"][0]) > 0:
                self.nb_drones = int(read["nb_drones"][0])
            else:
                raise ValueError("Invalid number of drones. Must be > 0.")

            if read.get("start_hub"):
                self.start_name = read["start_hub"][0].split()[0]
            if read.get("end_hub"):
                self.end_name = read["end_hub"][0].split()[0]

            if not self.start_name or not self.end_name:
                raise ValueError("Map must contain start_hub and end_hub")

            all_hubs_get = (
                read.get("start_hub", [])
                + read.get("end_hub", [])
                + read.get("hub", [])
            )
            filter_location = []
            for hub in all_hubs_get:
                list_hub = hub.split(maxsplit=3)
                max_drones = 1
                color = "white"
                type_zone = ZoneType.NORMAL
                name = list_hub[0]
                if '-' in name:
                    raise ValueError(
                        f"Invalid hub name '{name}'. '-' is not allowed.")
                x, y = (int(list_hub[1]), int(list_hub[2]))
                if (x, y) in filter_location:
                    raise ValueError(
                        f"Duplicate location ({x}, {y}) for hub '{name}'.")
                else:
                    filter_location.append((x, y))

                if name == "impossible_goal":
                    name = "goal"

                if name == "start" or name == "goal":
                    max_drones = self.nb_drones

                if len(list_hub) > 3:
                    for item in list_hub[3].split():
                        attributes = item.strip("[]").split("=")
                        if (attributes[0] == "zone" and
                                attributes[1] in ZoneType):
                            type_zone = attributes[1]

                        if attributes[0] == "color":
                            color = attributes[1]

                        if attributes[0] == "max_drones":
                            max_drones = int(attributes[1])

                self.hubs[name] = Hub(
                    name=name,
                    type_zone=type_zone,
                    max_drones=max_drones,
                    color=color,
                    x=x,
                    y=y,
                )

            for i in range(1, self.nb_drones + 1):
                self.drones["D" + str(i)] = Drones(
                    id_drone="D" + str(i),
                    current_hub=self.hubs[self.start_name],
                    status=status_drone.LAZY,
                )

            for connection in read["connection"]:
                list_connection = connection.split(maxsplit=1)
                names = list_connection[0].split("-")
                if not names or len(names) > 2:
                    raise ValueError(
                        f"Invalid connection format for {list_connection[0]}.")
                names = [name.replace("impossible_goal", "goal")
                         for name in names]

                attr_dict = {}
                if len(list_connection) > 1:
                    attr_dict = dict(
                        item.strip("[]").split("=")
                        for item in list_connection[1].split()
                    )
                if not names[0] in self.connections:
                    self.connections[names[0]] = []
                self.connections[names[0]].append(
                    Connection(
                        objective=self.hubs[names[-1]],
                        max_capacity=int(attr_dict.get(
                            "max_link_capacity", 1)),
                    )
                )
            if self.hubs['start'].type_zone == ZoneType.BLOCKED:
                raise ValueError("Start hub cannot be blocked")
            if self.hubs['goal'].type_zone == ZoneType.BLOCKED:
                raise ValueError("End hub cannot be blocked")
            if self.hubs['start'].max_drones < self.nb_drones:
                raise ValueError(
                    "Start hub max_drones must be at least nb_drones")
            if self.hubs['goal'].max_drones < self.nb_drones:
                raise ValueError(
                    "End hub max_drones must be at least nb_drones")

            for name in self.connections:
                for neighbor in self.connections[name]:
                    self.hubs[name].neighbors.append(neighbor)
        except Exception as e:
            raise ValueError(f"Map parsing failed: {e}")
