import inspect
from typing import Any, Dict
import re

def parse_description(docstring: str | None) -> str:
    """
    Parse a function's docstring to extract the description.

    Args:
        docstring (str): The docstring to parse.

    Returns:
        str: The description.
    """

    if not docstring:
        return ""

    lines = [line.strip() for line in docstring.strip().split("\n")]
    description_lines: list[str] = []

    for line in lines:
        if re.match(r":param", line) or re.match(r":return", line):
            break

        description_lines.append(line)

    return "\n".join(description_lines)


def parse_docstring(docstring):
    """
    Parse a function's docstring to extract parameter descriptions in reST format.

    Args:
        docstring (str): The docstring to parse.

    Returns:
        dict: A dictionary where keys are parameter names and values are descriptions.
    """
    if not docstring:
        return {}

    # Regex to match `:param name: description` format
    param_pattern = re.compile(r":param (\w+):\s*(.+)")
    param_descriptions = {}

    for line in docstring.splitlines():
        match = param_pattern.match(line.strip())
        if not match:
            continue
        param_name, param_description = match.groups()
        if param_name.startswith("__"):
            continue
        param_descriptions[param_name] = param_description

    return param_descriptions

def function_to_dict(func: callable) -> Dict[str, Any]:
    """Convertit une fonction en un dictionnaire au format OpenWebUI."""

    docstring = func.__doc__
    description = parse_description(docstring)
    param_descriptions = parse_docstring(docstring)
    signature = inspect.signature(func)
    parameters = signature.parameters

    spec = {
        "name": func.__name__,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }

    for name, param in parameters.items():
        if name == "__id__" or name == "__user__" or name == "request": # Paramètres spéciaux à ignorer
            continue

        param_type = type(param.default).__name__ if param.default is not param.empty else "string" # Type par défaut: string
        description = param_descriptions.get(name, "")

        spec["parameters"]["properties"][name] = {
            "type": param_type,
            "description": description
        }
        if param.default is param.empty: # Paramètre requis
            spec["parameters"]["required"].append(name)

    return {
        "callable": func,
        "spec": spec
    }