import json
from .models import FunctionDefinition, TestPrompt
from .parser import parse_test_prompts, parse_functions_definition


def build_prompt(
    prompt: TestPrompt, functions: list[FunctionDefinition]
) -> str:
    """Assemble the system prompt guiding the generation.

    Args:
        prompt: The user query context to include.
        functions: Accessible functions to inject into the prompt.

    Returns:
        A fully formatted text body prompting the LLM for function calling.
    """
    function_json_format = json.dumps(
        [f.model_dump() for f in functions], indent=2
    )
    return f"""
You are a helpful assistant that converts natural \
language to function call JSON.

Here are the available functions:
{function_json_format}

Example Output:
{{"name": "fn_example", "parameters": {{"arg": "value"}}}}

User Query: {prompt.prompt}

- If no available function is relevant to the user query,\
 use the function name "fn_is_not".
"""


if __name__ == "__main__":
    funcs = parse_functions_definition(r"data/input/functions_definition.json")
    prompt = parse_test_prompts(r"data/input/function_calling_tests.json")

    print(build_prompt(prompt[1], funcs))
