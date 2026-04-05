class Plant():
    """
    Serves as a blueprint for any plant (name, height, age).
    """
    def __init__(self, name, height, age):
        """
        Initializes a new Plant with the given attributes.

        Args:
            name: The name of the plant.
            height: The height of the plant.
            age: The age of the plant.
        """
        self.name = name
        self.height = height
        self.age = age
        print(f"{self.name}: {self.height}cm, {self.age} days old")


if __name__ == "__main__":
    print("=== Garden Plant Registry ===")
    Plant("Rose", 25, 30)
    Plant("Sunflower", 80, 45)
    Plant("Cactus", 15, 120)
