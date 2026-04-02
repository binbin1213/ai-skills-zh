---
name: voice-tts
description: 使用 edge-tts 生成高质量中文语音消息并发送。当用户要求发语音、语音回复、TTS、文字转语音、语音播报、语音消息时使用。支持多种中文声音（男声/女声/方言），可调节语速音调，适用于飞书/Telegram/Discord 等渠道的语音消息发送。支持两种实现：Python edge-tts（推荐，稳定）和 Node.js node-edge-tts（功能完整）。
---

# Voice TTS（edge-tts 语音合成）

使用 Microsoft edge-tts（免费）生成高质量中文语音，通过 `message` 工具发送语音消息。

支持两种实现方式：
1. **Python edge-tts** - 通过 `tts.sh` 包装，稳定成熟，推荐使用
2. **Node.js node-edge-tts** - 完整功能，支持配置持久化，适合深度定制

## ⚠️ 安装（首次使用必读）

### 方式一：Python edge-tts（推荐）

本 skill 依赖 **edge-tts** Python包，需先全局安装。安装前请自查系统环境：

#### 1. 检查是否已安装

```bash
which edge-tts
```

如果返回路径（如 `/usr/local/bin/edge-tts`），说明已安装，跳到「快速流程」。

#### 2. 根据系统选择安装方式

**macOS（推荐 pipx，独立环境不污染系统）：**

```bash
# 先确认 pipx 是否已安装
which pipx
# 如果没有：brew install pipx
pipx install edge-tts
pipx ensurepath
```

> ⚠️ macOS 的 Homebrew Python 受 PEP 668 限制，禁止直接 `pip install`。
> 不要用 `pip install --break-system-packages`，会污染系统 Python。

**Linux（推荐 pipx，或用 --user 安装）：**

```bash
# 方式一：pipx（推荐）
pipx install edge-tts

# 方式二：pip --user（如果 pipx 不可用）
pip install --user edge-tts
# 安装后确保 ~/.local/bin 在 PATH 中
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

**Windows（PowerShell）：**

```powershell
pip install edge-tts
# 或
pipx install edge-tts
```

#### 3. 验证安装

```bash
edge-tts --list-voices | head -5
```

看到语音列表即安装成功。

### Post-Installation Setup（Python 版）

安装完成后，**你（智能体）必须**执行以下步骤：

1. **验证安装**：运行命令确认功能正常
   ```bash
   edge-tts --list-voices | grep "zh-"
   ```

2. **确认并告知用户**：
   > "✅ Edge TTS (Python) 安装成功！"

   如果命令失败：
   > "❌ 安装验证失败，请检查 edge-tts 是否正确安装。"

3. **告知关键信息**：
   - 使用微软 Edge 免费神经 TTS 服务，不需要 API 密钥
   - 输出为 opus 格式，适合语音消息
   - 需要互联网连接
   - 支持多种中文音色，包括方言

4. **询问用户偏好**：
   - 默认音色选择（推荐：`zh-CN-YunxiNeural` 男声）
   - 默认语速（默认正常，可选择 -10% 到 +20%）
   - 如果需要使用代理，请询问代理 URL

5. **保存偏好**：
   Python 版本没有内置配置管理器，但你（智能体）可以在对话中记住用户偏好，或将配置保存在 `~/.config/voice-tts.conf`。

---

### 方式二：Node.js node-edge-tts

如果你偏好 Node.js 环境，或需要配置持久化功能：

```bash
cd scripts
npm install
```

这将安装：
- `node-edge-tts` - TTS 库
- `commander` - 命令行参数解析

安装后需要完成设置：

1. **验证安装**：运行基础测试确认功能正常
   ```bash
   cd scripts
   npm test
   ```

2. **确认并告知用户**：如果测试通过，告诉用户 "✅ Edge TTS 安装成功！"；失败则提示检查网络

3. **告知关键信息**：免费服务，不需要 API 密钥，需要联网

4. **询问用户偏好**：
   - 默认音色选择
   - 默认语速
   - 是否默认保存字幕
   - 是否需要代理

5. **保存偏好**：使用配置管理器保存
   ```bash
   cd scripts
   node config-manager.js --set-voice <selected-voice>
   ```

6. **确认配置**：展示已保存配置
   
   ```bash
   cd scripts
   node config-manager.js --get
   ```

---

## 项目结构

```text
voice-tts/
├── SKILL.md                 # 技能文档
├── scripts/                 # 脚本目录
│   ├── tts.sh               # Python edge-tts 封装（推荐使用）
│   ├── tts-converter.js     # Node.js TTS 转换器
│   ├── config-manager.js    # Node.js 配置管理器
│   └── package.json         # NPM 依赖
└── references/
    ├── node_edge_tts_guide.md       # node-edge-tts 完整参考文档
    └── openclaw-voice-send.md      # OpenClaw 飞书语音发送教程
