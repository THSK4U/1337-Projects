from typing import Callable, Any


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combiner(*args: Any, **keyword: Any) -> tuple:
        return (spell1(*args, **keyword), spell2(*args, **keyword))

    return combiner


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplifier(*arg: Any, **keyword: Any) -> int:
        return int(base_spell(*arg, **keyword) * multiplier)

    return amplifier


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def caster(*arg: Any, **keyword: Any) -> bool | str:
        return (
            spell(*arg, **keyword)
            if condition(*arg, **keyword)
            else "Spell fizzled"
        )

    return caster


def spell_sequence(spells: list[Callable]) -> Callable:
    def sequence(*arg: Any, **keyword: Any) -> list:
        result = []
        for spell in spells:
            result.append(spell(*arg, **keyword))
        return result

    return sequence


def main() -> None:
    print("\nTesting spell combiner...")

    combiner = spell_combiner(
        lambda target, attacker: f"{attacker} hits {target}",
        lambda target, attacker=None: f"Heals {target}",
    )
    print("Combined spell result:", ", ".join(combiner("Dragon", "Fireball")))

    print("\nTesting power amplifier...")

    def fireball(number: int) -> int:
        return int((number * 10) / 10)

    number = 10
    mega_fireball = power_amplifier(fireball, 3)
    print(f"Original: {fireball(number)}, Amplified: {mega_fireball(number)}")


main()
