import hashlib

from alfred_dev_tools.alfred import copy_item, item, items_response, preview_text


DEFAULT_ALGORITHM = "all"
ALGORITHMS = ("sha1", "sha224", "sha256", "sha384", "sha512")
ALL_DISPLAY_ORDER = ("sha256", "sha512", "sha1", "sha224", "sha384")
ALGORITHM_ALIASES = {
    "1": "sha1",
    "224": "sha224",
    "256": "sha256",
    "384": "sha384",
    "512": "sha512",
    "sha1": "sha1",
    "sha224": "sha224",
    "sha256": "sha256",
    "sha384": "sha384",
    "sha512": "sha512",
}


def usage_response():
    return items_response(
        item(
            "SHA 哈希工具",
            "输入: sha hello | sha sha512 hello | sha all hello | 默认展示全部结果",
            valid=False,
        )
    )


def error_response(message):
    return items_response(item(message, "请检查输入参数", valid=False))


def parse_query(query):
    query = query.strip()
    if not query:
        return None, None, "empty"

    parts = query.split(maxsplit=1)
    head = parts[0].lower()
    algorithm = ALGORITHM_ALIASES.get(head, head)

    if algorithm in ALGORITHMS or algorithm == "all":
        text = parts[1] if len(parts) > 1 else ""
    else:
        algorithm = DEFAULT_ALGORITHM
        text = query

    if not text:
        return None, None, "empty"

    return algorithm, text, None


def build_results(algorithm, text):
    targets = ALL_DISPLAY_ORDER if algorithm == "all" else [algorithm]
    preview = preview_text(text, limit=48)
    items = []

    for name in targets:
        digest = getattr(hashlib, name)(text.encode("utf-8")).hexdigest()
        items.append(
            copy_item(
                digest,
                f'{name.upper()}("{preview}") | 回车复制',
                uid=f"sha-{name}-{digest[:10]}",
            )
        )

    return items_response(*items)
