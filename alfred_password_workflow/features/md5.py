import hashlib

from alfred_password_workflow.alfred import item, items_response


def usage_response():
    return items_response(
        item(
            "MD5 生成器",
            "输入: md5 hello | md5 123456 | md5 any text here",
            valid=False,
        )
    )


def build_result(text):
    digest = hashlib.md5(text.encode("utf-8")).hexdigest()
    return items_response(
        item(
            digest,
            f'MD5("{text}") | 回车后复制到剪贴板',
            valid=True,
            uid=f"md5-{digest}",
            arg=digest,
            text={"copy": digest, "largetype": digest},
        )
    )
