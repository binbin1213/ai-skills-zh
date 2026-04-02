# OpenClaw 平台语音发送执行手册

## 快速开始

这个文件告诉你拿到 `MEDIA:{path}.ogg` 后，如何根据平台发送。

**核心原则**：
```
主技能输出 OGG → OpenClaw 根据平台选择发送方式 → 添加平台参数 → 告诉用户结果
```

## 用途

这个文件是给 OpenClaw 用的，告诉你拿到 `MEDIA:{绝对路径}` 后，如何根据平台发送。

当用户关心下面这些问题时，再读取本文件：
- "发到 Telegram/飞书/WhatsApp/Discord/iMessage，要用什么参数？"
- "为什么这条消息发出去是附件，不是语音气泡？"

如果用户只是说"语音说一段话"，通常不需要读取本文件。

## 核心判断

主技能当前输出是：
- 本地音频文件
- 优先格式为 `OGG/Opus`
- 转码失败时回退到 `MP3`
- 通过 `MEDIA:{绝对路径}` 交给宿主发送

OpenClaw 按下面的顺序判断：

1. 识别 `MEDIA:` 输出的文件路径
2. 确认用户指定或默认目标平台
3. 查阅对应平台的发送要求
4. 构造发送参数（包含 platform、target、media 和推荐参数）
5. 执行发送并向用户说明预期效果

---

## 各平台执行指南

### Telegram

**发送参数选择**

如果 OpenClaw 支持 Telegram 发送，拿到 `MEDIA:{path}.ogg` 后：

```json
{
  "action": "send",
  "channel": "telegram",
  "target": "username_or_id",
  "media": "MEDIA:{path}.ogg",
  "asVoice": true
}
```

**关键说明**

- `media`：主技能输出的 `MEDIA:` 路径
- `asVoice: true`：尝试让 Telegram 显示成语音气泡
- 如果当前 OpenClaw 链路不支持 `asVoice` 参数，就如实说"会以普通音频发送"
- 如果用户明确要求 Telegram 语音气泡，而当前不支持，建议对方检查 OpenClaw Telegram 插件是否支持 `asVoice` 或 `[[audio_as_voice]]`

**用户对话示例**

用户："发到 Telegram，要语音气泡"

OpenClaw："已生成 OGG 格式音频。我会尝试用语音消息方式发送，但如果当前 Telegram 链路不支持，会以普通音频发送。"

---

### 飞书

**发送参数选择**

如果 OpenClaw 支持飞书发送，拿到 `MEDIA:{path}.ogg` 后：

```json
{
  "action": "send",
  "channel": "feishu",
  "target": "user_id_or_phone",
  "media": "MEDIA:{path}.ogg",
  "msg_type": "audio"
}
```

**关键说明**

- `media`：主技能输出的 `MEDIA:` 路径
- `msg_type: "audio"`：让飞书识别为音频消息而不是普通文件附件
- 如果当前 OpenClaw 链路不支持 `msg_type`，说明"会以普通附件发送"

**用户对话示例**

用户："发到飞书"

OpenClaw："已生成 OGG 格式音频。我会尝试按音频消息发送，但如果当前飞书链路不支持音频消息类型，会以普通文件发送。"

---

### WhatsApp

**发送参数选择**

如果 OpenClaw 支持 WhatsApp 发送，拿到 `MEDIA:{path}.ogg` 后：

```json
{
  "action": "send",
  "channel": "whatsapp",
  "target": "phone_number",
  "media": "MEDIA:{path}.ogg"
}
```

**关键说明**

- WhatsApp 通常对语音消息支持较好
- 当前 `.ogg` 输出比 `.mp3` 更接近 WhatsApp 原生语音格式
- 如果 OpenClaw 链路有自动转换，可能会直接按语音消息发送
- 如果用户问"为什么不是语音气泡"，说明："已用 OGG 格式，是否显示为更原生的语音消息取决于 WhatsApp 连接器实现"

**用户对话示例**

用户："发到 WhatsApp"

OpenClaw："已生成 OGG 格式音频。已更接近 WhatsApp 语音消息格式，但最终是否显示为语音消息取决于连接器实现。"

---

### Discord

**发送参数选择**

如果 OpenClaw 支持 Discord 发送，拿到 `MEDIA:{path}.ogg` 后：

