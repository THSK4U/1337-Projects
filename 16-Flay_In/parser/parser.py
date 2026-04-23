from pydantic import BaseModel, Field
from typing import Optional
from .map import read_map
from enum import Enum


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Hub(BaseModel):
    name: str
    type_zone: ZoneType = Field(default=ZoneType.NORMAL)
    max_drones: int
    current_drones: int = Field(default=0)
    color: str
    x: int
    y: int
    neighbors: Optional[Connection] = Field(default=[])


class Connection(BaseModel):
    objective: Hub
    max_capacity: int = Field(default=1)


class Drones(BaseModel):
    id_drone: str
    current_hub: Hub
    status: status_drone


class status_drone(Enum):
    LAZY = "lazy"
    MOVING = "moving"


# 'nb_drones', 'start_hub', 'hub', 'end_hub', 'connection'
class Graph:
    def __init__(self, path_file: str):
        self.data = path_file
        self.drones = {}
        self.hubs = {}
        self.connections = {}
        self.start_name = None
        self.end_name = None

        read = read_map(self.data)

        self.nb_drones = int(read["nb_drones"][0])

        if read.get("start_hub"):
            self.start_name = read["start_hub"][0].split()[0]
        if read.get("end_hub"):
            self.end_name = read["end_hub"][0].split()[0]

        all_hubs_get = (
            read.get("start_hub", [])
            + read.get("end_hub", [])
            + read.get("hub", [])
        )

        for hub in all_hubs_get:
            list_hub = hub.split(maxsplit=3)
            # print(list_hub)
            x, y = (int(list_hub[1]), int(list_hub[2]))
            max_drones = 1
            name = list_hub[0]

            if name == "impossible_goal":
                name = "goal"

            if name == "start" or name == "goal":
                max_drones = self.nb_drones

            color = "white"
            type_zone = ZoneType.NORMAL

            if len(list_hub) > 3:
                for item in list_hub[3].split():
                    attributes = item.strip("[]").split("=")
                    if attributes[0] == "zone" and attributes[1] in ZoneType:
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
            self.drones["drone_" + str(i)] = Drones(
                id_drone="drone_" + str(i),
                current_hub=self.hubs[self.start_name],
                status=status_drone.LAZY,
            )

        # print(self.hubs)

        # print(read)
        for connection in read["connection"]:
            list_connection = connection.split(maxsplit=1)
            names = list_connection[0].split("-")
            names = [name.replace("impossible_goal", "goal") for name in names]

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
                    max_capacity=int(attr_dict.get("max_link_capacity", 1)),
                )
            )
        # print(self.connections['start'])

        for name in self.connections:
            for neighbor in self.connections[name]:
                self.hubs[name].neighbors.append(neighbor)
            # print(self.connections[name])
        # for conn in self.hubs['gate2'].neighbors:
        # print(self.hubs['start'].x)
        # exit()


if __name__ == "__main__":
    Graph(r"/home/tsellak/FL/maps/hard/03_ultimate_challenge.txt")
