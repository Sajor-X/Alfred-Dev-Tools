import re
import subprocess

from alfred_dev_tools.alfred import copy_item, item, items_response, preview_text


DELIMITERS = "/|#~,@"

FLAG_MAP = {
    "i": re.IGNORECASE,
    "m": re.MULTILINE,
    "s": re.DOTALL,
    "x": re.VERBOSE,
    "a": re.ASCII,
}


def usage_response(hint=None):
    subtitle = (
        "输入: sub /old/new/[flags] 使用剪贴板内容做正则替换 | "
        "示例: sub /\\d+/N/ | sub |http://|https://| | sub /(\\w+)/[\\1]/i"
    )
    if hint:
        subtitle = f"{hint} | {subtitle}"
    return items_response(
        item(
            "剪贴板正则替换",
            subtitle,
            valid=False,
        )
    )


def _split_by_delim(text, delim):
    parts = []
    current = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "\\" and i + 1 < len(text) and text[i + 1] == delim:
            current.append(delim)
            i += 2
            continue
        if ch == delim:
            parts.append("".join(current))
            current = []
            i += 1
            continue
        current.append(ch)
        i += 1
    parts.append("".join(current))
    return parts


def _parse_command(text):
    stripped = text.strip()
    if not stripped:
        return None

    first = stripped[0]
    if first in DELIMITERS:
        parts = _split_by_delim(stripped[1:], first)
        if len(parts) < 2:
            return None
        pattern = parts[0]
        replacement = parts[1]
        flags_str = parts[2] if len(parts) >= 3 else ""
        return pattern, replacement, flags_str

    if " " in stripped:
        pattern, replacement = stripped.split(" ", 1)
        return pattern, replacement, ""

    return None


def _compile_flags(flags_str):
    flags = 0
    unknown = []
    for ch in flags_str:
        if ch == "g":
            continue
        mapped = FLAG_MAP.get(ch.lower())
        if mapped is None:
            unknown.append(ch)
            continue
        flags |= mapped
    return flags, unknown


def _read_clipboard():
    try:
        result = subprocess.run(
            ["pbpaste"],
            capture_output=True,
            text=True,
            timeout=2,
        )
    except FileNotFoundError:
        return None, "系统中未找到 pbpaste 命令"
    except subprocess.TimeoutExpired:
        return None, "读取剪贴板超时"
    except Exception as exc:  # noqa: BLE001
        return None, f"读取剪贴板异常: {exc}"
    if result.returncode != 0:
        return None, "pbpaste 执行失败"
    return result.stdout, None


def build_results(text, *, clipboard_reader=_read_clipboard):
    if not text or not text.strip():
        return usage_response()

    parsed = _parse_command(text)
    if parsed is None:
        return usage_response("未识别为 /pattern/replacement/ 或 pattern replacement 格式")

    pattern, replacement, flags_str = parsed
    if pattern == "":
        return usage_response("pattern 不能为空")

    flags, unknown_flags = _compile_flags(flags_str)
    if unknown_flags:
        return items_response(
            item(
                "剪贴板正则替换",
                f"未知 flag: {''.join(unknown_flags)} | 支持 i(忽略大小写) m(多行) s(dotall) x(verbose) g(全局，默认)",
                valid=False,
                uid="sub-flag-error",
            )
        )

    try:
        regex = re.compile(pattern, flags)
    except re.error as exc:
        return items_response(
            item(
                "正则表达式错误",
                f"{exc} | pattern={preview_text(pattern, 40)}",
                valid=False,
                uid="sub-regex-error",
            )
        )

    source, err = clipboard_reader()
    if err is not None:
        return items_response(
            item(
                "读取剪贴板失败",
                err,
                valid=False,
                uid="sub-clipboard-error",
            )
        )

    if not source:
        return items_response(
            item(
                "剪贴板为空",
                f"先复制一段文本再执行 | {preview_text(pattern, 24)} → {preview_text(replacement, 24) or '(空)'}",
                valid=False,
                uid="sub-clipboard-empty",
            )
        )

    try:
        result_text, count = regex.subn(replacement, source)
    except re.error as exc:
        return items_response(
            item(
                "替换失败",
                f"{exc} | 检查反向引用（如 \\1）是否与 pattern 匹配",
                valid=False,
                uid="sub-sub-error",
            )
        )

    result_preview = preview_text(result_text, 56) or "(空)"
    source_preview = preview_text(source, 56) or "(空)"
    pattern_preview = preview_text(pattern, 24)
    replacement_preview = preview_text(replacement, 24) or "(空字符串)"

    flag_hint = f" flags={flags_str}" if flags_str else ""
    summary_subtitle = (
        f"匹配 {count} 处 | pattern={pattern_preview} → {replacement_preview}"
        f"{flag_hint} | 回车复制完整结果"
    )

    items = [
        copy_item(
            result_preview,
            summary_subtitle,
            uid="sub-result",
            value=result_text,
        ),
    ]

    if count == 0:
        items.append(
            item(
                "未匹配到任何内容",
                f"pattern={pattern_preview} | 剪贴板保持原样",
                valid=False,
                uid="sub-no-match",
            )
        )

    items.append(
        copy_item(
            source_preview,
            f"原剪贴板内容 | {len(source)} chars | 回车复制原文",
            uid="sub-source",
            value=source,
        )
    )

    return items_response(*items)
