from abc import ABC, abstractmethod


class Card(ABC):
    def __init__(self, name: str, cost: int, rarity: str):
        if cost <= 0:
            raise ValueError("must be a positive integer")
        self.name = name
        self.cost = cost
        self.rarity = rarity
        self.type = self.__class__.__name__[:-4]

    def play(self, game_state: dict) -> dict: ...

    play = abstractmethod(play)

    def get_card_info(self) -> dict:
        return {
            "name": self.name,
            "cost": self.cost,
            "rarity": self.rarity,
            "type": self.type,
        }

    def is_playable(self, available_mana: int) -> bool:
        return available_mana >= self.cost
