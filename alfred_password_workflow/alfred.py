import json


def print_json(payload):
    print(json.dumps(payload, ensure_ascii=False))


def item(title, subtitle, *, valid, uid=None, arg=None, text=None):
    result = {
        "title": title,
        "subtitle": subtitle,
        "valid": valid,
    }
    if uid is not None:
        result["uid"] = uid
    if arg is not None:
        result["arg"] = arg
    if text is not None:
        result["text"] = text
    return result


def items_response(*items):
    return {"items": list(items)}


def copy_item(title, subtitle, *, uid, value=None, valid=True):
    copy_value = title if value is None else value
    copy_text = str(copy_value)
    return item(
        str(title),
        subtitle,
        valid=valid,
        uid=uid,
        arg=copy_text,
        text={"copy": copy_text, "largetype": copy_text},
    )


def preview_text(text, limit=72):
    compact = " ".join(str(text).split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."
