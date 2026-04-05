from ex3.CardFactory import CardFactory
from ex3.GameStrategy import GameStrategy


class GameEngine:
    def __init__(self) -> None:
        self.factory: CardFactory | None = None
        self.strategy: GameStrategy | None = None
        self.hand: list = []
        self.battlefield: list = []
        self.turns_simulated = 0
        self.total_damage = 0

    def configure_engine(
        self, factory: CardFactory, strategy: GameStrategy
    ) -> None:
        self.factory = factory
        self.strategy = strategy
        self.turns_simulated = 0
        self.total_damage = 0
        self.battlefield = []
        themed_deck = self.factory.create_themed_deck(3)
        self.hand = themed_deck["cards"]

    def simulate_turn(self) -> dict:
        if self.factory is None or self.strategy is None:
            raise ValueError("Engine is not configured")

        hand = []
        for card in self.hand:
            hand.append(f"{card.name} ({card.cost})")

        actions = self.strategy.execute_turn(self.hand, self.battlefield)
        played_names = list(actions.get("cards_played", []))
        remaining_hand = []

        for card in self.hand:
            if card.name in played_names:
                played_names.remove(card.name)
                if card.type in ("Creature", "Artifact"):
                    self.battlefield.append(card)
            else:
                remaining_hand.append(card)

        self.hand = remaining_hand

        self.turns_simulated += 1
        self.total_damage += actions.get("damage_dealt", 0)
        hand_cards = f"[{', '.join(hand)}]"
        return {
            "hand": hand_cards,
            "strategy": self.strategy.get_strategy_name(),
            "actions": actions,
        }

    def get_engine_status(self) -> dict:
        strategy_name = "Not configured"
        cards_created = 0

        if self.strategy is not None:
            strategy_name = self.strategy.get_strategy_name()
        if self.factory is not None:
            cards_created = self.factory.cards_created

        return {
            "turns_simulated": self.turns_simulated,
            "strategy_used": strategy_name,
            "total_damage": self.total_damage,
            "cards_created": cards_created,
        }
