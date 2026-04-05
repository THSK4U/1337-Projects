import json
from models import FunctionDefinition, TestPrompt


def parse_functions_definition(file_path: str) -> list[FunctionDefinition]:
    with open(file_path, "r") as file:
        data = json.load(file)

    results = []
    for obj in data:
        results.append(FunctionDefinition(**obj))
    return results


def parse_test_prompts(file_path: str) -> list[TestPrompt]:
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
