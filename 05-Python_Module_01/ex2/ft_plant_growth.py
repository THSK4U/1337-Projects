class Plant():
    """
    Serves as a blueprint for any plant (name, height, age).
    """
    def __init__(self, name, height, age):
        """
        Initializes a new Plant.

        Args:
            name: Plant name.
            height: Initial height.
            age: Initial age.
        """
        self.name = name
        self.height = height
        self._age = age

    def grow(self):
        """
        Simulates the plant growing.
        Increases height by the growth rate (1cm).
        """
        self.height += 1

    def age(self):
        """
        Simulates the plant aging.
        Increases age by 1 day.
        """
        self._age += 1

    def get_info(self):
        """
        Prints the current status of the plant.
        """
        print(f"{self.name}: {self.height}cm, {self._age} days old")


if __name__ == "__main__":
    plant = Plant("Rose", 25, 30)
    day = 7
    i = 0
    print("=== Day 1 ===")
    plant.get_info()
    while i < day - 1:
        plant.grow()
        plant.age()
        i += 1
    print(f"=== Day {day} ===")
    plant.get_info()
    print(f"Growth this week: +{i}cm")
