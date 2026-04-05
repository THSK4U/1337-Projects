from abc import ABC, abstractmethod


class Rankable(ABC):
    def calculate_rating(self) -> int: ...

    calculate_rating = abstractmethod(calculate_rating)

    def update_wins(self, wins: int) -> None: ...

    update_wins = abstractmethod(update_wins)

    def update_losses(self, losses: int) -> None: ...

    update_losses = abstractmethod(update_losses)

    def get_rank_info(self) -> dict: ...

    get_rank_info = abstractmethod(get_rank_info)
