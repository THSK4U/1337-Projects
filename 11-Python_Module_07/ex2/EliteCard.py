from ex0.Card import Card
from ex2.Combatable import Combatable
from ex2.Magical import Magical


class EliteCard(Card, Combatable, Magical):
    count = 0

    def __init__(
        self,
        name: str,
        cost: int,
        rarity: str,
        attack: int,
        shield: int,
        health: int,
    ):
        super().__init__(name, cost, rarity)
        self.attack_ = attack
        self.shield = shield
        self.play_count = 0
        self.attack_count = 0
        EliteCard.count += 1
        self.defence_count = 0
        self.health = health

    def attack(self, target: str) -> dict:
        self.attack_count += 1
        return {
            "attacker": self.name,
            "target": target,
            "damage": self.attack_,
            "combat_type": "melee",
        }

    def defend(self, incoming_damage: int) -> dict:
        self.defence_count += 1
        if incoming_damage < 0:
            incoming_damage = 0
        if incoming_damage <= self.shield:
            damage_blocked = self.shield - incoming_damage
            damage_taken = incoming_damage
        else:
            damage_blocked = 0
            damage_taken = incoming_damage - self.shield
        self.health -= damage_taken
        still_alive = self.health > 0
        return {
            "defender": self.name,
            "damage_taken": damage_taken,
            "damage_blocked": damage_blocked,
            "still_alive": still_alive,
        }

    def cast_spell(self, spell_name: str, targets: list) -> dict:
        return {
            "caster": self.name,
            "spell": spell_name,
            "targets": targets,
            "mana_used": self.cost,
        }

    def channel_mana(self, amount: int) -> dict:
        return {"channeled": amount, "total_mana": amount + 4}

    def play(self, game_state: dict) -> dict:
        self.play_count += 1
        available_mana = game_state.get("available_mana", 0)
        if not self.is_playable(available_mana):
            return {
                "card_played": self.name,
                "mana_used": 0,
                "effect": "Not enough mana to play this creature",
            }
        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Creature summoned to battlefield",
        }

    def get_combat_stats(self) -> dict:
        return {
            "attack_count": self.attack_count,
            "defence_count": self.defence_count,
        }

    def get_magic_stats(self) -> dict:
        return {"card_count": EliteCard.count, "play_count": self.play_count}
