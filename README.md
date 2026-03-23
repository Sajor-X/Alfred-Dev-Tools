# Alfred-Dev-Tools

[![Version](https://img.shields.io/badge/version-v0.1.4-111827?style=flat-square)](https://github.com/Sajor-X/Alfred-Dev-Tools)
[![License](https://img.shields.io/badge/license-MIT-16a34a?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Alfred%20Workflow-0ea5e9?style=flat-square)](https://www.alfredapp.com/)
[![Language](https://img.shields.io/badge/python-3.x-f59e0b?style=flat-square)](https://www.python.org/)

一个给开发者用的 Alfred 工具箱。

它把平时最常用的一批开发小工具收进 Alfred，让你不用切浏览器找在线工具，不用临时写脚本，不用反复复制粘贴网页，直接在 Alfred 里输入命令就能完成哈希、编码解码、JSON 格式化、UUID 生成、Cron 预览、时间戳转换、文本统计、JWT 解码、倒计时提醒等操作。

## ✨ 适合谁用

- 想把常见开发小工具放进 Alfred 的开发者
- 习惯键盘流，想减少打开网页工具站次数的人
- 想持续扩展自己 Alfred Workflow 的维护者

## 🚀 快速开始

1. 导入打包好的 workflow：
   `Alfred-Dev-Tools-v0.1.4.alfredworkflow`
2. 打开 Alfred
3. 直接输入命令，例如：

```text
md5 hello world
sha hello
json {"a":1}
url hello%20world
timer 10m 喝水
```

默认不加统一前缀，开箱即用。

如果你想给全部命令加前缀，也支持在 workflow 配置里设置 `keyword_prefix`，比如改成 `dv` 之后，就会变成：

- `dvhelp`
- `dvpwg`
- `dvmd5`
- `dvsha`
- `dvjson`
- `dvurl`
- `dvtimer`

## 🧭 总览命令

输入：

```text
help
```

会直接展示全部工具、对应作用和示例。

如果你设置了前缀，例如 `dv`，则总览入口会变成：

```text
dvhelp
```

## 🧩 功能模块

### 🔐 哈希与密码

| 命令 | 作用 | 示例 |
| --- | --- | --- |
| `pwg` | 生成随机密码 | `pwg 10 -_+` |
| `md5` | 计算 MD5 | `md5 hello world` |
| `sha` | 计算 SHA 哈希 | `sha hello` / `sha all hello` |

### 🔁 编码与格式化

| 命令 | 作用 | 示例 |
| --- | --- | --- |
| `b64` | Base64 编码与解码 | `b64 hello` |
| `json` | JSON 格式化 / 压缩 | `json {"a":1}` |
| `url` | URL 编码 / 解码 | `url hello world` |
| `html` | HTML 实体转义 / 反转义 | `html &lt;div&gt;hello&lt;/div&gt;` |
| `jwt` | JWT 解码 | `jwt eyJ...` |

### 🕒 时间与调度

| 命令 | 作用 | 示例 |
| --- | --- | --- |
| `uuid` | UUID 生成 | `uuid` / `uuid all` |
| `cron` | 查看最近 5 次执行时间 | `cron */15 * * * *` |
| `ts` | 时间戳与日期互转 | `ts 1710505200` |
| `timer` | 倒计时提醒 | `timer 10m 喝水` |

### 📝 文本与命名

| 命令 | 作用 | 示例 |
| --- | --- | --- |
| `tc` | 文本字数统计 | `tc hello world` |
| `case` | 命名风格转换 | `case hello_world` |

## 📘 命令说明

下面这部分是标准用法说明。每个命令都给出“命令是什么、怎么输入、返回什么”。

### `pwg`

作用：
生成随机密码。

命令格式：

```text
pwg [长度] [特殊符号集合] [count=数量] [nospecial]
```

使用示例：

```text
pwg
pwg 16
pwg 10 -_+
pwg 24 count=8
pwg 32 nospecial
```

规则说明：

- 第一个参数是密码长度
- 默认长度是 `16`
- 默认返回 `6` 条候选密码
- 默认包含内置特殊字符集合
- `nospecial` 表示完全不使用特殊字符
- 如果你提供一个仅由非字母数字字符组成的参数，它会被当成“允许使用的特殊符号集合”
- `pwg 10 -_+` 表示生成 10 位密码，且特殊字符只允许来自 `-`、`_`、`+`

### `md5`

作用：
对输入文本计算 MD5 十六进制字符串。

命令格式：

```text
md5 <文本>
```

使用示例：

```text
md5 hello
md5 123456
md5 hello world
```

返回结果：

- 一条 MD5 结果
- 回车后直接复制哈希值

### `sha`

作用：
计算常见 SHA 哈希。

支持算法：

- `sha1`
- `sha224`
- `sha256`
- `sha384`
- `sha512`
- `all`

命令格式：

```text
sha <文本>
sha <算法> <文本>
```

使用示例：

```text
sha hello
sha sha1 hello
sha sha512 hello
sha all hello
```

规则说明：

- 不写算法时，默认直接展示全部结果
- 默认顺序是：`sha256`、`sha512`、`sha1`、`sha224`、`sha384`
- 写 `all` 时，也按同样顺序展示全部结果

### `b64`

作用：
Base64 编码与解码。

命令格式：

```text
b64 <文本>
```

使用示例：

```text
b64 hello
b64 aGVsbG8=
```

规则说明：

- 默认同时返回 Base64 编码结果和解码结果
- 如果输入不是合法 Base64，会显示“解码失败”提示
- 不需要再写 `encode` 或 `decode`

### `json`

作用：
JSON 格式化与压缩。

命令格式：

```text
json <JSON>
json pretty <JSON>
json min <JSON>
```

使用示例：

```text
json {"a":1,"b":2}
json pretty {"a":1}
json min {"a":1,"b":2}
```

返回结果：

- `Pretty JSON`
- `Minified JSON`

规则说明：

- 默认优先展示格式化结果
- 如果输入不是合法 JSON，会提示错误位置

### `url`

作用：
同时展示 URL Encode 和 URL Decode 结果。

命令格式：

```text
url <文本>
```

使用示例：

```text
url hello world
url hello%20world
url name%3Dalfred%20tools
```

规则说明：

- 不需要区分 `urlencode` 和 `urldecode`
- 默认同时返回两种结果

### `html`

作用：
同时展示 HTML Encode 和 HTML Decode 结果。

命令格式：

```text
html <文本>
```

使用示例：

```text
html <div class="box">
html &lt;div&gt;hello&lt;/div&gt;
```

规则说明：

- 默认同时返回 Encode 和 Decode 两种结果
- 适合处理 HTML 片段或富文本内容

### `uuid`

作用：
生成 UUID。

命令格式：

```text
uuid
uuid all
uuid 1
uuid 4 count=5
```

规则说明：

- 默认直接等同于 `uuid all`
- 会返回 `UUID v1` 和 `UUID v4`
- 也支持单独指定 `v1`、`v4`
- 支持 `count=数字`

### `cron`

作用：
查看 cron 表达式从当前时间起最近 5 次执行时间。

命令格式：

```text
cron <表达式>
```

使用示例：

```text
cron */15 * * * *
cron 0 0/15 * * * ?
cron 0 30 9 * * MON-FRI
```

规则说明：

- 自动识别 `Linux crontab` 和 `Java cron`
- 结果中会明确标识类型
- 默认展示“从当前时间起向后计算”的最近 5 次执行

当前支持：

- `*`
- `,`
- `-`
- `/`
- `?`

当前暂不支持：

- `L`
- `W`
- `#`

### `ts`

作用：
时间戳和日期互转。

命令格式：

```text
ts
ts <时间戳>
ts <日期>
```

使用示例：

```text
ts
ts 1710505200
ts 1710505200000
ts 2026-03-22
ts 2026-03-22 10:30:00
```

规则说明：

- 不带参数时，显示当前时间、当日 0 点、当前秒级时间戳、当前毫秒级时间戳
- 输入纯数字时，自动识别为秒或毫秒时间戳
- 输入日期时，转换为秒和毫秒时间戳

### `tc`

作用：
文本统计。

命令格式：

```text
tc <文本>
```

使用示例：

```text
tc hello world
tc 这是一个测试
```

返回结果：

- 字符数
- 非空白字符数
- 单词数
- 行数
- UTF-8 字节数
- 中文字符数

### `case`

作用：
命名风格转换。

命令格式：

```text
case <文本>
```

使用示例：

```text
case hello world
case hello_world
case helloWorld
case HelloWorld
```

返回结果：

- `snake_case`
- `kebab-case`
- `camelCase`
- `PascalCase`
- `CONSTANT_CASE`
- `dot.case`

### `jwt`

作用：
JWT 解码。

命令格式：

```text
jwt <token>
```

使用示例：

```text
jwt eyJ...
```

规则说明：

- 当前只做解码
- 不校验签名
- 会返回 Header、Payload、Claims 摘要、Signature 和原始 JWT

### `timer`

作用：
创建倒计时提醒。

命令格式：

```text
timer <时间> [提醒内容]
```

使用示例：

```text
timer 10 喝水
timer 10s 起身活动
timer 1h 开会
```

规则说明：

- 纯数字默认按分钟
- `s` 表示秒
- `m` 表示分钟
- `h` 表示小时
- 默认是 `5` 分钟
- 时间到了会弹窗提醒并响铃

## 🧪 从源码运行

如果你在本地调试，可以统一通过 `workflow.py` 调度：

```bash
python3 workflow.py help ""
python3 workflow.py pwg "10 -_+"
python3 workflow.py md5 "hello world"
python3 workflow.py sha "hello"
python3 workflow.py b64 "aGVsbG8="
python3 workflow.py json '{"name":"dev-tools","stars":1}'
python3 workflow.py url "hello%20world"
python3 workflow.py uuid ""
python3 workflow.py cron "*/15 * * * *"
python3 workflow.py ts ""
python3 workflow.py tc "hello world"
python3 workflow.py case "hello_world"
python3 workflow.py html "&lt;div&gt;hello&lt;/div&gt;"
python3 workflow.py jwt "eyJ..."
python3 workflow.py timer --dry-run "10s 喝水"
```

## 📦 打包发布

项目内置标准打包脚本：

```bash
./scripts/package.sh
./scripts/package.sh v0.1.4
```

脚本会自动：

- 读取或更新 `info.plist` 中的版本号
- 打包生成 `.alfredworkflow`
- 校验 `info.plist`
- 检查包内的 `version` 和 `webaddress`

## 🏗️ 项目结构

```text
Alfred-Dev-Tools/
├── info.plist
├── icon.png
├── workflow.py
├── scripts/
├── docs/
└── alfred_dev_tools/
    ├── alfred.py
    ├── cli/
    └── features/
```

目录说明：

- `workflow.py`：统一入口，Alfred 通过它分发到具体命令
- `alfred_dev_tools/features/`：核心功能逻辑
- `alfred_dev_tools/cli/`：命令行与 Alfred 适配层
- `info.plist`：Alfred Workflow 配置
- `scripts/package.sh`：标准打包脚本
- `docs/GITHUB_DESCRIPTION.md`：GitHub 发布与推广文案

## 📚 额外文档

- GitHub 仓库描述与推广文案：
  [docs/GITHUB_DESCRIPTION.md](docs/GITHUB_DESCRIPTION.md)

## 📄 License

[MIT](LICENSE)
