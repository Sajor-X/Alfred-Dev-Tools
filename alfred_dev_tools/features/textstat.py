import re

from alfred_dev_tools.alfred import copy_item, item, items_response, preview_text


def usage_response():
    return items_response(
        item(
            "文本统计工具",
            "输入: tc hello world",
            valid=False,
        )
    )


def _cjk_count(text):
    return sum(1 for char in text if "\u4e00" <= char <= "\u9fff")


def build_results(text):
    if not text:
        return usage_response()

    chars = len(text)
    chars_without_spaces = len(re.sub(r"\s+", "", text))
    words = len(re.findall(r"\S+", text))
    lines = text.count("\n") + 1
    bytes_utf8 = len(text.encode("utf-8"))
    cjk_chars = _cjk_count(text)
    preview = preview_text(text, limit=56)
    summary = (
        f"chars={chars} | no-space={chars_without_spaces} | "
        f"words={words} | lines={lines} | bytes={bytes_utf8}"
    )

    return items_response(
        copy_item(
            summary,
            f"统计汇总 | {preview}",
            uid="textstat-summary",
        ),
        copy_item(str(chars), "字符数 | 回车复制", uid="textstat-chars"),
        copy_item(
            str(chars_without_spaces),
            "非空白字符数 | 回车复制",
            uid="textstat-chars-no-space",
        ),
        copy_item(str(words), "单词数 | 回车复制", uid="textstat-words"),
        copy_item(str(lines), "行数 | 回车复制", uid="textstat-lines"),
        copy_item(str(bytes_utf8), "UTF-8 字节数 | 回车复制", uid="textstat-bytes"),
        copy_item(str(cjk_chars), "中文字符数 | 回车复制", uid="textstat-cjk"),
    )
