# ai-skills-zh

## 高质量 AI Agent 对话技能集合

针对 OpenClaw 等 AI Agent 对话平台（支持语音、消息）的中文技能集合，提升对话效率和工作体验。

---

## 📦 技能列表

### [voice-tts](./voice-tts/)
使用 edge-tts 生成高质量中文语音消息并发送。支持多种中文声音（男声/女声/方言），可调节语速音调，适用于飞书/Telegram/Discord 等渠道。

**适用平台：**
- ✅ **OpenClaw**（推荐）- 完全支持语音对话
- ✅ Claude Code - 基础功能
- ✅ 其他支持 SKILL.md 格式的 Agent

---

## 🚀 快速安装

### 针对 OpenClaw 用户（推荐）

OpenClaw 是一个 **AI Agent 对话平台**，支持语音消息、多平台集成等功能。

#### 方式 1：通过 ClawHub 安装（最简单）

```bash
# 安装 ClawHub CLI（如未安装）
npm i -g clawdhub

# 从 ClawHub 搜索并安装技能
clawdhub install voice-tts
```

#### 方式 2：通过 GitHub 仓库链接

在 OpenClaw 对话中直接发送：
```
请安装这个技能：https://github.com/binbin1213/ai-skills-zh/tree/main/voice-tts
```
OpenClaw 会自动处理安装。

#### 方式 3：手动安装（高级用户）

```bash
# 克隆技能到 OpenClaw 目录
git clone https://github.com/binbin1213/ai-skills-zh.git ~/.openclaw/skills/voice-tts
```

---

### 针对 Claude Code / Cursor / Windsurf 用户

OpenSkills 是通用的技能加载器，适用于所有 AI agent。

#### 方式 1：使用 OpenSkills（推荐，通用）

OpenSkills 支持所有 AI agent（Claude Code、Cursor、Windsurf 等）。

```bash
# 安装 OpenSkills CLI（如未安装）
npm install -g openskills

# 安装单个技能
npx openskills install binbin1213/ai-skills-zh#voice-tts

# 安装所有技能
npx openskills install binbin1213/ai-skills-zh
```

#### 方式 2：Claude Code Marketplace（仅 Claude Code）

在 Claude Code 中运行：

```
/plugin marketplace add anthropics/skills
```

然后选择 `anthropic-agent-skills` 并找到 `voice-tts`。

#### 方式 3：手动安装（通用）

```bash
# 克隆仓库到本地
git clone https://github.com/binbin1213/ai-skills-zh.git
cd ai-skills-zh

# 手动复制技能到 Claude skills 目录
mkdir -p ~/.claude/skills
cp -r voice-tts ~/.claude/skills/
```

---

## 📖 使用说明

### 针对 OpenClaw

OpenClaw 技能使用与 Claude 相同的 SKILL.md 格式。

```bash
# 验证安装
ls ~/.openclaw/skills/voice-tts

# 在 OpenClaw 中测试
# 输入：帮我用语音说"你好"
```

### 针对 Claude Code / OpenSkills

```bash
# 检查技能是否安装成功
ls ~/.claude/skills/voice-tts

# 在 AI Agent 中测试技能
# 输入：帮我用语音说"你好"
```

---

## 🤝 贡献指南

欢迎贡献新技能或改进现有技能！

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## 📄 License

MIT License - 详见 [LICENSE](./LICENSE)

---

## 🔗 相关资源

### 官方资源
- [Anthropic Skills Development Guide](https://docs.anthropic.com/claude/docs/skills)
- [Anthropic Skills 官方仓库](https://github.com/anthropics/skills)

### 工具和平台
- **OpenClaw** - AI Agent 对话平台（支持语音）
  - 官网：https://openclaw.ai
  - ClawHub：https://github.com/openclaw/clawhub
  - 安装：`clawdhub install skill-name`
- **OpenSkills** - 通用技能加载器
  - 仓库：https://github.com/numman-ali/openskills
  - 安装：`npx openskills install repo#skill`

### 技能格式
所有技能使用统一的 SKILL.md 格式（Anthropic Agent Skills 规范），确保在不同平台间兼容。

---

**⭐ 如果这个仓库对你有帮助，请给个 Star！**