```

---

## 快速流程（Python 版）

1. 运行 `tts.sh` 生成语音 → 获取文件路径
2. 用 `message` 工具发送（设置 `asVoice: true`）

## 生成语音（Python 版）

```bash
bash <skill_dir>/scripts/tts.sh "文本内容" [voice] [output_path]
```

**预期输出：**

- 返回生成的音频文件路径（如 `~/.openclaw/media/openclaw_voice_1710556800.opus`）
- 文件格式：opus（高质量，体积小）
- 文件大小：约 5-20 KB（取决于文本长度）

**参数说明：**
- 第 1 参数（必填）：文本内容，建议 50-300 字
- 第 2 参数（可选）：声音名称，默认 `zh-CN-YunxiNeural`
- 第 3 参数（可选）：输出路径，默认 `~/.openclaw/media/`

**示例：**
```bash
# 基础用法
bash <skill_dir>/scripts/tts.sh "你好，这是一条测试语音"

# 指定声音
bash <skill_dir>/scripts/tts.sh "你好" "zh-CN-XiaoxiaoNeural"

# 指定输出路径
bash <skill_dir>/scripts/tts.sh "你好" "zh-CN-YunxiNeural" "/tmp/test.opus"
```

## 发送语音

### OpenClaw 飞书发送要求

OpenClaw 对语音消息有特定格式要求：

```json
{
  "action": "send",
  "channel": "feishu",
  "asVoice": true,
  "filePath": "/tmp/openclaw/voice.opus",
  "mimeType": "audio/opus"
}
```

**必须满足：**
- ✅ 文件格式：**`.opus`**（不是 mp3）
- ✅ 输出目录：`/tmp/openclaw/`（必须放在这个允许目录）
- ✅ `asVoice: true`（作为语音消息，不是普通文件）
- ✅ `mimeType: "audio/opus"`

**预期结果：**
- 音频文件作为语音消息发送到指定渠道
- 消息格式：语音消息（不是文件附件）
- 发送时间：通常 1-3 秒（取决于文件大小和网络）

**参数说明：**
- `action`: 固定为 "send"
- `channel`: 目标渠道（feishu/telegram/discord）
- `asVoice`: 必须为 `true`（触发语音消息发送）
- `filePath`: 语音文件的绝对路径，必须在允许目录内
- `mimeType`: MIME 类型，opus 格式用 `"audio/opus"`

用 `message` 工具调用，`channel` 设为当前渠道。

### 生成语音时指定 opus 格式

**Python 版 tts.sh** 默认输出就是 `opus` 到 `~/.openclaw/media/`，需要移动到 `/tmp/openclaw/`：
```bash
OUTPUT=$(bash <skill_dir>/scripts/tts.sh "文本内容")
mv "$OUTPUT" /tmp/openclaw/voice.opus
# 然后发送 /tmp/openclaw/voice.opus
```

**Node.js 版 tts-converter.js** 指定输出路径和 opus：
```bash
cd scripts
node tts-converter.js "文本内容" --voice zh-CN-XiaoxiaoNeural --output /tmp/openclaw/voice.opus
```

### 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 语音没收到 | 缺少 `asVoice: true` | 添加 `asVoice: true` |
| 文件发送失败 | 路径不在允许目录 | 必须放到 `/tmp/openclaw/` |
| 格式不支持 | 使用了 mp3 格式 | 转换为 opus 格式 |

### 清理

**发送成功后必须立即删除临时文件**：
```bash
rm "/tmp/openclaw/voice.opus"
```

否则 `/tmp/openclaw/` 会累积大量冗余文件占用磁盘空间。

## 可用中文声音

| Voice | 性别 | 风格 |
|-------|------|------|
| zh-CN-YunxiNeural | 男 | 活泼阳光 ⭐ 默认 |
| zh-CN-XiaoxiaoNeural | 女 | 温暖自然 |
| zh-CN-YunyangNeural | 男 | 沉稳旁白 |
| zh-CN-XiaoyiNeural | 女 | 活泼 |
| zh-CN-liaoning-XiaobeiNeural | 女 | 东北话 |
| zh-TW-HsiaoChenNeural | 女 | 台湾腔 |

---

## 完整场景示例

### 场景 1：飞书通知

```bash
# 1. 生成语音（会议提醒）
bash <skill_dir>/scripts/tts.sh "提醒：项目评审会议将在5分钟后开始，请做好准备"
# 输出：~/.openclaw/media/openclaw_voice_1710556800.opus

