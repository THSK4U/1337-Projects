from typing import Callable
from operator import add, mul, gt
from functools import reduce, partial
from functools import lru_cache, singledispatch


def spell_reducer(spells: list[int], operation: str) -> int:
    if operation == "add":
        return reduce(add, spells)
    if operation == "multiply":
        return reduce(mul, spells)
    if operation == "max":
        return reduce(lambda a, b: a if gt(a, b) else b, spells)
    if operation == "min":
        return reduce(min, spells)


def partial_enchanter(base_enchantment: callable) -> dict[str, callable]:
    fire_enchant = partial(base_enchantment, 50, "fire")
    ice_enchant = partial(base_enchantment, 50, "ice")
    lightning_enchant = partial(base_enchantment, 50, "lightning")

    return {
        "fire_enchant": fire_enchant,
        "ice_enchant": ice_enchant,
        "lightning_enchant": lightning_enchant,
    }


@lru_cache()
def memoized_fibonacci(n: int) -> int:
    return (
        n if n <= 1 else memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)
    )


def spell_dispatcher() -> Callable:

    @singledispatch
    def dispatcher(param) -> str:
        return "Unknown type"

    @dispatcher.register(int)
    def _(damage: int) -> str:
        return f"Damage spell: {damage}"

    @dispatcher.register
    def _(enchantment) -> str:
        return f"Enchantment: {enchantment}"

    @dispatcher.register
    def _(multi_cast: list) -> str:
        return f"Multi-cast spell: {multi_cast}"

    return dispatcher


def main() -> None:
    try:
        print("\nTesting spell reducer...")
        spell_powers = [30, 25, 37, 16, 12, 29]
        print("Sum:", spell_reducer(spell_powers, "add"))
        print("Product:", spell_reducer(spell_powers, "multiply"))
        print("Max:", spell_reducer(spell_powers, "max"))

        print("\nTesting memoized fibonacci...")
        num = 10
        print(f"Fib({num}): {memoized_fibonacci(num)}")
        num = 15
        print(f"Fib({num}): {memoized_fibonacci(num)}")
    except Exception as e:
        print(e)


main()
