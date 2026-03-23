import json

from alfred_dev_tools.alfred import copy_item, item, items_response


MINIFY_WORDS = {"min", "minify"}
PRETTY_WORDS = {"pretty", "fmt", "format"}


def usage_response():
    return items_response(
        item(
            "JSON 格式化工具",
            "输入: json {\"a\":1} | json min {\"a\":1}",
            valid=False,
        )
    )


def error_response(message):
    return items_response(item(message, "请检查 JSON 内容", valid=False))


def parse_query(query):
    query = query.strip()
    if not query:
        return None, None

    parts = query.split(maxsplit=1)
    head = parts[0].lower()

    if head in MINIFY_WORDS:
        return "minify", parts[1] if len(parts) > 1 else ""
    if head in PRETTY_WORDS:
        return "pretty", parts[1] if len(parts) > 1 else ""

    return "pretty", query


def build_result(mode, text):
    if not text:
        return usage_response()

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return error_response(f"JSON 无效: 第 {exc.lineno} 行第 {exc.colno} 列附近")

    pretty_output = json.dumps(data, ensure_ascii=False, indent=2)
    minify_output = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    pretty_item = copy_item(
        "Pretty JSON",
        "2 空格缩进格式化 | 回车复制",
        uid="json-pretty",
        value=pretty_output,
    )
    minify_item = copy_item(
        "Minified JSON",
        "压缩成单行 JSON | 回车复制",
        uid="json-minify",
        value=minify_output,
    )

    if mode == "minify":
        return items_response(minify_item, pretty_item)
    return items_response(pretty_item, minify_item)
