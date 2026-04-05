data_list = {
    'alice': [
        'first_blood', 'pixel_perfect', 'speed_runner', 'first_blood',
        'level_10', 'first_kill'
    ],
    'bob': [
        'level_master', 'boss_hunter', 'treasure_seeker', 'level_master',
        'level_10', 'first_kill'
    ],
    'charlie': [
        'treasure_seeker', 'boss_hunter', 'combo_king', 'first_blood',
        'boss_hunter', 'first_blood', 'level_10', 'first_blood'
    ],
}


class achievements():
    def __init__(self, name, achievements):
        self.name = name
        self.achievements = set(achievements)

    def display(self):
        print(f"Player {self.name} achievements: ", end="")
        print(self.achievements)


def main():
    print("=== Achievement Tracker System ===")
    print()
    alice = achievements("alice", data_list["alice"])
    bob = achievements("bob", data_list["bob"])
    charlie = achievements("charlie", data_list["charlie"])

    alice.display()
    bob.display()
    charlie.display()
    print()

    print("=== Achievement Analytics ===")
    all_unique = alice.achievements.union(
        bob.achievements, charlie.achievements
    )
    print("All unique achievements:", all_unique)
    print("Total unique achievements:", len(all_unique))
    print()

    all_common = alice.achievements.intersection(
        bob.achievements, charlie.achievements
    )
    print("Common to all players:", all_common)

    rare_alice = alice.achievements.difference(
        bob.achievements, charlie.achievements
    )
    rare_bob = bob.achievements.difference(
        alice.achievements, charlie.achievements
    )
    rare_charlie = charlie.achievements.difference(
        bob.achievements, alice.achievements
    )

    rare = rare_alice.union(rare_bob, rare_charlie)
    print("Rare achievements (1 player):", rare)
    print()

    print(
        "Alice vs Bob common:",
        alice.achievements.intersection(bob.achievements)
    )
    print("Alice unique:", alice.achievements.difference(bob.achievements))
    print("Bob unique:", bob.achievements.difference(alice.achievements))


main()
