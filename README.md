# ai-skills-zh

## 高质量 AI 技能集合

支持所有 Agent 平台的中文技能集合，提升对话效率和工作体验。

## 📦 技能列表

### [voice-tts](./voice-tts/)
使用 edge-tts 生成高质量中文语音消息并发送。支持多种中文声音（男声/女声/方言），可调节语速音调，适用于飞书/Telegram/Discord 等渠道。

**安装（推荐 - 使用 OpenSkills）：**
```bash
# 先安装 OpenSkills CLI（如未安装）
npm install -g openskills

# 安装单个技能
npx openskills install binbin1213/ai-skills-zh#voice-tts
```

### [更多技能]
（待添加）

## 🚀 快速安装

### 方式 1：使用 OpenSkills（推荐，通用）

OpenSkills 支持所有 AI agent（Claude Code、Cursor、Windsurf 等）。

```bash
# 安装 OpenSkills CLI（如未安装）
npm install -g openskills

# 安装单个技能
npx openskills install binbin1213/ai-skills-zh#voice-tts

# 安装所有技能
npx openskills install binbin1213/ai-skills-zh
```

### 方式 2：Claude Code Marketplace（仅 Claude Code）

在 Claude Code 中运行：

```
/plugin marketplace add anthropics/skills
```

然后选择 `anthropic-agent-skills` 并找到 `voice-tts`。

### 方式 3：手动安装（通用）

```bash
# 克隆仓库到本地
git clone https://github.com/binbin1213/ai-skills-zh.git
cd ai-skills-zh

# 手动复制技能到 Claude skills 目录
mkdir -p ~/.claude/skills
cp -r voice-tts ~/.claude/skills/
```

## 📖 使用说明

### 前置要求
- 已安装 AI Agent（Claude/GPT 等）
- 已安装 Node.js（用于 OpenSkills）

### 安装 OpenSkills（推荐，通用）

OpenSkills 是通用的 skills 加载器，适用于 Claude Code、Cursor、Windsurf 等所有 AI agent。

```bash
# 安装 OpenSkills CLI
npm install -g openskills
```

### 验证安装
```bash
# 检查技能是否安装成功
ls ~/.claude/skills/voice-tts

# 在 AI Agent 中测试技能
# 输入：帮我用语音说"你好"
```

## 🤝 贡献指南

欢迎贡献新技能或改进现有技能！

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)

## 📄 License

MIT License - 详见 [LICENSE](./LICENSE)

## 🔗 相关资源

- [Anthropic Skills Development Guide](https://docs.anthropic.com/claude/docs/skills)
- [Anthropic Skills 官方仓库](https://github.com/anthropics/skills)
- [OpenSkills - Universal Skills Loader](https://github.com/numman-ali/openskills)

---

**⭐ 如果这个仓库对你有帮助，请给个 Star！**
