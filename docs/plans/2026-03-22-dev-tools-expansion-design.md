# Dev Tools Expansion Design

## Goal

把当前 Alfred Workflow 从单点能力工具升级为可持续扩展的开发者工具箱，并保持后续新增功能的实现成本稳定可控。

## Chosen Approach

继续沿用并强化当前的三层结构：

- `features/` 负责纯业务逻辑
- `cli/` 负责 Alfred / 命令行入口适配
- 顶层脚本只做极薄转发

这比把业务逻辑直接写进 Alfred 脚本更容易维护，也比为了少量功能过早引入复杂框架更轻量。

## Added Capability Set

本轮新增能力：

- SHA 哈希
- Base64 编解码
- JSON 格式化
- URL Encode / Decode
- UUID 生成
- 文本统计
- 命名风格转换
- HTML 实体转义 / 反转义
- JWT 解码

保留原有能力：

- 随机密码
- MD5
- 时间戳转换
- 倒计时提醒

## UX Principles

- 所有 Alfred Script Filter 尽量返回可直接复制的结果
- 输入空值时展示简洁 usage
- 对开发场景高频结果提供多项备选，例如 `jsonfmt` 同时给 pretty 和 minified
- 对多结果场景统一复用剪贴板输出

## Next Recommended Additions

- Query String parser
- Regex tester
- Hex / ASCII converter
- HTTP status lookup
- Cron helper
