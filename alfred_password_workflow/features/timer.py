import re


DEFAULT_MINUTES = 5
DEFAULT_MESSAGE = "时间到了"


def usage_response():
    return {
        "items": [
            {
                "title": "已设置 settimer",
                "subtitle": "示例: settimer 10 喝水 | settimer 10s 站起来 | settimer 1h 开会",
                "valid": False,
            }
        ]
    }


def parse_duration(token):
    match = re.fullmatch(r"(?i)(\d+)(s|m|h)?", token)
    if not match:
        return None

    value = int(match.group(1))
    unit = (match.group(2) or "m").lower()

    if unit == "s":
        return value
    if unit == "m":
        return value * 60
    if unit == "h":
        return value * 3600
    return None


def parse_query(query):
    tokens = query.split()
    if not tokens:
        return DEFAULT_MINUTES * 60, DEFAULT_MESSAGE

    seconds = parse_duration(tokens[0])
    if seconds is None:
        seconds = DEFAULT_MINUTES * 60
        message = query.strip()
    else:
        message = " ".join(tokens[1:]).strip() or DEFAULT_MESSAGE

    if seconds <= 0:
        raise ValueError("时间必须大于 0")

    return seconds, message


def format_duration(seconds):
    if seconds % 3600 == 0:
        return f"{seconds // 3600} 小时"
    if seconds % 60 == 0:
        return f"{seconds // 60} 分钟"
    return f"{seconds} 秒"
