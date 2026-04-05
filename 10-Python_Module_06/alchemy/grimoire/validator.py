def validate_ingredients(ingredients: str) -> str:

    valid = {"fire", "water", "earth", "air"}

    for ingredient in ingredients.split(" "):
        if ingredient not in valid:
            return f"{ingredients} - INVALID"
    return f"{ingredients} - VALID"
