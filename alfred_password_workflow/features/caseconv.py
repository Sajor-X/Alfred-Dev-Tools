import re

from alfred_password_workflow.alfred import copy_item, item, items_response, preview_text


def usage_response():
    return items_response(
        item(
            "命名风格转换",
            "输入: case hello world | case hello_world | case helloWorld",
            valid=False,
        )
    )


def _split_words(text):
    normalized = text.strip()
    if not normalized:
        return []

    normalized = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", normalized)
    normalized = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", normalized)
    normalized = re.sub(r"[^A-Za-z0-9]+", " ", normalized)
    return [word.lower() for word in normalized.split() if word]


def build_results(text):
    words = _split_words(text)
    if not words:
        return usage_response()

    snake = "_".join(words)
    kebab = "-".join(words)
    camel = words[0] + "".join(word.capitalize() for word in words[1:])
    pascal = "".join(word.capitalize() for word in words)
    constant = "_".join(word.upper() for word in words)
    dot_case = ".".join(words)
    preview = preview_text(text, limit=48)

    return items_response(
        copy_item(snake, f"snake_case | {preview}", uid="case-snake"),
        copy_item(kebab, f"kebab-case | {preview}", uid="case-kebab"),
        copy_item(camel, f"camelCase | {preview}", uid="case-camel"),
        copy_item(pascal, f"PascalCase | {preview}", uid="case-pascal"),
        copy_item(constant, f"CONSTANT_CASE | {preview}", uid="case-constant"),
        copy_item(dot_case, f"dot.case | {preview}", uid="case-dot"),
    )
