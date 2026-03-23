import os

from alfred_dev_tools.alfred import item, items_response


DEFAULT_PREFIX = ""
TOOLS = [
    ("pwg", "随机密码生成", "10 -_+"),
    ("md5", "计算 MD5 哈希", "hello world"),
    ("sha", "计算 SHA 哈希", "sha512 hello world"),
    ("b64", "Base64 编码 / 解码，默认同时显示两种结果", "hello"),
    ("json", "JSON 格式化 / 压缩", '{"a":1}'),
    ("url", "URL 编码 / 解码，默认同时显示两种结果", "hello world"),
    ("uuid", "UUID 生成，默认直接返回 all", ""),
    ("cron", "Cron 表达式查看，支持 Linux crontab 与 Java cron", "*/15 * * * *"),
    ("ts", "时间戳与日期互转", "1710505200"),
    ("tc", "文本统计", "hello world"),
    ("case", "命名风格转换", "hello_world"),
    ("html", "HTML 实体转义 / 反转义，默认同时显示两种结果", "&lt;div&gt;"),
    ("jwt", "JWT 解码", "eyJ..."),
    ("timer", "倒计时提醒", "10m 喝水"),
]


def build_results(query):
    prefix = os.getenv("keyword_prefix", DEFAULT_PREFIX).strip() or DEFAULT_PREFIX
    needle = query.strip().lower()
    root_title = f"{prefix}help" if prefix else "help"
    items = [
        item(
            root_title,
            "查看全部工具关键词说明 | 可继续输入空格后筛选",
            valid=False,
            uid="catalog-root",
        )
    ]

    for suffix, description, sample_args in TOOLS:
        full_keyword = f"{prefix}{suffix}"
        example = f"示例: {full_keyword} {sample_args}".strip()
        haystack = f"{suffix} {description} {sample_args}".lower()
        if needle and needle not in haystack:
            continue
        items.append(
            item(
                full_keyword,
                f"{description} | {example}",
                valid=False,
                uid=f"catalog-{suffix}",
                autocomplete=f"{full_keyword} ",
            )
        )

    return items_response(*items)
