import os
import json
import argparse
from pydantic import ValidationError
from src.schemas import (
    FunctionsDefinition,
    FunctionCallingTests,
    FunctionCallingResults,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call memaybe - Function Calling System"
    )
    parser.add_argument(
        "--functions_definition",
        type=str,
        default="data/input/functions_definition.json",
        help="Path to the functions definition JSON file."
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/input/function_calling_tests.json",
        help="Path to the test prompts JSON file."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output/function_calling_results.json",
        help="Path to the output results JSON file."
    )
    return parser.parse_args()


def load_functions(file_path: str) -> list[FunctionsDefinition]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                print(f"Error: Expected a JSON list in {file_path}")
                return []

            functions = []
            for item in data:
                obj = FunctionsDefinition(**item)
                functions.append(obj)
            return functions

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON syntax in {file_path}")
        return []
    except ValidationError as error:
        print(f"Error: Data does not match Pydantic"
              f" schema in {file_path}: \n{error}")
        return []


def load_tests(file_path: str) -> list[FunctionCallingTests]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                print(f"Error: Expected a JSON list in {file_path}")
                return []
            tests = []
            for item in data:
                obj = FunctionCallingTests(**item)
                tests.append(obj)
            return tests
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON syntax in {file_path}")
        return []
    except ValidationError as error:
        print(f"Error: Data does not match Pydantic"
              f" schema in {file_path}: \n{error}")
        return []


def save_results(
    file_path: str,
    results: list[FunctionCallingResults]
) -> None:
    try:
        folder = os.path.dirname(file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        data_to_save = [item.model_dump() for item in results]

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=2, ensure_ascii=False)

        print(f"✅ Result successfully saved to {file_path}")
    except Exception as error:
        print(f"Error saving results to {file_path}: {error}")
