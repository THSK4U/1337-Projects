class Plant():
    """
    Base class for any plant.
    """
    def __init__(self, name, height, age):
        """
        Initializes a base Plant.
        """
        self.name = name
        self.height = height
        self.age = age
        print(f"{self.name} ({self.__class__.__name__}):", end=" ")
        print(f"{self.height}cm, {self.age} days,", end=" ")


class Flower(Plant):
    """
    Represents a flower, inheriting from Plant.
    """
    def __init__(self, name, height, age, color):
        """
        Initializes a Flower with a color.
        """
        super().__init__(name, height, age)
        self.color = color
        print(f"{self.color} color")

    def bloom(self):
        """
        Simulates the flower blooming.
        """
        print(f"{self.name} is blooming beautifully!")


class Tree(Plant):
    """
    Represents a tree, inheriting from Plant.
    """
    def __init__(self, name, height, age, trunk_diameter):
        """
        Initializes a Tree with trunk diameter.
        """
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter
        print(f"{self.trunk_diameter} diameter")

    def produce_shade(self):
        """
        Calculates and prints the shade produced by the tree.
        """
        shade = ((self.height / 100) ** 2) * 3.14
        print(f"{self.name} provides {shade:.0f} square meters of shade")


class Vegetable(Plant):
    """
    Represents a vegetable, inheriting from Plant.
    """
    def __init__(self, name, height, age, harvest_season, nutritional_value):
        """
        Initializes a Vegetable with harvest season and nutritional value.
        """
        super().__init__(name, height, age)
        self.harvest_season = harvest_season
        self.nutritional = nutritional_value
        print(f"{self.harvest_season} harvest")

    def nutritional_info(self):
        """
        Prints the nutritional information of the vegetable.
        """
        print(f"{self.name} is rich in {self.nutritional}")


if __name__ == "__main__":
    print("=== Garden Plant Types ===")
    rose = Flower("Rose", 25, 30, "red")
    rose.bloom()
    tulip = Flower("Tulip", 15, 12, "yellow")
    tulip.bloom()
    print()
    oak = Tree("Oak", 500, 1825, 50)
    oak.produce_shade()
    pine = Tree("Pine", 300, 1000, 30)
    pine.produce_shade()
    print()
    tomat = Vegetable("Tomato", 80, 90, "summer", "Vitamin C")
    tomat.nutritional_info()
    carrot = Vegetable("Carrot", 10, 60, "spring", "Vitamin A")
    carrot.nutritional_info()
