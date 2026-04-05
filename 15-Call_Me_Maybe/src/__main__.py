from decoder import run_pipeline
from parser import parse_functions_definition, parse_test_prompts
from models import TestPrompt, FunctionCallResult, FunctionDefinition
import json
import re

def main():
    try:
        functions_definition = parse_functions_definition(r"data/input/functions_definition.json")
        prompts_test = parse_test_prompts(r"data/input/function_calling_tests.json")
        result = []

        fallback_fn = FunctionDefinition(
        name="fn_is_not",
        description="Call this function only when no available function is relevant to the user query.",
        parameters={ "s": { "type":"string"}}
        )
        extended_functions = [fallback_fn] + functions_definition

        for prompt in prompts_test:
            dict_output = run_pipeline(extended_functions, prompt)

            result.append(dict_output)
            print(f"\r{dict_output}\n")

        with open("./data/output/function_calling_results.json", "w") as f:
            json.dump(result, f, indent=4)
    except Exception as e:
        print("\n[ERROR]", e)
        exit()


if __name__ == "__main__":
    main()
