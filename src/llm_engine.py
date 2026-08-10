import json
import torch

from llm_sdk import Small_LLM_Model
from src.schemas import FunctionsDefinition, FunctionCallingResults

SYSTEM_PROMPT = """You are a precise function calling assistant.
Given a list of available functions in JSON format and a user prompt,
 select the best function and extract its arguments.

Available Functions:
{functions_json}

User Prompt: {user_prompt}

CRITICAL INSTRUCTIONS:
1. Respond ONLY with a valid JSON object.
2. Do NOT write any markdown formatting like ```json or ```.
3. Do NOT add explanations, intro text, or outro text.
4. The JSON must strictly match this structure:
{{
    "prompt": "{user_prompt}",
    "name": "<chosen_function_name>",
    "parameters": {{
        "<parameter_name>": <value>
    }}
}}
"""


def generate_text(model: Small_LLM_Model, prompt_text: str) -> str:
    inputs_ids = model.encode(prompt_text)
    with torch.no_grad():
        output_ids = model._model.generate(
            inputs_ids,
            max_new_tokens=200,
            do_sample=False,
            pad_token_id=model._tokenizer.pad_token_id,
        )
    new_tokens = output_ids[0][inputs_ids.shape[1]:]
    decoded_text: str = model.decode(new_tokens)
    return decoded_text.strip()


def process_single_test(
    model: Small_LLM_Model,
    user_prompt: str,
    functions: list[FunctionsDefinition],
) -> FunctionCallingResults | None:
    functions_data = [f.model_dump() for f in functions]
    functions_json = json.dumps(functions_data, indent=2)

    full_prompt = SYSTEM_PROMPT.format(
        functions_json=functions_json,
        user_prompt=user_prompt
    )
    raw_response = generate_text(model, full_prompt)

    try:
        data = json.loads(raw_response)
        data["prompt"] = user_prompt
        return FunctionCallingResults(**data)
    except (json.JSONDecodeError, Exception) as error:
        print(f"ERROR parsing JSON to '{user_prompt}': {error}")
        print(f"Raw answer of model: {raw_response}")
        return None