# 2. 发送到飞书群
{
  "action": "send",
  "channel": "feishu",
  "asVoice": true,
  "filePath": "~/.openclaw/media/openclaw_voice_1710556800.opus"
}
```

### 场景 2：Telegram 私信

```bash
# 1. 生成语音（客服回复）
bash <skill_dir>/scripts/tts.sh "zh-CN-XiaoxiaoNeural" "您好，您的问题已收到，我们会尽快处理"
# 输出：~/.openclaw/media/openclaw_voice_1710556900.opus

# 2. 发送到 Telegram
{
  "action": "send",
  "channel": "telegram",
  "asVoice": true,
  "filePath": "~/.openclaw/media/openclaw_voice_1710556900.opus"
}
```

### 场景 3：Discord 频道公告

```bash
# 1. 生成语音（系统公告，正式语速）
bash <skill_dir>/scripts/tts.sh "zh-CN-YunxiNeural" "服务器维护将于今晚23:00开始，预计2小时"
# 输出：~/.openclaw/media/openclaw_voice_1710557000.opus

# 2. 发送到 Discord 频道
{
  "action": "send",
  "channel": "discord",
  "asVoice": true,
  "filePath": "~/.openclaw/media/openclaw_voice_1710557000.opus"
}
```

### 场景 4：长文本分段生成

```bash
# 长文本（>500字）必须分段
TEXT_PART1="第一部分：今天天气晴朗，温度适宜，适合外出活动。"
TEXT_PART2="第二部分：请大家注意防晒，多喝水，保持良好的作息时间。"
TEXT_PART3="第三部分：祝大家度过美好的一天！"

# 分别生成
VOICE1=$(bash <skill_dir>/scripts/tts.sh "$TEXT_PART1")
VOICE2=$(bash <skill_dir>/scripts/tts.sh "$TEXT_PART2")
VOICE3=$(bash <skill_dir>/scripts/tts.sh "$TEXT_PART3")

# 依次发送（实际使用时可能需要根据渠道限制添加延迟）
echo "$VOICE1"  # 第一段语音路径
echo "$VOICE2"  # 第二段语音路径
echo "$VOICE3"  # 第三段语音路径
```

### 场景 5：定制参数（语速/音调/音量）

```bash
# 快节奏通知（语速 +20%）
edge-tts --voice zh-CN-YunxiNeural --rate +20% --text "紧急通知：服务器将在1分钟后重启" --write-media /tmp/emergency.opus

# 正式公告（语速 -10%，音量 +5%）
edge-tts --voice zh-CN-YunxiNeural --rate -10% --volume +5% --text "年度总结大会将于下周一举行" --write-media /tmp/announcement.opus

