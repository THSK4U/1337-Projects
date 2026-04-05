from ex3.AggressiveStrategy import AggressiveStrategy
from ex3.FantasyCardFactory import FantasyCardFactory
from ex3.GameEngine import GameEngine


def main() -> None:
    print("=== DataDeck Game Engine ===")
    print("\nConfiguring Fantasy Card Game...")

    factory = FantasyCardFactory()
    strategy = AggressiveStrategy()
    engine = GameEngine()
    engine.configure_engine(factory, strategy)

    print("Factory:", factory.__class__.__name__)
    print("Strategy:", strategy.get_strategy_name())
    print("Available types:", factory.get_supported_types())

    print("\nSimulating aggressive turn...")
    turn_report = engine.simulate_turn()
    print("Hand:", turn_report["hand"])

    print("\nTurn execution:")
    print("Strategy:", turn_report["strategy"])
    print("Actions:", turn_report["actions"])

    print("\nGame Report:")
    print(engine.get_engine_status())
    print(
        "\nAbstract Factory + Strategy Pattern: Maximum flexibility achieved!"
    )


if __name__ == "__main__":
    main()
