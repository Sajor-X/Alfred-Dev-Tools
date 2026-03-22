# Alfred-Dev-Tools

一个面向开发者的 Alfred Workflow，内置哈希、编码解码、JSON 格式化、UUID、时间戳、文本统计、命名风格转换、JWT 解码、随机密码、倒计时提醒等常用工具。

- Author: `Sajor`
- GitHub: [Sajor-X/Alfred-Dev-Tools](https://github.com/Sajor-X/Alfred-Dev-Tools)
- License: `MIT`

项目目标很简单：

- 让常见开发小工具都能通过 Alfred 一步直达
- 保持纯 Python 标准库实现，方便安装、维护和二次扩展
- 用统一的 `features/ + cli/ + 顶层薄入口` 结构持续扩容

## Features

当前已支持：

- `pwd`：随机密码生成
- `md5`：MD5 哈希
- `sha`：SHA1 / SHA224 / SHA256 / SHA384 / SHA512
- `b64`：Base64 编码 / 解码
- `jsonfmt`：JSON pretty / minify
- `urlencode`：URL 编码
- `urldecode`：URL 解码
- `uuid`：UUID v1 / v4 批量生成
- `ts`：当前时间、时间戳与日期互转
- `textstat`：字符数、单词数、行数、字节数统计
- `case`：snake / kebab / camel / Pascal / CONSTANT / dot case 转换
- `html`：HTML 实体转义 / 反转义
- `jwt`：JWT Header / Payload 解码
- `settimer`：倒计时提醒

适合继续扩展的候选能力：

- 正则测试与提取
- Query String 解析
- JWT 过期时间提醒
- Hex / ASCII / Unicode 转换
- SQL / XML / YAML 格式化
- Cron 表达式辅助
- HTTP 状态码速查
- Color Hex / RGB / HSL 转换

## Install

你有两种方式使用：

1. 直接导入仓库里的 `.alfredworkflow` 包
2. 在 Alfred 中手动创建 Workflow，并把 `info.plist` / Python 脚本接进去

推荐直接导入：

- `Alfred-Dev-Tools.alfredworkflow`

## Keywords

| Keyword | 用途 | 示例 |
| --- | --- | --- |
| `pwd` | 生成随机密码 | `pwd 24 nospecial count=4` |
| `md5` | 生成 MD5 | `md5 hello world` |
| `sha` | 生成 SHA 哈希 | `sha hello` / `sha sha512 hello` / `sha all hello` |
| `b64` | Base64 编解码 | `b64 hello` / `b64 decode aGVsbG8=` |
| `jsonfmt` | 格式化 JSON | `jsonfmt {"a":1}` / `jsonfmt min {"a":1}` |
| `urlencode` | URL 编码 | `urlencode hello world` |
| `urldecode` | URL 解码 | `urldecode hello%20world` |
| `uuid` | 生成 UUID | `uuid` / `uuid 1` / `uuid all` / `uuid count=5` |
| `ts` | 时间戳与日期互转 | `ts` / `ts 1710505200` / `ts 2026-03-22 10:30:00` |
| `textstat` | 文本统计 | `textstat hello world` |
| `case` | 命名风格转换 | `case hello_world` / `case helloWorld` |
| `html` | HTML 转义 | `html <div>` / `html decode &lt;div&gt;` |
| `jwt` | JWT 解码 | `jwt eyJ...` |
| `settimer` | 倒计时提醒 | `settimer 10m 喝水` |

更多用法见 [docs/USAGE.md](docs/USAGE.md)。

## Project Structure

```text
alfred-password-workflow/
├── info.plist
├── icon.png
├── *.py
└── alfred_password_workflow/
    ├── alfred.py
    ├── cli/
    └── features/
```

分层约定：

- `alfred_password_workflow/features/`：核心业务逻辑
- `alfred_password_workflow/cli/`：命令行入口
- 顶层 `*.py`：给 Alfred 调用的薄包装脚本
- `info.plist`：Workflow 配置

新增能力时推荐继续遵循这个模式：

1. 先在 `features/` 写核心功能
2. 再在 `cli/` 补 Alfred 入口
3. 最后在顶层加一个极薄的兼容脚本
4. 将新 keyword 接入 `info.plist`

## Local Test

```bash
python3 md5.py "hello world"
python3 sha.py "sha512 hello world"
python3 b64.py "decode aGVsbG8="
python3 jsonfmt.py '{"name":"dev-tools","stars":1}'
python3 urlencode.py "hello world"
python3 urldecode.py "hello%20world"
python3 uuidgen.py "all"
python3 ts.py ""
python3 textstat.py "hello world"
python3 caseconv.py "hello_world"
python3 htmlcodec.py "<div class=\"box\">"
python3 jwt.py "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4iLCJpYXQiOjE1MTYyMzkwMjJ9.signature"
python3 start_timer.py --dry-run "10s 喝水"
```

## Open Source Notes

准备放到 GitHub 时，建议把这些文件一起带上：

- `README.md`
- `docs/USAGE.md`
- `docs/GITHUB_DESCRIPTION.md`
- `.gitignore`

如果你准备正式开源，下一步建议补：

- License
- CONTRIBUTING
- Release Notes
- 演示截图 / GIF

GitHub 仓库描述与推广文案已经整理在 [docs/GITHUB_DESCRIPTION.md](docs/GITHUB_DESCRIPTION.md)。

## License

[MIT](LICENSE)
