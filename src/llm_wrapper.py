from llm_sdk.llm_sdk import Small_LLM_Model
from typing import Any


class Wrapper_LLM():
    def __init__(self, model: Small_LLM_Model):
        self.model = model

    def generate(
        self, prompt: str,
        functions_def: list[dict[str, Any]],
        max_tokens: int) -> dict[str, Any]:
        full_prompt = f"""
        You are a function-calling model.
        Return ONLY valid JSON.
        Do not write explanations.

        Allowed function names:
        {[f["name"] for f in functions_def]}

        User prompt:
        {prompt}

        Output format (exact keys):
        {{
            "name": "<allowed function name>",
            "parameters": {{}}
        }}
        """
        actual_context = self.model.encode(full_prompt)
        context_ids = actual_context[0].tolist()
        generated_tokens = []

        for _ in range(max_tokens):
            logits = self.model.get_logits_from_input_ids(context_ids)
            next_token_id = max(range(len(logits)), key=lambda i: logits[i])
            generated_tokens.append(next_token_id)
            context_ids.append(next_token_id)
        out_text = self.model.decode(generated_tokens)
        print(out_text, flush=True)
        return {"name": "raw_text", "parameters":{"text": out_text}}
    
    def clean_output(self, out_text: str) -> int:
        count = 0
        for c in out_text:
            if c in "{"
                count += 1
            elif c in "}"
                count -= 1
        if count == 0:
            return out_text[:1]