```json
{
  "action": "send",
  "channel": "discord",
  "target": "channel_id",
  "path": "MEDIA:{path}.ogg",
  "asVoice": true
}
```

**关键说明**

- `path`：主技能输出的 `MEDIA:` 路径（Discord 通常要求本地文件路径）
- `asVoice: true`：尝试让 Discord 识别为语音消息
- Discord 语音体验往往还依赖 `ffmpeg`/`ffprobe` 进行波形生成和元数据补充
- 如果用户要求的是 Discord 里的语音样式消息，OpenClaw 应说明："主技能已生成音频，但 Discord 端语音体验是否成立，取决于宿主是否具备转码和语音消息发送能力"

**用户对话示例**

用户："发到 Discord"

OpenClaw："已生成音频文件。已满足 Discord 本地文件要求，但语音消息体验取决于宿主是否支持转码和语音消息发送。"

---

### iMessage（BlueBubbles 等）

**发送参数选择**

如果 OpenClaw 支持 iMessage 发送，拿到 `MEDIA:{path}.ogg` 后：

```json
{
  "action": "send",
  "channel": "imessage",
  "target": "email_or_phone",
  "media": "MEDIA:{path}.ogg",
  "asVoice": true
}
```

**关键说明**

- `media`：主技能输出的 `MEDIA:` 路径
- `asVoice: true`：让桥接层尝试按语音消息发送（某些桥接会自动转为 `CAF` 等语音格式）
- iMessage 语音支持高度依赖桥接层（如 BlueBubbles）
- 如果用户要求 iMessage 原生语音形式，OpenClaw 应把责任边界说清楚："这个技能负责生成音频，最终是否成为原生语音取决于桥接层"

**用户对话示例**

用户："发到 iMessage"

OpenClaw："已生成音频文件。已通过 asVoice 参数尝试语音消息发送，但最终是否显示为原生语音取决于 iMessage 桥接实现。"

---

## 快速决策表

OpenClaw 拿到 `MEDIA:{path}.ogg` 后，根据平台快速决策：

| 平台 | 必须参数 | 推荐参数 | 若不支持则说明 |
| --- | --- | --- | --- |
| Telegram | `media` | `asVoice: true` | "会以普通音频发送" |
| 飞书 | `media`, `msg_type` | `msg_type: "audio"` | "会以普通附件发送" |
| WhatsApp | `media` | 无（当前格式已合适） | "是否语音消息取决于连接器" |
| Discord | `path`, `asVoice` | `asVoice: true` | "已生成本地音频，语音样式取决于连接器" |
| iMessage | `media`, `asVoice` | `asVoice: true` | "是否原生语音取决于桥接层" |

---

## 常见对话模板

### 场景 1：用户只说"语音说 xxx"

```
OpenClaw: 直接调用主技能生成音频，拿到 MEDIA:{path}.ogg

如果用户指定了平台：
  → 查本文件的"各平台执行指南"段落
  → 选择该平台推荐的参数组合
  → 如果当前不支持，诚实说明会是什么效果
```

### 场景 2：用户问"为什么不是语音气泡？"

```
OpenClaw: 按顺序说明：

1. 主技能已成功生成 OGG/Opus 格式
2. 当前输出已比纯 MP3 更接近语音消息要求
3. 但最终是否显示成语音气泡，取决于平台和 OpenClaw 发送链路
4. 如果当前链路不支持平台专用参数（asVoice、msg_type 等），通常会退化成普通音频/附件
```

### 场景 3：用户指定"Telegram/飞书/WhatsApp/Discord/iMessage + 语音"

```
OpenClaw:

1. 确认主技能已输出 MEDIA:{path}.ogg
2. 查本文件对应平台的"发送参数选择"
3. 构造该平台的 JSON 参数（包含 platform、target、media、以及推荐参数）
4. 如果当前 OpenClaw 不支持某些参数，如实告知用户
5. 执行发送后，向用户说明预期效果（如"应该会以语音消息发送"或"可能只是普通附件"）
```

---

## 一句话原则

**主技能负责生成 `.ogg`，OpenClaw 负责根据平台选择发送方式和参数。是否显示成语音气泡取决于平台和发送链路实现，不要把平台专用逻辑硬塞进主技能里。**
