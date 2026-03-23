import secrets
import string

from alfred_dev_tools.alfred import item, items_response


DEFAULT_LENGTH = 16
DEFAULT_COUNT = 6
MAX_COUNT = 12
SPECIAL_WORDS = {"special", "s"}
NO_SPECIAL_WORDS = {"nospecial", "ns", "n"}
DEFAULT_SPECIALS = "!@#$%^&*()-_=+[]{};:,.?/|~"


def usage_response():
    return items_response(
        item(
            "随机密码生成器",
            "输入: pwg 16 | pwg 10 -_+ | pwg 32 nospecial count=8",
            valid=False,
        )
    )


def error_response(message):
    return items_response(
        item(
            message,
            "示例: pwg 16 | pwg 10 -_+ | pwg 32 nospecial count=8",
            valid=False,
        )
    )


def parse_query(query):
    length = DEFAULT_LENGTH
    count = DEFAULT_COUNT
    special_chars = DEFAULT_SPECIALS
    custom_special_token = None

    for token in query.split():
        lowered = token.lower()
        if token.isdigit():
            length = int(token)
        elif lowered in SPECIAL_WORDS:
            special_chars = DEFAULT_SPECIALS
        elif lowered in NO_SPECIAL_WORDS:
            special_chars = ""
        elif lowered.startswith("count=") and lowered[6:].isdigit():
            count = int(token[6:])
        elif custom_special_token is None:
            custom_special_token = token
        else:
            return None, f"无法识别参数: {token}"

    if custom_special_token is not None:
        if any(char.isalnum() for char in custom_special_token):
            return None, "自定义特殊符号参数只能包含非字母数字字符"
        special_chars = "".join(dict.fromkeys(custom_special_token))

    if length < 4:
        return None, "长度不能小于 4"
    if count < 1 or count > MAX_COUNT:
        return None, f"count 必须在 1 到 {MAX_COUNT} 之间"

    return (length, count, special_chars), None


def shuffle(chars):
    chars = list(chars)
    for index in range(len(chars) - 1, 0, -1):
        random_index = secrets.randbelow(index + 1)
        chars[index], chars[random_index] = chars[random_index], chars[index]
    return "".join(chars)


def make_password(length, special_chars):
    groups = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    if special_chars:
        groups.append(special_chars)

    chars = [secrets.choice(group) for group in groups]
    alphabet = "".join(groups)

    while len(chars) < length:
        chars.append(secrets.choice(alphabet))

    return shuffle(chars)


def build_results(length, count, special_chars):
    items = []
    seen = set()
    if special_chars == DEFAULT_SPECIALS:
        mode_text = "默认特殊字符"
    elif special_chars:
        mode_text = f"特殊符号: {special_chars}"
    else:
        mode_text = "仅字母数字"

    while len(items) < count:
        password = make_password(length, special_chars)
        if password in seen:
            continue
        seen.add(password)
        items.append(
            item(
                password,
                f"{length} 位 | {mode_text} | 回车后复制到剪贴板",
                valid=True,
                uid=f"pwg-{length}-{len(items)}",
                arg=password,
                text={"copy": password, "largetype": password},
            )
        )

    return items_response(*items)
