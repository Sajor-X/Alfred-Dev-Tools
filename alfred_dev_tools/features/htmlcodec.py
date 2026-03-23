from html import escape, unescape

from alfred_dev_tools.alfred import copy_item, item, items_response, preview_text


def usage_response():
    return items_response(
        item(
            "HTML 转义工具",
            "输入: html <div> | 默认同时显示转义和反转义结果",
            valid=False,
        )
    )

def build_results(text):
    text = text.strip()
    if not text:
        return usage_response()

    preview = preview_text(text)
    return items_response(
        copy_item(
            escape(text, quote=True),
            f"HTML Encode 结果 | {preview}",
            uid="html-encode",
        ),
        copy_item(
            unescape(text),
            f"HTML Decode 结果 | {preview}",
            uid="html-decode",
        ),
    )
