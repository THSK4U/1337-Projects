from typing import Callable, Any


def mage_counter() -> Callable:
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def spell_accumulator(initial_power: int) -> Callable:
    total_power = initial_power

    def accumulator(power: int) -> int:
        nonlocal total_power
        total_power += power
        return total_power

    return accumulator


def enchantment_factory(enchantment_type: str) -> Callable:
    return lambda item_name: f"{enchantment_type} {item_name}"


def memory_vault() -> dict[str, Callable]:
    memory_storage = {}

    def store(key: str, value: Any) -> None:
        memory_storage[key] = value

    def recall(key: str):
        return memory_storage.get(key, "Memory not found")

    return {"store": store, "recall": recall}


def main() -> None:
    print("\nTesting mage counter...")
    counter = mage_counter()
    for call in range(1, 4):
        print(f"Call {call}: {counter()}")

    print("\nTesting enchantment factory...")
    factory = enchantment_factory("Flaming")
    print(factory("Sword"))
    factory = enchantment_factory("Frozen")
    print(factory("Shield"))


main()
