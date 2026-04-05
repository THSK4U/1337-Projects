from typing import Callable
from time import time, sleep
from functools import wraps


def spell_timer(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Casting", func.__name__)
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        print(f"Spell completed in {(end_time - start_time):.3} seconds")
        return result

    return wrapper


def power_validator(min_power: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                power = args[2]
                if power >= min_power:
                    return func(*args, **kwargs)
            except IndexError:
                return "Expected power as the third positional argument"

            return "Insufficient power for this spell"

        return wrapper

    return decorator


def retry_spell(max_attempts: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            mutable_args = list(args)
            for attempt in range(1, max_attempts + 1):
                try:
                    mutable_args[2] -= 20
                    return func(*mutable_args, **kwargs)
                except Exception:
                    if attempt < max_attempts:
                        print("Spell failed, retrying..")
                        sleep(1)
                    else:
                        return (
                            "pell casting failed after max_attempts attempts"
                        )

        return wrapper

    return decorator


class MageGuild:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def validate_mage_name(name: str) -> bool:
        cleaned = name.strip()
        if len(cleaned) < 3:
            return False

        for ch in cleaned:
            if not (ch.isalpha() or ch.isspace()):
                return False

        return True

    @power_validator(10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


def main() -> None:
    print("\nTesting spell timer...")

    @spell_timer
    def fireball(spell_name):
        sleep(0.101)
        return f"{spell_name.capitalize()} cast!"

    print("Result:", fireball("fireball"))

    print("\nTesting MageGuild...")
    cast = MageGuild("Lightning")
    print(cast.validate_mage_name(cast.name))
    print(cast.validate_mage_name(cast.name + "15"))
    print(cast.cast_spell(cast.name, 15))

    print(cast.cast_spell(cast.name, 1))


main()
