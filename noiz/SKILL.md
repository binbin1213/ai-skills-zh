---
name: noiz
description: Use when OpenClaw needs to turn user-provided text into a spoken audio message, especially for requests like “语音说 {文本}”, “把这段话转成语音”, “念出来”, “朗读这段话”, or “生成语音消息”.
---

# Noiz 语音技能

## Overview

使用 Noiz text-to-speech API 生成音频，并优先转成更适合语音消息的 `OGG/Opus` 文件，再输出 `MEDIA:{绝对路径}`。

这个技能是给 OpenClaw 执行的，不是给最终用户手动运行的安装说明。

脚本职责有三件事：

1. 调用 Noiz API 生成原始音频文件
2. 优先把音频转成 `OGG/Opus`
3. 打印 `MEDIA:{绝对路径}` 让宿主环境继续发送媒体

是否会以“语音气泡”还是“普通音频附件”发送，取决于 OpenClaw 所连接的平台和媒体发送实现。

## When to Use

- 用户要求“语音说 {文本}”
- 用户要求把一段文本转成语音消息
- 当前环境支持识别 `MEDIA:` 输出并发送音频文件

不要在这些情况下使用：

- 用户还没有提供要朗读的文本
- 当前环境没有配置 `NOIZ_API_KEY`
- 用户目标是特定平台的“语音气泡”，但宿主当前并不支持对应格式或参数

## Preconditions

在调用脚本前，先确认以下前置条件：

1. 已配置环境变量 `NOIZ_API_KEY`
2. 当前运行环境可以访问 `https://api.noiz.ai`
3. 技能目录或 `NOIZ_DOWNLOAD_DIR` 可写

如果 `NOIZ_API_KEY` 未配置，不要直接假装调用成功。先提示用户完成以下操作：

1. 注册并登录 `https://noiz.ai`
2. 进入 `https://developers.noiz.ai`
3. 在 `API Keys` 页面创建 API Key
4. 新用户通常会获得 `100,000` 免费积分，可先用于测试
5. 让宿主环境配置 `NOIZ_API_KEY`

## Execution

运行脚本：

```bash
python3 ./tts_noiz.py "要说的文本"
```

成功时脚本会输出：

```text
MEDIA:/Users/binbin/Desktop/noiz/downloads/noiz_a1b2c3d4.ogg
```
更真实的示例（实际运行会生成类似路径）：
```text
MEDIA:./downloads/noiz_a1b2c3d4.ogg
```

如果宿主支持 `MEDIA:` 约定，应继续发送该文件。

如果脚本输出不是 `MEDIA:` 开头，视为失败并向用户说明原因。

## Output Contract

- API 端点：`https://api.noiz.ai/v1/text-to-speech`
- 认证方式：`Authorization: $NOIZ_API_KEY`
- 优先输出音频格式：`OGG/Opus`
- 转码失败时回退格式：`MP3`
- 默认输出目录：技能目录下的 `downloads/`
- 可选输出目录：环境变量 `NOIZ_DOWNLOAD_DIR`
- 成功标志：标准输出包含一行 `MEDIA:{绝对路径}`

## Platform Notes

这个技能现在会优先输出 `OGG/Opus`，比单纯 `MP3` 更接近许多平台的语音消息要求。对 OpenClaw 来说，这能减少“发出去只是普通音频文件”的概率；但是否最终显示成平台原生语音消息，仍然取决于宿主发送链路。

快速参考：

| 平台 | 当前输出可用性 | 语音消息额外要求 |
| --- | --- | --- |
| Telegram | 当前默认 `OGG/Opus` 更合适 | 若宿主支持 `asVoice: true` 或 `[[audio_as_voice]]`，更容易形成语音气泡 |
| 飞书 | `OGG/Opus`/`Opus` 更接近语音消息需求 | 仍可能需要宿主走音频消息类型 |
| WhatsApp | 当前默认 `OGG/Opus` 更合适 | 是否显示为原生语音消息，仍取决于连接器实现 |
| Discord | 当前输出是本地文件，链路更友好 | 宿主通常还需要 `ffmpeg`/`ffprobe` 或额外语音消息处理 |
| iMessage | 可作为音频文件继续发送 | 是否转成更原生语音形式，仍取决于桥接层 |

更详细的平台说明见同目录参考文件 `platform-voice-guide.md`。只有当用户明确关心某个平台会怎么发送，或要求“语音气泡”而不是普通附件时，再读取该参考文件。

## Failure Handling

### 缺少 API Key

脚本输出：

```text
缺少环境变量 NOIZ_API_KEY
```

处理方式：不要重试调用。改为引导用户注册 Noiz、创建 API Key，并在 OpenClaw 运行环境中配置 `NOIZ_API_KEY`。

### API 返回非 200

脚本输出类似：

```text
生成失败：401 - ...
```

处理方式：提示用户检查 API Key、账户状态、积分是否足够，以及 Noiz API 是否有变更。

### 网络错误

脚本输出类似：

```text
请求异常：...
```

处理方式：确认当前宿主环境能访问 `https://api.noiz.ai`，再决定是否重试。

### 平台不支持语音气泡

如果用户明确要“语音气泡”而当前宿主仍然没有按语音消息方式发送，要如实说明：

- 当前技能已成功生成语音文件
- 当前技能已经优先输出 `OGG/Opus`
- 如果仍然没有语音气泡，通常说明还缺平台专用参数或宿主发送链路支持

## Examples

用户说：

```text
语音说 你好，我是心心
```

执行：

```bash
python3 ./tts_noiz.py "你好，我是心心"
```

脚本返回：

```text
MEDIA:/absolute/path/to/noiz_a1b2c3d4.ogg
```

此时 OpenClaw 应把该文件继续作为媒体发送。

## Tips

- 不要把 Noiz API Key 写进源码，只从环境变量读取。
- 如果用户还没开通 Noiz，不要先执行脚本，先引导注册和创建 API Key。
- 新用户通常有 `100,000` 免费积分，适合先做一次短文本验证。
- `MEDIA:` 是这个技能和宿主之间的契约，不要改成别的输出格式。
- 当前默认会先尝试输出 `OGG/Opus`；只有转码失败时才回退到 `MP3`。
- 在 OpenClaw 环境中，优先输出 `OGG/Opus` 能显著提升语音消息体验。
- OpenClaw 发送时，参考 `platform-voice-guide.md` 选择正确的平台参数（`asVoice`、`msg_type` 等）。
- 不要承诺一定能成语音气泡，除非确认发送链路支持特定参数。
- 中文文本编码统一使用 UTF-8，避免跨环境时的不一致问题。
