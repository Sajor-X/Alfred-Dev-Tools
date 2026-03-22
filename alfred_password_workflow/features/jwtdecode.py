import base64
import json
from datetime import datetime

from alfred_password_workflow.alfred import copy_item, item, items_response, preview_text


def usage_response():
    return items_response(
        item(
            "JWT 解码工具",
            "输入: jwt <token>",
            valid=False,
        )
    )


def error_response(message):
    return items_response(item(message, "请输入合法的 JWT 字符串", valid=False))


def _decode_segment(segment):
    padded = segment + "=" * (-len(segment) % 4)
    raw = base64.urlsafe_b64decode(padded.encode("utf-8"))
    return raw.decode("utf-8")


def _format_unix_timestamp(value):
    try:
        dt = datetime.fromtimestamp(int(value)).astimezone()
    except (OverflowError, OSError, TypeError, ValueError):
        return None
    return dt.strftime("%Y-%m-%d %H:%M:%S %Z")


def _claims_summary(payload):
    lines = []

    for key in ("iss", "sub", "aud", "jti"):
        if key in payload:
            lines.append(f"{key}: {payload[key]}")

    for key in ("iat", "nbf", "exp"):
        if key in payload:
            formatted = _format_unix_timestamp(payload[key])
            if formatted is not None:
                lines.append(f"{key}: {payload[key]} ({formatted})")
            else:
                lines.append(f"{key}: {payload[key]}")

    return "\n".join(lines)


def build_results(token):
    token = token.strip()
    if not token:
        return usage_response()

    parts = token.split(".")
    if len(parts) not in {2, 3}:
        return error_response("JWT 必须包含 2 段或 3 段")

    try:
        header = json.loads(_decode_segment(parts[0]))
        payload = json.loads(_decode_segment(parts[1]))
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return error_response("JWT 解码失败，Header 或 Payload 不是合法 JSON")

    header_json = json.dumps(header, ensure_ascii=False, indent=2)
    payload_json = json.dumps(payload, ensure_ascii=False, indent=2)
    claims = _claims_summary(payload)
    payload_preview = preview_text(json.dumps(payload, ensure_ascii=False), limit=56)

    items = [
        copy_item(
            "JWT Payload (JSON)",
            f"{payload_preview} | 回车复制",
            uid="jwt-payload",
            value=payload_json,
        ),
        copy_item(
            "JWT Header (JSON)",
            "回车复制 Header JSON",
            uid="jwt-header",
            value=header_json,
        ),
    ]

    if claims:
        items.insert(
            1,
            copy_item(
                "JWT Claims Summary",
                "iat / nbf / exp 等关键信息 | 回车复制",
                uid="jwt-claims",
                value=claims,
            ),
        )

    if len(parts) == 3 and parts[2]:
        items.append(
            copy_item(
                parts[2],
                "JWT Signature 段 | 回车复制",
                uid="jwt-signature",
            )
        )

    items.append(copy_item(token, "原始 JWT | 回车复制", uid="jwt-raw"))
    return items_response(*items)
