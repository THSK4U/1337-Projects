import json
from .models import FunctionDefinition, TestPrompt
import argparse


def parse_optional_arguments() -> argparse.Namespace:
    """Parse the command line arguments.

    Returns:
        The namespace containing all configured arguments.
    """
    parser = argparse.ArgumentParser(
        description="Function Calling with Constrained Decoding",
        conflict_handler="error",
    )

    parser.add_argument(
        "--functions_definition",
        type=str,
        default="data/input/functions_definition.json",
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/input/function_calling_tests.json",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output/function_calling_results.json",
    )

    return parser.parse_args()


def parse_functions_definition(file_path: str) -> list[FunctionDefinition]:
    """Parse function definitions from a given JSON file.

    Args:
        file_path: The path to the JSON file containing function structures.

    Returns:
        A list of parsed FunctionDefinition objects.
    """
    with open(file_path, "r") as file:
        data = json.load(file)

    results = []
    for obj in data:
        results.append(FunctionDefinition(**obj))
    return results


def parse_test_prompts(file_path: str) -> list[TestPrompt]:
    """Parse experimental prompts from a JSON file.

    Args:
        file_path: The path to the JSON formatted prompts file.

    Returns:
        A list of parsed TestPrompt objects.
    """
    with open(file_path, "r") as file:
        data = json.load(file)

    results = []
    for obj in data:
        results.append(TestPrompt(**obj))
    return results


if __name__ == "__main__":
    funcs = parse_functions_definition(r"data/input/functions_definition.json")
    for func in funcs:
        print(func.name)

    print("\n\n")
    prompet = parse_test_prompts(r"data/input/function_calling_tests.json")
    print(prompet)
