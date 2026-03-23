from dataclasses import dataclass
from datetime import datetime, timedelta

from alfred_dev_tools.alfred import copy_item, item, items_response


MONTH_ALIASES = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12,
}

WEEKDAY_ALIASES = {
    "SUN": 0,
    "MON": 1,
    "TUE": 2,
    "WED": 3,
    "THU": 4,
    "FRI": 5,
    "SAT": 6,
}

UNSUPPORTED_SPECIALS = {"L", "W", "#", "C"}
MAX_SEARCH_DAYS = 3660
DEFAULT_OCCURRENCE_COUNT = 5


@dataclass
class FieldSpec:
    values: list[int]
    wildcard: bool
    question: bool = False


@dataclass
class CronSpec:
    kind: str
    seconds: FieldSpec
    minutes: FieldSpec
    hours: FieldSpec
    day_of_month: FieldSpec
    month: FieldSpec
    day_of_week: FieldSpec
    year: FieldSpec


def usage_response():
    return items_response(
        item(
            "Cron 执行时间查看",
            "输入 Linux crontab 或 Java cron，默认展示从当前时间起最近 5 次执行",
            valid=False,
        )
    )


def error_response(message):
    return items_response(item(message, "示例: cron */15 * * * * | cron 0 0/15 * * * ?", valid=False))


def _python_weekday_to_cron(dt):
    return (dt.weekday() + 1) % 7


def _normalize_linux_weekday(value):
    if value == 7:
        return 0
    return value


def _normalize_java_weekday(value):
    if value in {0, 7}:
        return 0
    if 1 <= value <= 7:
        return value - 1
    return value


def _parse_token(token, aliases, normalizer):
    token = token.upper()
    if token in aliases:
        return aliases[token]
    value = int(token)
    if normalizer is not None:
        value = normalizer(value)
    return value


def _parse_field(expr, min_value, max_value, *, aliases=None, normalizer=None, allow_question=False):
    expr = expr.strip().upper()
    aliases = aliases or {}

    if any(symbol in expr for symbol in UNSUPPORTED_SPECIALS):
        unsupported = ", ".join(sorted(symbol for symbol in UNSUPPORTED_SPECIALS if symbol in expr))
        raise ValueError(f"暂不支持 cron 特殊语法: {unsupported}")

    if expr == "?":
        if not allow_question:
            raise ValueError("当前字段不支持 ? 语法")
        return FieldSpec(list(range(min_value, max_value + 1)), wildcard=True, question=True)

    if expr == "*":
        return FieldSpec(list(range(min_value, max_value + 1)), wildcard=True, question=False)

    values = set()
    for part in expr.split(","):
        if not part:
            raise ValueError("cron 字段中存在空的分段")

        if "/" in part:
            base, step_text = part.split("/", 1)
            if not step_text.isdigit() or int(step_text) <= 0:
                raise ValueError(f"无效的步长: {part}")
            step = int(step_text)
        else:
            base = part
            step = None

        if base in {"*", "?"}:
            start = min_value
            end = max_value
        elif "-" in base:
            start_text, end_text = base.split("-", 1)
            start = _parse_token(start_text, aliases, normalizer)
            end = _parse_token(end_text, aliases, normalizer)
        else:
            start = _parse_token(base, aliases, normalizer)
            end = max_value if step is not None else start

        if start > end:
            raise ValueError(f"无效范围: {part}")

        if start < min_value or end > max_value:
            raise ValueError(f"字段超出允许范围: {part}")

        if step is None:
            values.update(range(start, end + 1))
        else:
            values.update(range(start, end + 1, step))

    if not values:
        raise ValueError(f"字段没有可用值: {expr}")

    return FieldSpec(sorted(values), wildcard=False, question=False)


