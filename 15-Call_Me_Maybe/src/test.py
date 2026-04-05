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

def generate_constrained(prompt_ids, allowed_strings=None, stop_char=None):
    generated_text = ""

    while True:
        logits = llm.get_logits_from_input_ids(prompt_ids)

        if allowed_strings:
            current_typed = generated_text
            valid_ids = [t_id for t_str, t_id in vocab.items()
                        if any((current_typed + t_str).startswith(s) for s in allowed_strings)]

            if valid_ids:
                next_token_id = valid_ids[0]
                for v_id in valid_ids:
                    if logits[v_id] > logits[next_token_id]: next_token_id = v_id
            else:
                next_token_id = logits.index(max(logits))
        else:
            next_token_id = logits.index(max(logits))

        word = llm.decode([next_token_id])
        generated_text += word
        prompt_ids.append(next_token_id)
        print(word, end="", flush=True)

        if not stop_char and generated_text.count('{') == generated_text.count('}'):
            break

    return generated_text

def run_pipeline(functions_definition, query_prompt):
    start_json = f'{{"prompt": {json.dumps(query_prompt.prompt)}, "name": "'
    full_prompt = build_prompt(query_prompt, functions_definition) + "\n" + start_json
    prompt_ids = llm.encode(full_prompt)[0].tolist()

    fn_names = [f.name + '"' for f in functions_definition]
    selected_name = generate_constrained(prompt_ids, allowed_strings=fn_names, stop_char='"')

    suffix = ', "parameters": '
    print(suffix, end="")
    prompt_ids.extend(llm.encode(suffix)[0].tolist())

    params_json = generate_constrained(prompt_ids)

    full_json_str = start_json + selected_name + suffix + params_json
    try:
        clean_json = re.sub(r'\\(?!["\\bfnrtu])', r'\\\\', full_json_str)
        data = json.loads(clean_json)
        return FunctionCallResult(**data).model_dump()
    except Exception as e:
        print(f"\nError parsing JSON: {e}")
        return None
