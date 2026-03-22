# Usage Guide

## Hash

### `md5`

- `md5 hello`
- `md5 any text here`

输出 MD5 十六进制字符串，回车即可复制。

### `sha`

- `sha hello`
- `sha sha1 hello`
- `sha sha512 hello`
- `sha all hello`

默认算法是 `SHA256`。`all` 会同时返回多种 SHA 结果。

## Encode / Decode

### `b64`

- `b64 hello`
- `b64 encode hello`
- `b64 decode aGVsbG8=`

默认行为是 Base64 编码。

### `urlencode`

- `urlencode hello world`
- `urlencode name=alfred tools`

### `urldecode`

- `urldecode hello%20world`
- `urldecode name%3Dalfred%20tools`

### `html`

- `html <div class="box">`
- `html encode hello <world>`
- `html decode &lt;div&gt;hello&lt;/div&gt;`

默认行为是 HTML 转义。

## Formatting

### `jsonfmt`

- `jsonfmt {"a":1,"b":2}`
- `jsonfmt pretty {"a":1}`
- `jsonfmt min {"a":1,"b":2}`

会返回两项结果：

- Pretty JSON
- Minified JSON

如果显式写了 `min`，压缩结果会排在第一项。

## ID / Time

### `uuid`

- `uuid`
- `uuid 1`
- `uuid 4 count=5`
- `uuid all`

默认生成一个 `UUID v4`。

### `ts`

- `ts`
- `ts 1710505200`
- `ts 1710505200000`
- `ts 2026-03-22`
- `ts 2026-03-22 10:30:00`

规则：

- 空参数：显示当前时间、当日 0 点、当前秒级和毫秒级时间戳
- 纯数字：自动识别为秒或毫秒时间戳
- 日期字符串：转换成秒级和毫秒级时间戳

## Text

### `textstat`

- `textstat hello world`
- `textstat 这是一个测试`

统计项目包括：

- 字符数
- 非空白字符数
- 单词数
- 行数
- UTF-8 字节数
- 中文字符数

### `case`

- `case hello world`
- `case hello_world`
- `case helloWorld`
- `case HelloWorld`

返回以下风格：

- `snake_case`
- `kebab-case`
- `camelCase`
- `PascalCase`
- `CONSTANT_CASE`
- `dot.case`

## JWT

### `jwt`

- `jwt <token>`

会解析并返回：

- Header JSON
- Payload JSON
- 常见 Claims 摘要
- Signature 段
- 原始 JWT

注意：

- 当前只做解码，不校验签名
- 适合查看 token 内容，不适合安全校验场景

## Utility

### `pwd`

- `pwd`
- `pwd 16`
- `pwd 32 nospecial`
- `pwd 24 special count=8`

### `settimer`

- `settimer 10 喝水`
- `settimer 10s 起身活动`
- `settimer 1h 开会`

规则：

- 纯数字默认按分钟
- `s` 表示秒
- `m` 表示分钟
- `h` 表示小时
- 默认 5 分钟
