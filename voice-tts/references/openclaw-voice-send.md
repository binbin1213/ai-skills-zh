## **一、通过智能体工具发送**

### **1. 使用 `message` 工具**

```
{
  "action": "send",
  "channel": "feishu",
  "to": "user_id",  // 或 chat_id
  "media": "/path/to/voice.opus",
  "message": "这是语音消息"
}
```

### **2. 指定音频类型**

```
{
  "action": "send",
  "channel": "feishu",
  "to": "user_id",
  "media": "/path/to/voice.opus",
  "msg_type": "audio"  // 关键：指定为音频类型
}
```

## **二、通过 CLI 命令发送**

### **1. 基本命令**

```
# 发送语音文件
openclaw message send --channel feishu \
  --target "user:<user_id>" \
  --media /path/to/voice.opus

# 带标题的语音
openclaw message send --channel feishu \
  --target "chat:<chat_id>" \
  --media /path/to/voice.opus \
  --message "请听语音说明"
```

### **2. 指定为语音消息**

```
# 使用 --as-voice 参数
openclaw message send --channel feishu \
  --target "user:<user_id>" \
  --media /path/to/voice.opus \
  --as-voice
```

## **三、飞书特定的语音消息规则**

### **1. 支持的音频格式**

根据 `CHANGELOG.md` 文档：

- **.opus**：自动使用 `msg_type: "audio"`，作为语音消息发送
- **.mp3**：作为普通媒体文件发送（除非指定为音频）
- **.mp4**：使用 `msg_type: "media"`（视频）
- 其他文档：使用 `msg_type: "file"`

### **2. 自动类型检测**

飞书插件会自动检测文件类型：

- `.opus` → `msg_type: "audio"`（语音消息）
- `.mp4` → `msg_type: "media"`（视频）
- 其他 → `msg_type: "file"`（文件）

## **四、通过 TTS 生成语音发送**

### **1. 使用 TTS 工具**

```
{
  "action": "tts",
  "text": "这是一段语音消息",
  "provider": "elevenlabs",
  "voiceId": "pMsXgVXv3BLzUgSXRplE"
}
```

工具返回 `MEDIA:<path>`，然后可以发送给飞书。

### **2. 结合消息发送**

```
# 生成 TTS 音频
openclaw tts convert --text "你好，这是语音消息" --output voice.opus

# 发送到飞书
openclaw message send --channel feishu \
  --target "user:<user_id>" \
  --media voice.opus
```

## **五、在智能体回复中包含语音**

### **1. 回复中添加 MEDIA: 指令**

智能体在回复中单独一行包含：

```
这是文本回复。
MEDIA:/path/to/voice.opus
```

### **2. 使用语音指令标签**

```
{ "voice": "voice_id", "once": true }
这是一段需要转为语音的文本。
```

## **六、配置飞书语音消息**

### **1. 飞书插件配置**

```
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "your_app_id",
      "appSecret": "your_app_secret",
      "media": {
        "audioAsVoice": true,  // 自动将音频作为语音消息
        "maxSizeMb": 100
      }
    }
  }
}
```

### **2. 消息类型覆盖配置**

```
{
  "channels": {
    "feishu": {
      "msgTypeOverrides": {
        ".opus": "audio",
        ".mp3": "audio",
        ".m4a": "audio",
        ".mp4": "media",
        ".pdf": "file"
      }
    }
  }
}
```

## **七、完整工作流示例**

### **场景：发送会议录音**

```
# 1. 录制或获取语音文件
recording.opus

# 2. 发送给飞书用户
openclaw message send --channel feishu \
  --target "user:ou_123456" \
  --media recording.opus \
  --message "会议录音请查收"

# 3. 或发送到群组
openclaw message send --channel feishu \
  --target "chat:oc_123456" \
  --media recording.opus \
  --as-voice
```

### **场景：TTS 通知**

```
# 1. 创建 TTS 通知
openclaw tts convert \
  --text "下午三点有团队会议，请准时参加" \
  --provider edge \
  --output meeting-notice.opus

# 2. 发送到飞书群
openclaw message send --channel feishu \
  --target "chat:oc_789012" \
  --media meeting-notice.opus \
  --as-voice
```

## **八、故障排除**

### **问题 1：语音未作为消息发送**

```
# 检查文件类型
file voice.opus

# 强制指定类型
openclaw message send --channel feishu \
  --target "user:<id>" \
  --media voice.opus \
  --msg-type audio
```

### **问题 2：文件大小限制**

```
# 压缩音频
ffmpeg -i input.mp3 -c:a libopus -b:a 64k output.opus

# 检查配置限制
openclaw config get channels.feishu.media.maxSizeMb
```

### **问题 3：权限问题**

```
# 检查飞书机器人权限
openclaw channels status --channel feishu

# 验证媒体上传权限
openclaw channels test --channel feishu --test media
```

## **九、最佳实践**

### **1. 语音格式选择**

- **推荐**：`.opus` 格式，飞书原生支持为语音消息
- **兼容性**：`.mp3` 格式，但可能被视为普通文件
- **避免**：`.wav` 等未压缩格式，文件过大

### **2. 文件命名规范**

```
voice_YYYYMMDD_HHMM.opus
会议录音_20240315_1500.opus
```

### **3. 发送前预览**

```
# 先发送给自己测试
openclaw message send --channel feishu \
  --target "user:<your_id>" \
  --media voice.opus \
  --dry-run
```

## **十、API 直接调用**

### **使用飞书 SDK**

```
// 通过 OpenClaw 的飞书插件底层 API
const response = await client.im.message.create({
  receive_id: "user_id",
  msg_type: "audio",
  content: JSON.stringify({
    file_key: "audio_file_key"
  })
});
```

**总结**：在飞书会话中发送语音文件给用户：

1. **最简单命令**：

   ```
   openclaw message send --channel feishu --target user:<id> --media voice.opus
   ```

2. **确保语音消息**：使用 `.opus` 格式或添加 `--as-voice` 参数

3. **智能体集成**：在回复中使用 `MEDIA:` 指令或 `tts` 工具

4. **配置优化**：设置 `msgTypeOverrides` 确保音频正确识别

飞书对 `.opus` 格式有最好的语音消息支持，建议优先使用该格式。