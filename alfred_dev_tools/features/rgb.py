import hashlib
import os
from pathlib import Path
import re
import struct
import tempfile
import zlib

from alfred_dev_tools.alfred import copy_item, item, items_response


NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?%?"


def usage_response():
    return items_response(item(
        "RGB / RGBA 大色卡",
        "输入: rgb #CC73E1FF | rgb rgb(204,115,225) | rgb rgba(204,115,225,0.5)",
        valid=False,
    ))


def _component(token, *, alpha=False):
    if not re.fullmatch(NUMBER, token):
        raise ValueError("颜色分量必须是数字或百分比")
    percent = token.endswith("%")
    value = float(token[:-1] if percent else token)
    maximum = 100 if percent else (1 if alpha else 255)
    if not 0 <= value <= maximum:
        raise ValueError("RGB 范围为 0–255（或 0–100%），Alpha 为 0–1（或 0–100%）")
    if alpha:
        return value / 100 if percent else value
    return int((value * 255 / 100 if percent else value) + 0.5)


def parse_color(query):
    """Return (red, green, blue, alpha); hex alpha is the last component."""
    query = query.strip()
    hex_match = re.fullmatch(r"#?([0-9a-fA-F]{3,8})", query)
    if hex_match and len(hex_match[1]) in (3, 4, 6, 8):
        value = hex_match[1]
        if len(value) in (3, 4):
            value = "".join(c * 2 for c in value)
        channels = tuple(int(value[i:i + 2], 16) for i in range(0, 6, 2))
        return (*channels, int(value[6:], 16) / 255 if len(value) == 8 else 1.0)

    function = re.fullmatch(r"rgba?\s*\((.*)\)", query, re.IGNORECASE | re.DOTALL)
    body = function[1].strip() if function else query
    if "," in body:
        tokens = [part.strip() for part in body.split(",")]
    elif "/" in body:
        parts = body.split("/")
        if len(parts) != 2 or len(parts[0].split()) != 3:
            raise ValueError("使用三个 RGB 分量，斜杠后填写 Alpha")
        tokens = [*parts[0].split(), parts[1].strip()]
    else:
        tokens = body.split()
    if len(tokens) not in (3, 4):
        raise ValueError("支持 #RGB、#RGBA、#RRGGBB、#RRGGBBAA 或 RGB / RGBA 数值")
    channels = tuple(_component(token) for token in tokens[:3])
    return (*channels, _component(tokens[3], alpha=True) if len(tokens) == 4 else 1.0)


def _png_chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))


def swatch_png(color, width=1200, height=800):
    """Render the color over a checkerboard using only the standard library."""
    red, green, blue, alpha = color
    backgrounds = (255, 216)
    pixels = [bytes(int(channel * alpha + bg * (1 - alpha) + 0.5)
                    for channel in (red, green, blue)) for bg in backgrounds]
    rows = [b"\x00" + b"".join(pixels[(x // 32 + parity) % 2] for x in range(width))
            for parity in (0, 1)]
    data = b"".join(rows[(y // 32) % 2] for y in range(height))
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + _png_chunk(b"IHDR", header)
            + _png_chunk(b"IDAT", zlib.compress(data)) + _png_chunk(b"IEND", b""))


def swatch_path(color):
    cache = os.getenv("alfred_workflow_cache")
    root = Path(cache).expanduser() if cache else Path.home() / "Library/Caches/com.sajor.alfred.devtools"
    directory = root.resolve() / "rgb"
    directory.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(repr(color).encode("ascii")).hexdigest()[:20]
    path = directory / f"swatch-v1-{key}.png"
    if not path.is_file():
        # Publish atomically: Alfred must never read a partially written image.
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=directory, suffix=".png", delete=False) as handle:
                temporary = Path(handle.name)
                handle.write(swatch_png(color))
            temporary.replace(path)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()
    return str(path)


def build_results(query):
    if not query.strip() or query.strip().lower() in {"help", "?"}:
        return usage_response()
    try:
        color = parse_color(query)
    except ValueError as exc:
        return items_response(item("无法识别颜色", str(exc), valid=False))

    red, green, blue, alpha = color
    hex_rgb = f"#{red:02X}{green:02X}{blue:02X}"
    hex_rgba = f"{hex_rgb}{int(alpha * 255 + 0.5):02X}"
    alpha_text = f"{alpha:.6f}".rstrip("0").rstrip(".")
    rgb = f"rgb({red}, {green}, {blue})"
    rgba = f"rgba({red}, {green}, {blue}, {alpha_text})"
    opacity = f"不透明度 {alpha * 100:.2f}%"
    formats = [(hex_rgba, "HEX RGBA", "hex-rgba"), (rgba, "RGBA", "rgba"),
               (hex_rgb, "HEX RGB（不含透明度）", "hex"), (rgb, "RGB（不含透明度）", "rgb")]
    if alpha == 1:
        formats = [formats[2], formats[3], formats[0], formats[1]]
    try:
        preview = swatch_path(color)
    except OSError:
        preview = None

    results = []
    for value, label, uid in formats:
        hint = "Shift / ⌘Y 查看大色卡" if preview else "色卡生成失败，请检查缓存目录权限"
        result = copy_item(value, f"{label} | {opacity} | {hint} | 回车复制", uid=f"rgb-{uid}")
        if preview:
            result["icon"] = {"path": preview}
            result["quicklookurl"] = preview
        results.append(result)
    return items_response(*results)
