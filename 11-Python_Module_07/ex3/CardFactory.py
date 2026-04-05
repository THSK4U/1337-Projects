from abc import ABC, abstractmethod

from ex0.Card import Card


class CardFactory(ABC):
    def create_creature(self, name_or_power: object) -> Card: ...

    create_creature = abstractmethod(create_creature)

    def create_spell(self, name_or_power: object) -> Card: ...

    create_spell = abstractmethod(create_spell)

    def create_artifact(self, name_or_power: object) -> Card: ...

    create_artifact = abstractmethod(create_artifact)

    def create_themed_deck(self, size: int) -> dict: ...

    create_themed_deck = abstractmethod(create_themed_deck)

    def get_supported_types(self) -> dict: ...

    get_supported_types = abstractmethod(get_supported_types)
