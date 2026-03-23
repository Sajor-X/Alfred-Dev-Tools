from urllib.parse import quote, unquote

from alfred_dev_tools.alfred import copy_item, item, items_response, preview_text


def usage_response():
    return items_response(item("URL 编码解码工具", "输入: url hello world", valid=False))


def build_results(text):
    text = text.strip()
    if not text:
        return usage_response()

    preview = preview_text(text)
    encoded = quote(text, safe="")
    decoded = unquote(text)

    return items_response(
        copy_item(
            encoded,
            f"URL Encode 结果 | {preview}",
            uid="url-encode",
        ),
        copy_item(
            decoded,
            f"URL Decode 结果 | {preview}",
            uid="url-decode",
        ),
    )
