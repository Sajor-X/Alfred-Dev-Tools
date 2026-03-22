import uuid

from alfred_password_workflow.alfred import copy_item, item, items_response


DEFAULT_COUNT = 1
MAX_COUNT = 10
VERSION_ALIASES = {
    "1": "v1",
    "4": "v4",
    "v1": "v1",
    "v4": "v4",
    "all": "all",
}


def usage_response():
    return items_response(
        item(
            "UUID 生成器",
            "输入: uuid | uuid 1 | uuid 4 count=5 | uuid all",
            valid=False,
        )
    )


def error_response(message):
    return items_response(item(message, "请检查版本与数量参数", valid=False))


def parse_query(query):
    version = "v4"
    count = DEFAULT_COUNT

    for token in query.lower().split():
        if token in VERSION_ALIASES:
            version = VERSION_ALIASES[token]
        elif token.startswith("count=") and token[6:].isdigit():
            count = int(token[6:])
        elif token.isdigit():
            count = int(token)
        else:
            return None, f"无法识别参数: {token}"

    if count < 1 or count > MAX_COUNT:
        return None, f"count 必须在 1 到 {MAX_COUNT} 之间"

    return (version, count), None


def _make_uuid(version):
    if version == "v1":
        return str(uuid.uuid1())
    return str(uuid.uuid4())


def build_results(version, count):
    versions = ("v1", "v4") if version == "all" else (version,)
    items = []

    for current_version in versions:
        for index in range(count):
            value = _make_uuid(current_version)
            items.append(
                copy_item(
                    value,
                    f"UUID {current_version.upper()} #{index + 1} | 回车复制",
                    uid=f"uuid-{current_version}-{index}",
                )
            )

    return items_response(*items)
