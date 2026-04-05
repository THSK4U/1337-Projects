from ex0.Card import Card
from ex3.GameStrategy import GameStrategy


def sort_by_cost(card: Card) -> int:
    return card.cost


class AggressiveStrategy(GameStrategy):
    def execute_turn(self, hand: list, battlefield: list) -> dict:
        del battlefield
        mana_budget = 5
        remaining_mana = mana_budget
        cards_played: list[str] = []
        damage_dealt = 0

        ordered_hand = sorted(hand, key=sort_by_cost)

        for card in ordered_hand:
            if card.cost > remaining_mana:
                continue

            remaining_mana -= card.cost
            cards_played.append(card.name)

            if card.type == "Creature":
                damage_dealt += card.attack
            elif card.type == "Spell":
                damage_dealt += 5

        return {
            "cards_played": cards_played,
            "mana_used": mana_budget - remaining_mana,
            "targets_attacked": self.prioritize_targets(["Enemy Player"]),
            "damage_dealt": damage_dealt,
        }

    def get_strategy_name(self) -> str:
        return "AggressiveStrategy"

    def prioritize_targets(self, available_targets: list) -> list:
        return available_targets
