from ex0.CreatureCard import CreatureCard
from ex1 import ArtifactCard, Deck, SpellCard


def main() -> None:
    print("=== DataDeck Deck Builder ===")

    print("\nBuilding deck with different card types...")
    deck = Deck()

    c1 = CreatureCard("Fire Dragon", 5, "Legendary", 7, 5)
    c2 = ArtifactCard(
        "Mana Crystal", 4, "Common", 5, "Permanent: +1 mana per turn"
    )
    c3 = SpellCard("Lightning Bolt", 3, "Common", "damage")

    deck.add_card(c1)
    deck.add_card(c2)
    deck.add_card(c3)

    print("Deck stats:", deck.get_deck_stats())

    print("\nDrawing and playing cards:")
    drew = deck.draw_card()
    print("\nDrew:", drew.name, f"({drew.type})")
    print(
        "Play result:",
        drew.play(
            {
                "available_mana": 10,
                "effect": "Deal 3 damage to target",
            }
        ),
    )

    drew = deck.draw_card()
    print("\nDrew:", drew.name, f"({drew.type})")
    print(
        "Play result:",
        drew.play(
            {
                "available_mana": 10,
            }
        ),
    )

    drew = deck.draw_card()
    print("\nDrew:", drew.name, f"({drew.type})")
    print(
        "Play result:",
        drew.play(
            {
                "available_mana": 10,
            }
        ),
    )

    print(
        "\nPolymorphism in action: Same interface,",
        "different card behaviors!",
    )


if __name__ == "__main__":
    main()
