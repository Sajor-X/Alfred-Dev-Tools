from urllib.parse import quote, unquote

from alfred_password_workflow.alfred import copy_item, item, items_response, preview_text


def usage_response(mode):
    if mode == "encode":
        return items_response(item("URL 编码工具", "输入: urlencode hello world", valid=False))
    return items_response(item("URL 解码工具", "输入: urldecode hello%20world", valid=False))


def build_encode_result(text):
    text = text.strip()
    if not text:
        return usage_response("encode")

    output = quote(text, safe="")
    return items_response(
        copy_item(
            output,
            f"URL Encode 结果 | {preview_text(text)}",
            uid="url-encode",
        )
    )


def build_decode_result(text):
    text = text.strip()
    if not text:
        return usage_response("decode")

    output = unquote(text)
    return items_response(
        copy_item(
            output,
            f"URL Decode 结果 | {preview_text(text)}",
            uid="url-decode",
        )
    )
