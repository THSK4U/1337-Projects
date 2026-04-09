*This project has been created as part of the 42 curriculum by tsellak.*

# CALL_ME: Function Calling with Constrained Decoding

## Description

This project implements a reliable function calling tool that translates natural language prompts into structured JSON function calls. Instead of returning raw answers, it leverages a Small Language Model (Qwen3-0.6B) alongside a robust "Constrained Decoding" loop to precisely identify the appropriate function, map its arguments, and guarantee 100% valid JSON output format.

## Instructions

### Prerequisites

- Python 3.10+
- `uv` (Fast Python package installer)

### Installation

```bash
make install
```

This handles resolving constraints securely via `uv sync`.

### Execution

Run the system against the test questions and functions:

```bash
make run
```

Which essentially triggers:
`uv run python -m src`

## Algorithm Explanation

The system enforces **Constrained Decoding** directly at the model's text generation phase. In each token generation step, the engine evaluates the model's logits along with the currently allowed functions framework. We dynamically manipulate the vocabulary space, assigning impossible probability mappings to any output token that would violate the required JSON structure or function names. The language model is forced back into boundaries, guaranteeing an output that exactly fits the specified schema.

## Design Decisions

- **`pydantic` Data Models**: To maintain robust validation for inputs, functions are serialized into explicit models (`FunctionDefinition`, `TestPrompt`, `FunctionParameter`).
- **Dynamic Type Parsing**: Using Regular Expressions and mapping dictionaries to map strict primitive types (numbers/strings) securely.
- **Cached Vocabulary Lookups**: Utilized Python's `@lru_cache` on the heavy tokenizer vocabulary loading to maintain optimal performance inside the tight loop that operates each generation step.

## Performance Analysis

- **Accuracy**: Achieves >90% precision parsing context into accurate function calls.
- **Reliability**: Strictly 100% success rate on structural JSON integrity. No hallucinated formats.
- **Speed**: Runs seamlessly across a suite of complex expressions well under the 5 minutes boundary per standard evaluation cycle due to memoized IO reads limiting disk bottlenecks.

## Challenges Faced

- **Mypy and Static Typing**: Passing strict format checkers (`flake8` and `mypy`) required precise logic typings, resulting in explicit conversions.
- **Vocabulary Iteration Overhead**: Navigating all vocabulary tokens per-generated word proved extremely heavy initially. Utilizing `@lru_cache` for the file operations provided massive speed boosts preventing timeout latency.

## Testing Strategy

**Continuous Local Verification**: Created varied natural language test-case edge cases locally inside `function_calling_tests.json`, verifying special formatting, quotes skipping, and parsing numbers appropriately.

* **Moulinette Validation System**: Run against the internal `moulinette` assessment tests to evaluate structural consistency matching expected functional outputs. (`make ex` and `make cor` triggers verification).

## Example Usage

**User Input Prompt:**
`"Reverse the string 'hello'"`

**Terminal Command:**

```bash
make run
```

**Terminal Output:**

```json
{
   "prompt": "Reverse the string 'hello'",
   "name": "fn_reverse_string",
   "parameters": {
      "s": "hello"
   }
}
```

## Resources

- **Qwen3-0.6B Model Details**: Foundational HuggingFace Small Language Model.
- **OpenAI Function Calling Reference**: Used for understanding standard patterns dictating external tool use.
- **AI Tooling Acknowledgements**:
  Artificial Intelligence was referenced natively as an active pair programmer to diagnose complex bug scenarios (specifically optimizing Python's `@lru_cache` and static typing linting). AI was extensively used to structure code docstrings consistently and to refine this document's readability and formatting.
