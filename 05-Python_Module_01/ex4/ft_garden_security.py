class SecurePlant():
    """
    Serves as a blueprint for any plant with secure data access.
    """
    def __init__(self, name):
        """
        Initializes a new SecurePlant.

        Args:
            name: The name of the plant.
        """
        self.name = name
        self.__height = 0
        self.__age = 0
        print(f"Plant created: {self.name}")

    def get_height(self):
        """
        Getter for the private height attribute.

        Returns:
            int: The current height of the plant.
        """
        return self.__height

    def set_height(self, height):
        """
        Setter for the private height attribute.
        Validates that height is non-negative before setting.

        Args:
            height: The new height to set.
        """
        if height < 0:
            print("\nInvalid operation attempted:", end=" ")
            print(f"height {height}cm [REJECTED]")
            print("Security: Negative height rejected")
        else:
            self.__height = height
            print(f"Height updated: {height}cm [OK]")

    def get_age(self):
        """
        Getter for the private age attribute.

        Returns:
            int: The current age of the plant.
        """
        return self.__age

    def set_age(self, age):
        """
        Setter for the private age attribute.
        Validates that age is non-negative before setting.

        Args:
            age: The new age to set.
        """
        if age < 0:
            print(f"\nInvalid operation attempted: age {age}cm [REJECTED]")
            print("Security: Negative age rejected")
        else:
            self.__age = age
            print(f"Age updated: {age} days [OK]")


if __name__ == "__main__":
    print("=== Garden Security System ===")
    plant = SecurePlant("Rose")
    plant.set_height(25)
    plant.set_age(30)
    plant.set_height(-5)
    print(f"\nCurrent plant: {plant.name}", end=" ")
    print(f"({plant.get_height()}cm, {plant.get_age()} days)")
