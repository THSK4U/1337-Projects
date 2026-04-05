from random import shuffle as rn_shuffle
from ex0.Card import Card


class Deck:
    def __init__(self) -> None:
        self.cards: list[Card] = []

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def remove_card(self, card_name: str) -> bool:
        for card in self.cards:
            if card.name == card_name:
                self.cards.remove(card)
                return True
        return False

    def shuffle(self) -> None:
        rn_shuffle(self.cards)

    def draw_card(self) -> Card:
        if not self.cards:
            raise ValueError("Cannot draw from an empty deck")
        return self.cards.pop()

    def get_deck_stats(self) -> dict:
        total_cards = len(self.cards)
        if total_cards == 0:
            avg_cost = 0.0
        else:
            avg_cost = sum(card.cost for card in self.cards) / total_cards
        return {
            "total_cards": total_cards,
            "creatures": len(
                [0 for card in self.cards if card.type == "Creature"]
            ),
            "spells": len([0 for card in self.cards if card.type == "Spell"]),
            "artifacts": len(
                [0 for card in self.cards if card.type == "Artifact"]
            ),
            "avg_cost": avg_cost,
        }
