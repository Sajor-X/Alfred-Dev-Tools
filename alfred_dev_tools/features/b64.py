import base64

from alfred_dev_tools.alfred import copy_item, item, items_response, preview_text


def usage_response():
    return items_response(
        item(
            "Base64 编解码",
            "输入: b64 hello | 默认同时显示编码和解码结果",
            valid=False,
        )
    )

def _encode(text):
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def _decode(text):
    raw = base64.b64decode(text.encode("utf-8"), validate=True)
    return raw.decode("utf-8")


def build_results(text):
    text = text.strip()
    if not text:
        return usage_response()

    preview = preview_text(text)
    items = [
        copy_item(
            _encode(text),
            f"Base64 编码结果 | {preview}",
            uid="b64-encode",
        )
    ]

    try:
        decoded = _decode(text)
        items.append(
            copy_item(
                decoded,
                f"Base64 解码结果 | {preview}",
                uid="b64-decode",
            )
        )
    except Exception:
        items.append(
            item(
                "Base64 解码失败",
                "当前输入不是合法的 Base64 文本",
                valid=False,
                uid="b64-decode-error",
            )
        )

    return items_response(*items)
