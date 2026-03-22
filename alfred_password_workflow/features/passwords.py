import secrets
import string

from alfred_password_workflow.alfred import item, items_response


DEFAULT_LENGTH = 16
DEFAULT_COUNT = 6
MAX_COUNT = 12
SPECIAL_WORDS = {"special", "s"}
NO_SPECIAL_WORDS = {"nospecial", "ns", "n"}
SPECIALS = "!@#$%^&*()-_=+[]{};:,.?/|~"


def usage_response():
    return items_response(
        item(
            "随机密码生成器",
            "输入: pwd 16 | pwd 32 nospecial | pwd 24 special count=8",
            valid=False,
        )
    )


def error_response(message):
    return items_response(
        item(
            message,
            "示例: pwd 16 | pwd 32 nospecial | pwd 24 special count=8",
            valid=False,
        )
    )


def parse_query(query):
    length = DEFAULT_LENGTH
    count = DEFAULT_COUNT
    include_special = True

    for token in query.lower().split():
        if token.isdigit():
            length = int(token)
        elif token in SPECIAL_WORDS:
            include_special = True
        elif token in NO_SPECIAL_WORDS:
            include_special = False
        elif token.startswith("count=") and token[6:].isdigit():
            count = int(token[6:])
        else:
            return None, f"无法识别参数: {token}"

    if length < 4:
        return None, "长度不能小于 4"
    if count < 1 or count > MAX_COUNT:
        return None, f"count 必须在 1 到 {MAX_COUNT} 之间"

    return (length, count, include_special), None


def shuffle(chars):
    chars = list(chars)
    for index in range(len(chars) - 1, 0, -1):
        random_index = secrets.randbelow(index + 1)
        chars[index], chars[random_index] = chars[random_index], chars[index]
    return "".join(chars)


def make_password(length, include_special):
    groups = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    if include_special:
        groups.append(SPECIALS)

    chars = [secrets.choice(group) for group in groups]
    alphabet = "".join(groups)

    while len(chars) < length:
        chars.append(secrets.choice(alphabet))

    return shuffle(chars)


def build_results(length, count, include_special):
    items = []
    seen = set()
    mode_text = "包含特殊字符" if include_special else "仅字母数字"

    while len(items) < count:
        password = make_password(length, include_special)
        if password in seen:
            continue
        seen.add(password)
        items.append(
            item(
                password,
                f"{length} 位 | {mode_text} | 回车后复制到剪贴板",
                valid=True,
                uid=f"pwd-{length}-{len(items)}",
                arg=password,
                text={"copy": password, "largetype": password},
            )
        )

    return items_response(*items)
