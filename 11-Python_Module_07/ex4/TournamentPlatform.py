from ex4.TournamentCard import TournamentCard


def leaderboard_sort_key(card: TournamentCard) -> tuple[int, int]:
    return (card.rating, card.wins)


class TournamentPlatform:
    def __init__(self) -> None:
        self.cards: dict[str, TournamentCard] = {}
        self.matches_played = 0

    def register_card(self, card: TournamentCard) -> str:
        card_id = card.card_id
        if card_id in self.cards:
            raise ValueError("Card ID already registered")
        self.cards[card_id] = card
        return card_id

    def create_match(self, card1_id: str, card2_id: str) -> dict:
        if card1_id not in self.cards or card2_id not in self.cards:
            raise ValueError("Card ID not found")
        if card1_id == card2_id:
            raise ValueError("A card cannot match against itself")

        card1 = self.cards[card1_id]
        card2 = self.cards[card2_id]

        score1 = card1.attack_power + card1.rating
        score2 = card2.attack_power + card2.rating

        if score1 >= score2:
            winner = card1
            loser = card2
        else:
            winner = card2
            loser = card1

        winner.update_wins(1)
        loser.update_losses(1)
        self.matches_played += 1

        return {
            "winner": winner.card_id,
            "loser": loser.card_id,
            "winner_rating": winner.rating,
            "loser_rating": loser.rating,
        }

    def get_leaderboard(self) -> list[dict[str, str | int]]:
        ordered_cards = sorted(
            self.cards.values(),
            key=leaderboard_sort_key,
            reverse=True,
        )
        leaderboard: list[dict[str, str | int]] = []
        for card in ordered_cards:
            leaderboard.append(
                {
                    "card_id": card.card_id,
                    "name": card.name,
                    "rating": card.rating,
                    "record": f"{card.wins}-{card.losses}",
                }
            )
        return leaderboard

    def generate_tournament_report(self) -> dict:
        total_cards = len(self.cards)
        avg_rating = 0
        if total_cards > 0:
            avg_rating = int(
                sum(card.rating for card in self.cards.values()) / total_cards
            )

        status = "active" if total_cards > 0 else "empty"
        return {
            "total_cards": total_cards,
            "matches_played": self.matches_played,
            "avg_rating": avg_rating,
            "platform_status": status,
        }
