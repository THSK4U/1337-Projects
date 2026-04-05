from ex0.Card import Card
from ex2.Combatable import Combatable
from ex4.Rankable import Rankable


class TournamentCard(Card, Combatable, Rankable):
    def __init__(
        self,
        card_id: str,
        name: str,
        cost: int,
        rarity: str,
        attack: int,
        health: int,
        base_rating: int = 1200,
    ):
        if not isinstance(card_id, str):
            raise ValueError("card_id must be a non-empty string")
        if (
            not isinstance(attack, int)
            or attack <= 0
        ):
            raise ValueError("attack must be a positive integer")
        if (
            not isinstance(health, int)
            or health <= 0
        ):
            raise ValueError("health must be a positive integer")
        if (
            not isinstance(base_rating, int)
            or base_rating <= 0
        ):
            raise ValueError("base_rating must be a positive integer")
        super().__init__(name, cost, rarity)
        self.card_id = card_id
        self.attack_power = attack
        self.max_health = health
        self.current_health = health
        self.wins = 0
        self.losses = 0
        self.base_rating = base_rating
        self.rating = base_rating

    def play(self, game_state: dict) -> dict:
        available_mana = game_state.get("available_mana", 0)
        if not self.is_playable(available_mana):
            return {
                "card_played": self.name,
                "mana_used": 0,
                "effect": "Not enough mana to play this tournament card",
            }
        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Tournament card deployed",
        }

    def attack(self, target: str) -> dict:
        return {
            "attacker": self.name,
            "target": target,
            "damage_dealt": self.attack_power,
            "combat_resolved": True,
        }

    def defend(self, incoming_damage: int) -> dict:
        if incoming_damage < 0:
            incoming_damage = 0
        self.current_health -= incoming_damage
        still_alive = self.current_health > 0
        return {
            "defender": self.name,
            "damage_taken": incoming_damage,
            "still_alive": still_alive,
        }

    def get_combat_stats(self) -> dict:
        return {
            "attack": self.attack_power,
            "health": self.current_health,
            "max_health": self.max_health,
        }

    def calculate_rating(self) -> int:
        rating_delta = (16 * self.wins) - (16 * self.losses)
        self.rating = max(100, self.base_rating + rating_delta)
        return self.rating

    def update_wins(self, wins: int) -> None:
        self.wins += wins
        self.calculate_rating()

    def update_losses(self, losses: int) -> None:
        self.losses += losses
        self.calculate_rating()

    def get_rank_info(self) -> dict:
        return {
            "card_id": self.card_id,
            "rating": self.rating,
            "wins": self.wins,
            "losses": self.losses,
        }

    def get_tournament_stats(self) -> dict:
        return {
            "card_id": self.card_id,
            "name": self.name,
            "rating": self.rating,
            "record": f"{self.wins}-{self.losses}",
            "combat": self.get_combat_stats(),
        }
