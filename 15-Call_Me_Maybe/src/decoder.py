from llm_sdk import Small_LLM_Model as llm_model
from schema import generate_schema
from prompts import build_prompt
from models import TestPrompt, FunctionCallResult, FunctionDefinition
import json
import numpy as np

import json, re

llm = llm_model()
with open(llm.get_path_to_vocab_file(), 'r') as f:
    vocab = json.load(f)

def generate_constrained(prompt_ids, allowed_functions=None, stop_char=None):
    generated_text = ""

    while True:
        logits = llm.get_logits_from_input_ids(prompt_ids)

        if allowed_functions:
            current_typed = generated_text
            valid_ids = [t_id for t_str, t_id in vocab.items()
                        if any(f.startswith(current_typed + t_str) for f in allowed_functions)]

            if valid_ids:
                next_token_id = max(valid_ids, key= lambda v_id: logits[v_id])
            else:
                raise ValueError(f"NO Valid Function Start with {llm.decode([prompt_ids])}")
        else:
            next_token_id = logits.index(max(logits))

        word = llm.decode([next_token_id])
        generated_text += word
        prompt_ids.append(next_token_id)
        print(".", end="", flush=True)

        if stop_char in word :
            break

    return generated_text

def get_type_parameters(functions_definition, selected_name):
    fn_types = {}
    for f in functions_definition:
        if selected_name.startswith(f.name):
            for k, t in f.parameters.items():
                fn_types[k] = t.type

    return fn_types

def run_pipeline(functions_definition, query_prompt):
    try:
        start_json = f'{{"prompt": {json.dumps(query_prompt.prompt)}, "name": "'
        full_prompt = build_prompt(query_prompt, functions_definition) + "\n" + start_json
        prompt_ids = llm.encode(full_prompt)[0].tolist()

        fn_names = [f.name + '"' for f in functions_definition]
        selected_name = generate_constrained(prompt_ids, allowed_functions=fn_names, stop_char='"')

        suffix = ', "parameters": {"'
        # print(suffix, end="")
        prompt_ids.extend(llm.encode(suffix)[0].tolist())

        params_json = generate_constrained(prompt_ids, stop_char='}')

        type_parameters = get_type_parameters(functions_definition, selected_name)
        clean_numbers = params_json

        if "number" in type_parameters.values():
            clean_numbers = re.sub(r'([:\[,]\s*)(-?\d+)(?![\.\d])', r'\g<1>\g<2>.0', params_json)

        full_json_str = start_json + selected_name + suffix + clean_numbers
        try:
            clean_json = re.sub(r'\\(?!["\\bfnrtu])', r'\\\\', full_json_str)
            data = json.loads(clean_json)
            return FunctionCallResult(**data).model_dump()
        except Exception as e:
            print(f"\nError parsing JSON: {e}")
            return None
    except KeyboardInterrupt:
        print("Exit")
        exit()
