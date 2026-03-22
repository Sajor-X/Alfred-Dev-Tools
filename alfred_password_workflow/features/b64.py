import base64

from alfred_password_workflow.alfred import copy_item, item, items_response, preview_text


ENCODE_WORDS = {"e", "enc", "encode"}
DECODE_WORDS = {"d", "dec", "decode"}


def usage_response():
    return items_response(
        item(
            "Base64 编解码",
            "输入: b64 hello | b64 encode hello | b64 decode aGVsbG8=",
            valid=False,
        )
    )


def error_response(message):
    return items_response(item(message, "请检查输入内容", valid=False))


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


def _encode(text):
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def _decode(text):
    raw = base64.b64decode(text.encode("utf-8"), validate=True)
    return raw.decode("utf-8")


def build_result(mode, text):
    if not text:
        return usage_response()

    try:
        if mode == "decode":
            output = _decode(text)
            return items_response(
                copy_item(
                    output,
                    f"Base64 解码结果 | {preview_text(text)}",
                    uid="b64-decode",
                )
            )
        else:
            output = _encode(text)
            return items_response(
                copy_item(
                    output,
                    f"Base64 编码结果 | {preview_text(text)}",
                    uid="b64-encode",
                )
            )
    except Exception:
        return error_response("Base64 解码失败，输入可能不是合法 Base64")
