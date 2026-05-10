from pydantic import BaseModel, Field
from .map import read_map
from enum import Enum
from .exceptions import CustomError, Duplicate, InvalidName, InvalidPosition, InvalidNumber, InvalidSyntax, NotFound

class AllowedKeywords(Enum):
    """Enumeration representing all keywords allowed in the map."""
    NB_DRONES = "nb_drones"
    START_HUB = "start_hub"
    HUB = "hub"
    END_HUB = "end_hub"
    CONNECTION = "connection"
    COLOR = "color"
    ZONE = "zone"
    MAX_DRONES = "max_drones"
    MAX_LINK_CAPACITY = "max_link_capacity"

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
            self.nb_drones: int = 0

            read = read_map(self.data)

            not_valid = [[item, read[item][0][0]] for item in read if item not in AllowedKeywords]

            if not_valid:
                lines = [number[1] for number in not_valid]
                names = [item[0] for item in not_valid]
                raise InvalidName(lines, f"Unknown keyword(s): {names}")

            # print(not next(iter(read)) == "nb_drones" or not read.get("nb_drones", False))
            if not next(iter(read)) == "nb_drones" or not read.get("nb_drones", False):
                line = read["nb_drones"][0][0] if read.get("nb_drones", False) else 1
                raise InvalidPosition(line, "'nb_drones' must be the first line of the map.")

            try :
                if int(read["nb_drones"][0][1]) > 0:
                    self.nb_drones = int(read["nb_drones"][0][1])
            except Exception:
                raise InvalidNumber(read["nb_drones"][0][0], "'nb_drones' must be a positive integer. Example: nb_drones: 3")

            if not self.nb_drones > 0:
                raise InvalidNumber(read["nb_drones"][0][0], "Must be positive integer. nb_drones: <positive_integer>.")

            start_hubs = read.get("start_hub", [])
            if len(start_hubs) == 1:
                self.start_name = start_hubs[0][1].split()[0]
            elif len(start_hubs) == 0:
                raise NotFound("Map must contain exactly one 'start_hub'.")
            else:
                raise Duplicate(start_hubs[1][0], "Only one end_hub is allowed.")

            end_hubs = read.get("end_hub", [])
            if len(end_hubs) == 1:
                self.end_name = end_hubs[0][1].split()[0]
            elif len(end_hubs) == 0:
                raise NotFound("Map must contain exactly one 'end_hub'.")
            else:
                raise Duplicate(end_hubs[1][0], "Only one end_hub is allowed.")

            all_hubs_get = (
                read.get("start_hub", [])
                + read.get("end_hub", [])
                + read.get("hub", [])
            )

            filter_location = []
            for index, hub in all_hubs_get:
                list_hub = hub.split(maxsplit=3)
                max_drones = 1
                color = "white"
                type_zone = ZoneType.NORMAL
                name = list_hub[0]
                if '-' in name:
                    raise InvalidName(index, f"For Hub '{name}'. '-' is not allowed.")
                x, y = (int(list_hub[1]), int(list_hub[2]))
                if (x, y) in filter_location:
                    raise Duplicate(index, f"Duplicate location ({x}, {y}) for hub '{name}'.")
                else:
                    filter_location.append((x, y))

                if name == "impossible_goal":
                    name = "goal"

                if name == "start" or name == "goal":
                    max_drones = self.nb_drones

                if len(list_hub) > 3:
                    attributes: list = []
                    strip_1 = list_hub[3].strip('[]').replace("=", " = ")
                    tokens = strip_1.split()
                    step = 0
                    attributes_list = []

                    while step < len(tokens):
                        if tokens[step] in attributes_list:
                            raise Duplicate(index, f'Only one "{tokens[step]}" is allowed.')
                        if not tokens[step] in AllowedKeywords:
                            raise InvalidName(index, f'This Keyword "{tokens[step]}" is not allowed.')
                        try:
                            if tokens[step+1] == '=' and tokens[step+2]:
                                attributes_list += [tokens[step]]
                                attributes += [f"{tokens[step]}={tokens[step+2]}"]
                                step += 3
                            else:
                                raise
                        except:
                            raise InvalidSyntax(index, f"'{tokens[step]}' Expected format: key=value")

                    for item in attributes:
                        attribute = item.split('=')
                        if (attribute[0] == "zone" and
                                attribute[1] in ZoneType):
                            type_zone = attribute[1]

                        elif (attribute[0] == "zone" and
                                attribute[1] not in ZoneType):
                            raise CustomError(
                                "Invalid zone type", index,
                                f"'{attribute[1]}'. Must be one of:\nnormal, blocked, restricted, priority.")

                        from parser.visualizer import COLORS_DICT
                        if (attribute[0] == "color" and
                                attribute[1] in COLORS_DICT):
                                color = attribute[1]
                        elif (attribute[0] == "color" and
                                attribute[1] not in COLORS_DICT):
                            if attribute[1].isalpha():
                                print(f"\nWARNING: Invalid color '{attribute[1]}'. Defaulting to 'white'.")
                            else:
                                raise InvalidName(index, f"This Color '{attribute[1]}' is not valid single-word strings.")

                        try:
                            if (attribute[0] == "max_drones" and
                                    int(attribute[1]) > 0):
                                max_drones = int(attribute[1])
                            elif (attribute[0] == "max_drones" and
                                    not int(attribute[1]) > 0):
                                raise
                        except Exception:
                            raise InvalidNumber(index, "Must be positive integer max_drones: <positive_integer>.")


                if name in self.hubs:
                    raise Duplicate(index, f"This hub name '{name}' is duplicate.")
                else:
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

            connection_valid = set()
            for index, connection in read["connection"]:
                list_connection = connection.split(maxsplit=1)
                names = list_connection[0].split("-")
                if not names or len(names) != 2 or names[0] == names[1]:
                    raise CustomError("Invalid connection format", index,
                    f"'{list_connection[0]}'. Must be connection: <name1>-<name2> [metadata]") 

                names = [name.replace("impossible_goal", "goal")
                         for name in names]

                if frozenset(names) in connection_valid:
                    raise Duplicate(index,
                    f"This '{names}' is duplicate.") 
                else:
                    connection_valid.add(frozenset(names))

                max_capacity = 1
                if len(list_connection) > 1:
                    if not list_connection[1].startswith('[') and list_connection[1].endswith(']'):
                        raise InvalidSyntax(index, f"'{list_connection[1]}' Optional metadata can be specified in brackets [...]")

                    strip_1 = list_connection[1].strip('[]').replace("=", " = ")

                    tokens = strip_1.split()
                    if len(tokens) > 3 or not tokens[0] == "max_link_capacity":
                        raise InvalidSyntax(index, f"'{list_connection[1]}' Expected Only: max_link_capacity: <positive_integer>.")
                   
                    try:
                        max_capacity = int(tokens[2]) 
                        if not int(max_capacity) > 0:
                            raise
                    except Exception:
                        raise InvalidNumber(index, "Must be positive integer max_link_capacity: <positive_integer>.")
                
                if names[0] not in self.hubs:
                    raise InvalidName(index, f"Hub '{names[0]}' is not defined. Check your hub declarations.")
                if names[1] not in self.hubs:
                    raise InvalidName(index, f"Hub '{names[1]}' is not defined. Check your hub declarations.")

                names_list = [names[0], names[1]]
                for name in names_list:
                    if name not in self.connections:
                        self.connections[name] = []
                    self.connections[name].append(
                        Connection(
                            objective=self.hubs[names[1]],
                            max_capacity=max_capacity,
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
            raise ValueError(f"{e}")
