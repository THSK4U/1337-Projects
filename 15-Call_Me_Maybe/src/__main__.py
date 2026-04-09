from .decoder import run_pipeline
from .parser import (
    parse_functions_definition,
    parse_test_prompts,
    parse_optional_arguments,
)
from .models import FunctionDefinition, FunctionParameter
import json
import time
import sys

class Colors:
    """ANSI color codes used by the terminal UI."""

    RED = "\033[91m"
    GREEN = "\033[92m"
    END = "\033[0m"
    DARK_GRAY = '\033[90m'


def main() -> None:
    """Run the main entrypoint executing the model inference loop."""
    try:
        args = parse_optional_arguments()

        start_time = time.time()
        print(f"""{Colors.RED}Tsellak Json MAKER:
{Colors.END}""")
        functions_definition = parse_functions_definition(
            args.functions_definition
        )
        prompts_test = parse_test_prompts(args.input)
        result = []

        fallback_fn = FunctionDefinition(
            name="fn_is_not",
            description="Call this function only when no available function \
            is relevant to the user query.",
            parameters={"s": FunctionParameter(type="string")},
        )
        extended_functions = [fallback_fn] + functions_definition

        for prompt in prompts_test:
            try:
                dict_output = run_pipeline(extended_functions, prompt)

                result.append(dict_output)
                print(f"\r\033[K{Colors.DARK_GRAY}Result:")
                print(f"\n{Colors.GREEN}{json.dumps(dict_output, indent=3)}")
                print(f"{Colors.DARK_GRAY}{'`' * 15}\n{Colors.END}")
            except Exception as e:
                print(f"\n{Colors.RED}[ERROR] {e}{Colors.END}", file=sys.stderr)
                continue
        end_time = time.time()
        timer = (end_time - start_time) / 60
        print(f"Time Take : {timer:.2f} Minute")
        with open(args.output, "w") as f:
            json.dump(result, f, indent=4)
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[STOP]{Colors.END} Execution interrupted by user. Cleaning up...")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR] {e}{Colors.END}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
