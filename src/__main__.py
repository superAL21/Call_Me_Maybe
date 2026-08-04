import argparse
import json
from .utils.io_utils import load_json, save_json
from typing import Any
from llm_sdk.llm_sdk import Small_LLM_Model
from .llm_wrapper import Wrapper_LLM


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=str,
        default="data/input/function_calling_tests.json",
        help="Path to input prompts file",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="data/output/function_calling_results.json",
        help="Path to output results file",
    )

    parser.add_argument(
        "--functions_definition",
        type=str,
        default="data/input/functions_definition.json",
        help="Path to functions schema file"
    )
    return parser


def process_prompts(
    input_data: Any,
    functions_def: Any,
    model: Wrapper_LLM) -> list[dict[str, Any]]:
    if not isinstance(input_data, list):
        raise TypeError("input data must be a list")
    if not isinstance(functions_def, list):
        raise TypeError("functions_def must be a list")

    results: list[dict[str, Any]] = []
    for item in input_data[:1]:
        prompt = item["prompt"]
        response = model.generate(prompt, functions_def, max_tokens=30)
        try:
            results.append({
                "prompt": item["prompt"],
                "name": response["name"],
                "parameters": response["parameters"],
            })
        except Exception:
            results.append({
                "prompt": prompt,
                "name": "error",
                "parameters": {}
            })
    return results


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        input_data = load_json(args.input)
        functions_def = load_json(args.functions_definition)
        model = Small_LLM_Model()
        wrapper = Wrapper_LLM(model)
        result = process_prompts(input_data, functions_def, wrapper)

        save_json(args.output, result)
        print(result[:1], flush=True)
    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {e.doc}: line {e.lineno}, column {e.colno}")
    except OSError as e:
        print(f"I/O error: {e}")


if __name__ == "__main__":
    main()
