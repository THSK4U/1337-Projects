from ex0.CreatureCard import CreatureCard


def main() -> None:
    print("""=== DataDeck Card Foundation ===

Testing Abstract Base Class Design:
""")
    card = CreatureCard("Fire Dragon", 5, "Legendary", 7, 5)
    print(f"CreatureCard Info:\n{card.get_card_info()}")

    available_mana = 6
    print(f"\nPlaying {card.name} with {available_mana} mana available:")
    print("Playable:", card.is_playable(available_mana))
    print(
        "Play result:",
        card.play(
            {
                "available_mana": available_mana,
            }
        ),
    )

    print(f"\n{card.name} attacks Goblin Warrior:")
    print("Attack result:", card.attack_target("Goblin Warrior"))

    available_mana = 3
    print(f"\nTesting insufficient mana ({available_mana} available):")
    print("Playable:", card.is_playable(available_mana))

    print("\nAbstract pattern successfully demonstrated!")


if __name__ == "__main__":
    main()
