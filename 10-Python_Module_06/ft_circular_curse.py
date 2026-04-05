from alchemy.grimoire import record_spell, validate_ingredients


def main():
    print("=== Circular Curse Breaking ===")

    print("\nTesting ingredient validation:")
    print("validate_ingredients(\"fire air\"):",
          validate_ingredients("fire air"))
    print("validate_ingredients(\"dragon scales\"):",
          validate_ingredients("dragon scales"))

    print("\nTesting spell recording with validation:")
    print("record_spell(\"Fireball\", \"fire air\"):",
          record_spell("Fireball", "fire air"))
    print("record_spell(\"Dark Magic\", \"shadow\"):",
          record_spell("Dark Magic", "shadow"))

    print("\nTesting late import technique:")
    print("record_spell(\"Lightning\", \"air\"):",
          record_spell("Lightning", "air"))

    print("""\nCircular dependency curse avoided using late imports!
All spells processed safely!""")


main()
