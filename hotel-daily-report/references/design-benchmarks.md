# 结构化设计借鉴 — PM Skills Marketplace

> 2026-06-10 对比 phuryn/pm-skills 项目后记录。
> 目的：指导酒店技能 SKILL.md 的迭代方向。

## PM Skills 的结构特点

### 三段式结构（推荐参考）
```
## Purpose         ← 这个技能干什么
## Context         ← 背景信息
## Instructions    ← 逐步操作指南
```

### 参数化输入
```
## Input Arguments
- `$ARGUMENTS`: 用户输入的原始参数
- `$RESUME`: （可选）附件内容
```

### 强/弱示例对比
每个最佳实践分 Evaluation（评估什么）和 Guidance（怎么做），附 weak / strong 对比示例。

## 我们已做得好的部分
- ✅ 场景组合建议（日常型/业务型/暖心型/应急型/雨天型）
- ✅ 场景素材库（80个场景，8大类，编号体系）
- ✅ 门店信息集中管理（zhengzhou-store.md）
- ✅ 语气范文（voice-samples.md）
- ✅ 近期生成去重（recent-log.md）

## 待改进项

### 1. 给每个场景补 weak/strong 示例
每个场景（A1-A12 等 80 个）补上：
- weak 示例：什么写法会被判定为不合格（如太正式、像AI、编造设施）
- strong 示例：一个简短的合格写法片段

### 2. 考虑增加 Purpose/Context 段落
在 SKILL.md 头部增加：
- Purpose: 这段文字做什么
- Context: 适用于什么岗位、什么场景
- Input: 需要用户提供什么信息

### 3. 不推荐的改进（不需要做）
- ❌ 不需要拆成多个小技能（场景量太大，拆了反而难维护）
- ❌ 不需要引入命令系统（/discover 这种 slash command 对微信场景无意义）