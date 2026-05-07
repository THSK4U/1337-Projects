from models import FunctionDefinition


def generate_schema(func: FunctionDefinition) -> dict:
    """JSONScHEMA to make a valide json"""

    parameters_shema = {"type": "object", "properties": {}, "required": []}

    for param_name, param_detail in func.parameters.items():
        parameters_shema["properties"][param_name] = {
            "type": param_detail.type
        }
        parameters_shema["required"].append(param_name)

    full_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "enum": [func.name]},
            "parameters": parameters_shema,
        },
        "required": ["name", "parameters"],
    }

    return full_schema


if __name__ == "__main__":
    from parser import parse_functions_definition
    import json

    funcs = parse_functions_definition(r"data/input/functions_definition.json")

    print(json.dumps(generate_schema(funcs[0]), indent=2))