# 强调语气（音调 +5Hz）
edge-tts --voice zh-CN-YunxiNeural --pitch +5Hz --text "重要！" --write-media /tmp/emphasis.opus
```

查看全部中文声音：

```bash
edge-tts --list-voices | grep "zh-"
```

## 参数调节

通过 `--rate`（语速）、`--pitch`（音调）、`--volume`（音量）调节：

```bash
# 语速 +20%，音量 +10%
edge-tts --voice zh-CN-YunxiNeural --rate +20% --volume +10% --text "你好" --write-media ~/.openclaw/media/out.opus
```

## Node.js 版本使用

对于需要配置持久化或偏好 Node.js 环境：

### TTS 转换器

```bash
cd scripts
npm install
node tts-converter.js "你的文本" --voice zh-CN-YunxiNeural --rate +10% --output output.mp3
```

**选项：**
- `--voice, -v`: 音色名称
- `--lang, -l`: 语言代码
- `--format, -o`: 输出格式
- `--pitch`: 音高调整 (+10%, -20%)
- `--rate, -r`: 语速调整 (+10%, -20%)
- `--volume`: 音量调整 (+10%, -10%)
- `--save-subtitles, -s`: 保存字幕为 JSON
- `--output, -f`: 输出文件路径
- `--proxy, -p`: 代理 URL
- `--timeout`: 请求超时毫秒数
- `--list-voices, -L`: 列出常用音色

### 配置管理器

```bash
cd scripts
node config-manager.js --set-voice zh-CN-YunxiNeural
node config-manager.js --set-rate +10%
node config-manager.js --get
node config-manager.js --reset
```

保存的配置会持久化存储在 `~/.tts-config.json`。

## 注意事项

- 文本建议 1000 字以内，长文本分段生成
- 输出目录为 `~/.openclaw/media/`（确保 OpenClaw 有权限访问）
- 临时文件发送后可删除

---

## 💡 实用技巧

**文本长度优化：**
- 50-300 字最佳，语音质量最高
- 300-500 字可接受，建议用中性语速
- 超过 500 字必须分段，否则生成超时或质量下降

**声音选择建议：**
- 通知/提醒：`zh-CN-YunxiNeural`（男声，活泼阳光）⭐ 默认
- 客服/陪伴：`zh-CN-XiaoxiaoNeural`（女声，温暖自然）
- 互动娱乐：`zh-CN-XiaoyiNeural`（女声，活泼）
- 旁白叙述：`zh-CN-YunyangNeural`（男声，沉稳）
- 特定场景：方言声音增强亲和力，但通用场景慎用

**参数调节指南：**
```bash
# 快节奏通知：语速 +20%
edge-tts --voice zh-CN-YunxiNeural --rate +20% --text "提醒：会议将在5分钟后开始" --write-media out.opus

# 正式公告：语速 -10%，音量 +5%
edge-tts --voice zh-CN-YunxiNeural --rate -10% --volume +5% --text "系统维护通知" --write-media out.opus

# 嘈杂环境：音量 +10%
edge-tts --voice zh-CN-YunxiNeural --volume +10% --text "重要提醒" --write-media out.opus

# 强调语气：音调 +5Hz
edge-tts --voice zh-CN-YunxiNeural --pitch +5Hz --text "注意！" --write-media out.opus
```

**常见陷阱：**
- ❌ 文本过长：超过 1000 字会导致生成失败或超时
- ❌ 特殊符号：`<>{}` 等符号可能被错误解析，建议使用全角符号
- ❌ 输出路径：确保 `~/.openclaw/media/` 目录存在且 OpenClaw 有写入权限
- ❌ 音调过高：超过 +10Hz 会明显失真，建议控制在 ±5Hz 范围内

**性能优化：**
- 临时文件建议在发送后立即清理，避免磁盘空间累积
- 批量生成时建议用异步脚本，避免阻塞主流程
- 缓存常用文本的语音文件，减少重复生成

**跨渠道适配：**
- **飞书**：支持 opus/mp3/wav，推荐 opus（体积小质量好）
- **Telegram**：支持 ogg/wav，推荐 ogg/opus
- **Discord**：支持多种格式，推荐 mp3（兼容性最好）
