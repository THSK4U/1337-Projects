from ex0.Card import Card


class CreatureCard(Card):
    def __init__(
        self, name: str, cost: int, rarity: str, attack: int, health: int
    ):
        if attack <= 0:
            raise ValueError("attack must be a positive integer")
        if health <= 0:
            raise ValueError("health must be a positive integer")
        super().__init__(name, cost, rarity)
        self.attack = attack
        self.health = health

    def play(self, game_state: dict) -> dict:
        available_mana = game_state.get("available_mana", 0)
        if not self.is_playable(available_mana):
            return {
                "Error": "Not enough mana to play this creature",
            }
        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Creature summoned to battlefield",
        }

    def attack_target(self, target: str) -> dict:
        if target is not None:
            return {
                "attacker": self.name,
                "target": target,
                "damage_dealt": self.attack,
                "combat_resolved": True,
            }
        return {
            "attacker": self.name,
            "target": target,
            "damage_dealt": 0,
            "combat_resolved": False,
        }

    def get_card_info(self) -> dict:
        return {
            **super().get_card_info(),
            "attack": self.attack,
            "health": self.health,
        }
