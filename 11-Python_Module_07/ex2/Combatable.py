from abc import ABC, abstractmethod


class Combatable(ABC):
    def attack(self, target: str) -> dict: ...

    attack = abstractmethod(attack)

    def defend(self, incoming_damage: int) -> dict: ...

    defend = abstractmethod(defend)

    def get_combat_stats(self) -> dict: ...

    get_combat_stats = abstractmethod(get_combat_stats)
