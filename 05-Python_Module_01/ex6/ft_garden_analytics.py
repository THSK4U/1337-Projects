class Plant():
    """
    Base class for any plant in the garden.
    """
    def __init__(self, name, height):
        self.name = name
        self.height = height
        self.color = None
        self.prize_value = None


class FloweringPlant(Plant):
    """
    Represents a plant that flowers.
    """
    def __init__(self, name, height, color):
        super().__init__(name, height)
        self.color = color


class PrizeFlower(FloweringPlant):
    """
    Represents a prize-winning flower.
    """
    def __init__(self, name, height, color, prize_value):
        super().__init__(name, height, color)
        self.prize_value = prize_value


class GardenManager:
    """
    Manages a garden and its plants.
    """
    gardens_count = 0

    def __init__(self):
        self.garden_name = None
        self.plants = []
        self.total_plant = 0
        self.total_grew = 0

    @classmethod
    def create_garden(cls, gardename):
        """
        Creates a new garden instance and increments the garden count.
        """
        cls.gardens_count += 1
        new_instance = cls()
        new_instance.garden_name = gardename
        return new_instance

    @classmethod
    def create_garden_network(cls, *managers):
        """
        Class method acting on the class itself/multiple instances.
        Calculates and compares scores across different gardens.
        """
        print("Garden scores - ", end='')
        for manager in managers:
            score = cls.GardenStats.calculate_score(manager)
            print(f"{manager.garden_name}: {score}", end=' ')

        print(f"\nTotal gardens managed: {cls.gardens_count}")

    def add_plant(self, plant):
        """
        Adds a plant to the garden.
        """
        self.plants += [plant]
        self.total_plant += 1
        print(f"Added {plant.name} to {self.garden_name}'s garden")

    def grow_all(self):
        """
        Simulates growth for all plants in the garden.
        """
        print(f"{self.garden_name} is helping all plants grow...")
        for plant in self.plants:
            self.total_grew += 1
            plant.height += 1
            print(f"{plant.name} grew 1cm")

    def get_all(self):
        """
        Prints details of all plants in the garden.
        """
        print("Plants in garden:")
        for plant in self.plants:
            print(f"- {plant.name}: {plant.height}cm", end="")
            if plant.color:
                print(f", {plant.color} flowers (blooming)", end="")
            if plant.prize_value:
                print(f", Prize points: {plant.prize_value}", end="")
            print()

    @staticmethod
    def validate_height(height):
        """
        Validates if the height is positive.
        """
        return height > 0

    class GardenStats:
        """
        Helper class for garden statistics and reports.
        """
        def get_report(self):
            """
            Generates and prints a detailed report of the garden.
            """
            is_valid = 0
            regular_count = 0
            flowering_count = 0
            prize_count = 0
            print(f"=== {self.garden_name}'s Garden Report ===")
            self.get_all()
            print(f"\nPlants added: {self.total_plant},", end=" ")
            print(f"Total growth: {self.total_grew}cm")
            for plant in self.plants:
                if plant.prize_value is not None:
                    prize_count += 1
                elif plant.color is not None:
                    flowering_count += 1
                else:
                    regular_count += 1
            print(f"Plant types: {regular_count} regular,", end="")
            print(
                f"{flowering_count} flowering, "
                f"{prize_count} prize flowers\n"
            )

            for p in self.plants:
                is_valid += GardenManager.validate_height(p.height)
            if is_valid:
                print("Height validation test: True")
            else:
                print("Height validation test: False")

        @staticmethod
        def calculate_score(self):
            """
            Calculates the total score of the garden based on plant attributes.
            """
            score = 0
            for plant in self.plants:
                score += plant.height
                if plant.prize_value is not None:
                    score += 20
                if plant.color is not None:
                    score += 10
            return score


print("=== Garden Management System Demo ===\n")
alice = GardenManager.create_garden("Alice")

plant1 = Plant("Oak Tree", 100)
plant2 = FloweringPlant("Rose", 25, "red")
plant3 = PrizeFlower("Sunflower", 50, "yellow", 10)
alice.add_plant(plant1)
alice.add_plant(plant2)
alice.add_plant(plant3)
print()
alice.grow_all()
print()
alice.GardenStats.get_report(alice)
# ----

bob = GardenManager.create_garden("bob")

plant4 = PrizeFlower("Sunflower", 50, "yellow", 10)

bob.add_plant(plant4)

GardenManager.create_garden_network(alice, bob)
