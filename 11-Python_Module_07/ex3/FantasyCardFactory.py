from enum import Enum

from ex0.CreatureCard import CreatureCard
from ex1.ArtifactCard import ArtifactCard
from ex1.SpellCard import SpellCard
from ex3.CardFactory import CardFactory


class CardType(Enum):
    DRAGON = "dragon"
    GOBLIN = "goblin"
    FIREBALL = "fireball"
    MANA_RING = "mana_ring"
    LIGHTNING = "Lightning"


class FantasyCardFactory(CardFactory):
    def __init__(self) -> None:
        self.cards_created = 0

    def create_creature(self, name_or_power: object) -> CreatureCard:
        key = str(name_or_power).lower()
        if isinstance(name_or_power, CardType):
            key = name_or_power.value
        elif isinstance(name_or_power, int):
            if name_or_power >= 5:
                key = CardType.DRAGON.value
            else:
                key = CardType.GOBLIN.value

        if key == CardType.DRAGON.value:
            card = CreatureCard("Fire Dragon", 5, "Legendary", 7, 5)
        elif key == CardType.GOBLIN.value:
            card = CreatureCard("Goblin Warrior", 2, "Common", 3, 2)
        else:
            raise ValueError(f"Unknown: {name_or_power.value}")

        self.cards_created += 1
        return card

    def create_spell(self, name_or_power: object) -> SpellCard:
        key = str(name_or_power).lower()
        if isinstance(name_or_power, CardType):
            key = name_or_power.value

        cost = 3
        if isinstance(name_or_power, int):
            cost = name_or_power
            key = "lightning"

        if key == CardType.LIGHTNING.value:
            card = SpellCard("Lightning Bolt", cost, "Common", "damage")
        else:
            raise ValueError(f"Unknown: {name_or_power.value}")

        self.cards_created += 1
        return card

    def create_artifact(self, name_or_power: object) -> ArtifactCard:
        key = str(name_or_power).lower()
        if isinstance(name_or_power, CardType):
            key = name_or_power.value

        cost = 2
        if isinstance(name_or_power, int):
            cost = name_or_power

        if key == CardType.MANA_RING.value:
            card = ArtifactCard(
                "Mana Ring", cost, "Rare", 3, "Permanent: +1 mana per turn"
            )
        else:
            raise ValueError(f"Unknown: {name_or_power.value}")

        self.cards_created += 1
        return card

    def create_themed_deck(self, size: int) -> dict:
        cards = []
        try:
            for index in range(size):
                slot = index % 4
                if slot == 0:
                    cards.append(self.create_creature(CardType.DRAGON))
                elif slot == 1:
                    cards.append(self.create_creature(CardType.GOBLIN))
                elif slot == 2:
                    cards.append(self.create_spell(CardType.LIGHTNING))
                else:
                    cards.append(self.create_artifact(CardType.MANA_RING))
        except Exception as e:
            print(e)

        return {
            "theme": "Fantasy",
            "cards": cards,
            "size": len(cards),
        }

    def get_supported_types(self) -> dict:
        return {
            "creatures": [CardType.DRAGON.value, CardType.GOBLIN.value],
            "spells": [CardType.FIREBALL.value],
            "artifacts": [CardType.MANA_RING.value],
        }
