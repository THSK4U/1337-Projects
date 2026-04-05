from ex4.TournamentCard import TournamentCard
from ex4.TournamentPlatform import TournamentPlatform


def main() -> None:
    print("=== DataDeck Tournament Platform ===")
    print("Registering Tournament Cards...")

    platform = TournamentPlatform()
    dragon = TournamentCard(
        "dragon_001",
        "Fire Dragon",
        5,
        "Legendary",
        7,
        5,
        1200,
    )
    wizard = TournamentCard(
        "wizard_001",
        "Ice Wizard",
        4,
        "Epic",
        5,
        4,
        1150,
    )

    id1 = platform.register_card(dragon)
    id2 = platform.register_card(wizard)

    print(f"\n{dragon.name} (ID: {id1}):")
    print("- Interfaces: [Card, Combatable, Rankable]")
    print(f"- Rating: {dragon.rating}")
    print(f"- Record: {dragon.wins}-{dragon.losses}")
    print(f"\n{wizard.name} (ID: {id2}):")
    print("- Interfaces: [Card, Combatable, Rankable]")
    print(f"- Rating: {wizard.rating}")
    print(f"- Record: {wizard.wins}-{wizard.losses}")

    print("\nCreating tournament match...")
    match_result = platform.create_match(id1, id2)
    print("Match result:", match_result)

    print("\nTournament Leaderboard:")
    leaderboard = platform.get_leaderboard()
    for index, row in enumerate(leaderboard, start=1):
        print(
            f"{index}. {row['name']} - Rating: {row['rating']} "
            f"({row['record']})"
        )

    print("\nPlatform Report:")
    print(platform.generate_tournament_report())
    print("\n=== Tournament Platform Successfully Deployed! ===")
    print("All abstract patterns working together harmoniously!")


if __name__ == "__main__":
    main()
