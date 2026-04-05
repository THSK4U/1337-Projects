class Plant():
    """
    Serves as a blueprint for any plant (name, height, age).
    """
    def __init__(self, name, height, age):
        """
        Initializes a new Plant and prints its creation details.

        Args:
            name: Plant name.
            height: Initial height.
            age: Initial age.
        """
        self.name = name
        self.height = height
        self.age = age
        print(f"Created: {self.name} ({self.height}cm, {self.age} days)")


if __name__ == "__main__":
    list = [
        ["Rose", 25, 30],
        ["Oak", 200, 365],
        ["Cactus", 5, 90],
        ["Sunflower", 80, 45],
        ["Fern", 15, 120]
    ]
    i = 0
    print("=== Plant Factory Output ===")
    for name, height, age in list:
        Plant(name, height, age)
        i += 1
    print(f"\nTotal plants created: {i}")
