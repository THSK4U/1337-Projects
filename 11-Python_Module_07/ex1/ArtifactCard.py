from ex0.Card import Card


class ArtifactCard(Card):
    def __init__(
        self, name: str, cost: int, rarity: str, durability: int, effect: str
    ):
        if durability <= 0:
            raise ValueError("must be a positive integer")
        super().__init__(name, cost, rarity)
        self.durability = durability
        self.effect = effect
        self.in_play = False

    def play(self, game_state: dict) -> dict:
        available_mana = game_state.get("available_mana", 0)
        if not self.is_playable(available_mana):
            return {
                "Error": "Not enough mana to play this artifact",
            }
        self.in_play = True
        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": self.effect,
        }

    def activate_ability(self) -> dict:
        if not self.in_play:
            return {
                "artifact": self.name,
                "effect": "Artifact is not in play",
                "durability_remaining": self.durability,
                "active": False,
            }
        if self.durability <= 0:
            self.in_play = False
            return {
                "artifact": self.name,
                "effect": "Artifact destroyed",
                "durability_remaining": 0,
                "active": False,
            }
        self.durability -= 1
        if self.durability == 0:
            self.in_play = False
        return {
            "artifact": self.name,
            "effect": self.effect,
            "durability_remaining": self.durability,
            "active": self.in_play,
        }