def parse_expression(query):
    query = query.strip()
    if not query:
        raise ValueError("empty")

    parts = query.split()
    if len(parts) == 5:
        kind = "linux"
        second_expr = "0"
        minute_expr, hour_expr, dom_expr, month_expr, dow_expr = parts
        year_expr = "*"
        dow_normalizer = _normalize_linux_weekday
    elif len(parts) in {6, 7}:
        kind = "java"
        second_expr, minute_expr, hour_expr, dom_expr, month_expr, dow_expr = parts[:6]
        year_expr = parts[6] if len(parts) == 7 else "*"
        dow_normalizer = _normalize_java_weekday
    else:
        raise ValueError("cron 表达式必须是 5 段（Linux）或 6/7 段（Java）")

    return CronSpec(
        kind=kind,
        seconds=_parse_field(second_expr, 0, 59),
        minutes=_parse_field(minute_expr, 0, 59),
        hours=_parse_field(hour_expr, 0, 23),
        day_of_month=_parse_field(dom_expr, 1, 31, allow_question=(kind == "java")),
        month=_parse_field(month_expr, 1, 12, aliases=MONTH_ALIASES),
        day_of_week=_parse_field(
            dow_expr,
            0 if kind == "linux" else 0,
            6,
            aliases=WEEKDAY_ALIASES,
            normalizer=dow_normalizer,
            allow_question=(kind == "java"),
        ),
        year=_parse_field(year_expr, 1970, 2099),
    )


def _matches_day(spec, dt):
    dom_match = dt.day in spec.day_of_month.values
    dow_match = _python_weekday_to_cron(dt) in spec.day_of_week.values

    if spec.kind == "linux":
        if spec.day_of_month.wildcard and spec.day_of_week.wildcard:
            return True
        if spec.day_of_month.wildcard:
            return dow_match
        if spec.day_of_week.wildcard:
            return dom_match
        return dom_match or dow_match

    if spec.day_of_month.question and spec.day_of_week.question:
        return True
    if spec.day_of_month.question:
        return dow_match
    if spec.day_of_week.question:
        return dom_match
    return dom_match and dow_match


def next_occurrences(spec, now, count=DEFAULT_OCCURRENCE_COUNT):
    results = []
    tzinfo = now.tzinfo
    start_date = now.date()

    for day_offset in range(MAX_SEARCH_DAYS):
        current_date = start_date + timedelta(days=day_offset)

        if current_date.year not in spec.year.values:
            continue
        if current_date.month not in spec.month.values:
            continue

        candidate_day = datetime(
            current_date.year,
            current_date.month,
            current_date.day,
            tzinfo=tzinfo,
        )
        if not _matches_day(spec, candidate_day):
            continue

        for hour in spec.hours.values:
            for minute in spec.minutes.values:
                for second in spec.seconds.values:
                    candidate = datetime(
                        current_date.year,
                        current_date.month,
                        current_date.day,
                        hour,
                        minute,
                        second,
                        tzinfo=tzinfo,
                    )
                    if candidate <= now:
                        continue
                    results.append(candidate)
                    if len(results) == count:
                        return results

    raise ValueError("在可搜索范围内没有找到未来执行时间")


def build_results(query):
    if not query.strip():
        return usage_response()

    try:
        spec = parse_expression(query)
    except ValueError as exc:
        if str(exc) == "empty":
            return usage_response()
        return error_response(str(exc))

    now = datetime.now().astimezone()
    try:
        occurrences = next_occurrences(spec, now)
    except ValueError as exc:
        return error_response(str(exc))

    kind_label = "Linux crontab" if spec.kind == "linux" else "Java cron"
    items = [
        item(
            kind_label,
            f"按当前时间起向后计算最近 {DEFAULT_OCCURRENCE_COUNT} 次执行",
            valid=False,
            uid=f"cron-{spec.kind}-header",
        )
    ]

    for index, occurrence in enumerate(occurrences, start=1):
        display = occurrence.strftime("%Y-%m-%d %H:%M:%S %a %Z")
        items.append(
            copy_item(
                display,
                f"{kind_label} | 第 {index} 次执行 | 回车复制",
                uid=f"cron-{spec.kind}-{index}",
            )
        )

    return items_response(*items)
