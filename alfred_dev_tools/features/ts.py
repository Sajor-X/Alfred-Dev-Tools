from datetime import datetime
import re

from alfred_dev_tools.alfred import item, items_response

_DATE_PATTERNS = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
    "%Y/%m/%d %H:%M:%S",
    "%Y/%m/%d %H:%M",
    "%Y/%m/%d",
    "%Y.%m.%d %H:%M:%S",
    "%Y.%m.%d %H:%M",
    "%Y.%m.%d",
]


def usage_response():
    return items_response(
        item(
            "时间戳工具",
            "输入: ts | ts 1710505200 | ts 2026-03-22 10:30:00",
            valid=False,
        )
    )


def _local_timezone():
    return datetime.now().astimezone().tzinfo


def _format_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _copy_item(title, subtitle, uid, value):
    value_text = str(value)
    return item(
        title,
        subtitle,
        valid=True,
        uid=uid,
        arg=value_text,
        text={"copy": value_text, "largetype": value_text},
    )


def _is_integer_text(text):
    return bool(re.fullmatch(r"[+-]?\d+", text))


def _parse_datetime_text(text):
    candidate = text.strip().replace("T", " ")
    timezone = _local_timezone()

    for pattern in _DATE_PATTERNS:
        try:
            parsed = datetime.strptime(candidate, pattern)
            return parsed.replace(tzinfo=timezone)
        except ValueError:
            continue

    return None


def _timestamp_to_datetime(raw_text):
    value = int(raw_text)
    digits = len(raw_text.lstrip("+-"))
    is_milliseconds = digits >= 13 or abs(value) >= 100_000_000_000
    seconds = value / 1000 if is_milliseconds else value
    dt = datetime.fromtimestamp(seconds, tz=_local_timezone())
    return dt, is_milliseconds


def build_now_response():
    now = datetime.now().astimezone()
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    ts_seconds = int(now.timestamp())
    ts_milliseconds = int(now.timestamp() * 1000)

    return items_response(
        _copy_item(
            _format_datetime(now),
            "当前时间 | 回车复制",
            "ts-now",
            _format_datetime(now),
        ),
        _copy_item(
            _format_datetime(day_start),
            "当日 0 点时间 | 回车复制",
            "ts-day-start",
            _format_datetime(day_start),
        ),
        _copy_item(
            str(ts_seconds),
            "当前时间戳（秒）| 回车复制",
            "ts-seconds",
            ts_seconds,
        ),
        _copy_item(
            str(ts_milliseconds),
            "当前时间戳（毫秒）| 回车复制",
            "ts-milliseconds",
            ts_milliseconds,
        ),
    )


def build_from_timestamp_response(raw_text):
    dt, is_milliseconds = _timestamp_to_datetime(raw_text)
    normalized_seconds = int(dt.timestamp())
    normalized_milliseconds = int(dt.timestamp() * 1000)
    unit_text = "毫秒" if is_milliseconds else "秒"

    return items_response(
        _copy_item(
            _format_datetime(dt),
            f"由时间戳（{unit_text}）转换得到日期时间 | 回车复制",
            "ts-from-timestamp-datetime",
            _format_datetime(dt),
        ),
        _copy_item(
            str(normalized_seconds),
            "标准时间戳（秒）| 回车复制",
            "ts-from-timestamp-seconds",
            normalized_seconds,
        ),
        _copy_item(
            str(normalized_milliseconds),
            "标准时间戳（毫秒）| 回车复制",
            "ts-from-timestamp-milliseconds",
            normalized_milliseconds,
        ),
    )


def build_from_datetime_response(raw_text):
    dt = _parse_datetime_text(raw_text)
    if dt is None:
        return usage_response()

    ts_seconds = int(dt.timestamp())
    ts_milliseconds = int(dt.timestamp() * 1000)

    return items_response(
        _copy_item(
            _format_datetime(dt),
            "解析后的日期时间 | 回车复制",
            "ts-from-datetime-datetime",
            _format_datetime(dt),
        ),
        _copy_item(
            str(ts_seconds),
            "对应时间戳（秒）| 回车复制",
            "ts-from-datetime-seconds",
            ts_seconds,
        ),
        _copy_item(
            str(ts_milliseconds),
            "对应时间戳（毫秒）| 回车复制",
            "ts-from-datetime-milliseconds",
            ts_milliseconds,
        ),
    )


def build_response(query):
    query = query.strip()
    if not query:
        return build_now_response()

    if _is_integer_text(query):
        try:
            return build_from_timestamp_response(query)
        except (OverflowError, OSError, ValueError):
            return usage_response()

    return build_from_datetime_response(query)
