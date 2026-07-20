import re

from alfred_dev_tools.alfred import copy_item, item, items_response, preview_text


def usage_response():
    return items_response(
        item(
            "求和计算器",
            "输入: sum 1 2 3 | sum 1+2+3 | sum 1,2,3 | sum 15 % 4 | sum 1 2 3 4 5 % 7",
            valid=False,
        )
    )


def _format_number(value):
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    if isinstance(value, int):
        return str(value)
    formatted = f"{value:.10f}".rstrip("0").rstrip(".")
    return formatted or "0"


def _parse_numbers(raw):
    if not raw or not raw.strip():
        return [], []

    normalized = raw.replace(",", " ").replace("，", " ")
    normalized = re.sub(r"(?<=[\d\.\)])\s*\+\s*", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    if not normalized:
        return [], []

    tokens = normalized.split(" ")
    numbers = []
    invalid = []
    for token in tokens:
        try:
            if any(ch in token for ch in (".", "e", "E")):
                numbers.append(float(token))
            else:
                numbers.append(int(token))
        except ValueError:
            invalid.append(token)
    return numbers, invalid


def _split_modulus(text):
    if "%" not in text:
        return text, None, None

    left, _, right = text.partition("%")
    right = right.strip()
    if not right:
        return left, None, "缺少取模的除数，例如 sum 15 % 4"

    try:
        if any(ch in right for ch in (".", "e", "E")):
            modulus = float(right)
        else:
            modulus = int(right)
    except ValueError:
        return left, None, f"无法识别的除数: {right}"

    if modulus == 0:
        return left, None, "除数不能为 0"

    return left, modulus, None


def build_results(text):
    if not text or not text.strip():
        return usage_response()

    expression, modulus, mod_error = _split_modulus(text)
    numbers, invalid = _parse_numbers(expression)

    preview = preview_text(text, limit=56)

    if not numbers and not invalid and mod_error is None:
        return usage_response()

    if not numbers:
        hint = "无法识别到任何数字"
        if invalid:
            hint = f"无法识别: {', '.join(invalid)}"
        return items_response(
            item(
                "求和计算器",
                f"{hint} | {preview}",
                valid=False,
                uid="sum-error",
            )
        )

    total = sum(numbers)
    total_str = _format_number(total)
    count = len(numbers)
    average = total / count
    average_str = _format_number(average)
    minimum_str = _format_number(min(numbers))
    maximum_str = _format_number(max(numbers))

    summary_subtitle = f"求和 | count={count} avg={average_str} min={minimum_str} max={maximum_str}"
    if invalid:
        summary_subtitle += f" | 已忽略: {', '.join(invalid)}"

    results = [
        copy_item(
            total_str,
            f"{summary_subtitle} | {preview}",
            uid="sum-total",
        )
    ]

    if mod_error is not None:
        results.append(
            item(
                "取模失败",
                f"{mod_error} | sum={total_str}",
                valid=False,
                uid="sum-mod-error",
            )
        )
    elif modulus is not None:
        modulus_str = _format_number(modulus)
        if isinstance(total, float) or isinstance(modulus, float):
            mod_value = total - modulus * (total // modulus)
        else:
            mod_value = total % modulus
        mod_str = _format_number(mod_value)
        results.append(
            copy_item(
                mod_str,
                f"取模 | {total_str} % {modulus_str} = {mod_str}",
                uid="sum-mod",
            )
        )

    results.append(
        copy_item(
            average_str,
            f"平均值 | sum={total_str} / count={count}",
            uid="sum-average",
        )
    )

    return items_response(*results)
