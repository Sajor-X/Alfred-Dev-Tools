from html import escape, unescape

from alfred_password_workflow.alfred import copy_item, item, items_response, preview_text


ENCODE_WORDS = {"e", "enc", "encode"}
DECODE_WORDS = {"d", "dec", "decode"}


def usage_response():
    return items_response(
        item(
            "HTML 转义工具",
            "输入: html <div> | html decode &lt;div&gt;",
            valid=False,
        )
    )


def parse_query(query):
    query = query.strip()
    if not query:
        return None, None

    parts = query.split(maxsplit=1)
    head = parts[0].lower()

    if head in ENCODE_WORDS:
        return "encode", parts[1] if len(parts) > 1 else ""
    if head in DECODE_WORDS:
        return "decode", parts[1] if len(parts) > 1 else ""
    return "encode", query


def build_result(mode, text):
    if not text:
        return usage_response()

    if mode == "decode":
        output = unescape(text)
        subtitle = f"HTML Decode 结果 | {preview_text(text)}"
        uid = "html-decode"
    else:
        output = escape(text, quote=True)
        subtitle = f"HTML Encode 结果 | {preview_text(text)}"
        uid = "html-encode"

    return items_response(copy_item(output, subtitle, uid=uid))
