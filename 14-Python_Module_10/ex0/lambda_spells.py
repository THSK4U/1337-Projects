def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(
        artifacts, key=lambda artifact: artifact["power"], reverse=True
    )


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda mage: mage["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: "* " + spell + " *", spells))


def mage_stats(mages: list[dict]) -> dict:
    return {
        "max_power": max(mages, key=lambda mage: mage["power"])["power"],
        "min_power": min(mages, key=lambda mage: mage["power"])["power"],
        "avg_power": sum(map(lambda mage: mage["power"], mages)) / len(mages),
    }


def main() -> None:
    print("\nTesting artifact sorter...")
    artifacts = [
        {"name": "Crystal Orb", "power": 85},
        {"name": "Fire Staff ", "power": 92},
    ]
    sort_data = artifact_sorter(artifacts)
    print(
        f"{sort_data[0]['name']} ({sort_data[0]['power']} power)"
        " comes before ",
        f"{sort_data[-1]['name']} ({sort_data[-1]['power']} power)",
    )
    print("\nTesting spell transformer...")
    spells = ["fireball", "heal", "shield"]
    spell_trans = spell_transformer(spells)
    for spell in spell_trans:
        print(spell, end=" ")


main()
