from ex0.Card import Card


class SpellCard(Card):
    def __init__(self, name: str, cost: int, rarity: str, effect_type: str):
        valid_effect_types = {"damage", "heal", "buff", "debuff"}
        if effect_type not in valid_effect_types:
            raise ValueError(
                "effect_type must be one of: damage, heal, buff, debuff"
            )
        super().__init__(name, cost, rarity)
        self.effect_type = effect_type
        self.is_consumed = False

    def play(self, game_state: dict) -> dict:
        if self.is_consumed:
            return {
                "card_played": self.name,
                "mana_used": 0,
                "effect": "Spell already consumed",
            }
        available_mana = game_state.get("available_mana", 0)
        if not self.is_playable(available_mana):
            return {
                "card_played": self.name,
                "mana_used": 0,
                "effect": "Not enough mana to cast this spell",
            }
        self.is_consumed = True
        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": game_state.get("effect", self.effect_type),
        }

    def resolve_effect(self, targets: list) -> dict:
        return {
            "spell": self.name,
            "effect_type": self.effect_type,
            "targets": targets,
            "targets_affected": len(targets),
            "resolved": True,
        }
