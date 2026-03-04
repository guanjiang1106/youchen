# AI 技能系统快速开始

## 简介

AI 技能系统允许 AI Agent 访问和使用各种技能来完成任务。技能可以是命令行工具、API 调用或其他可执行的功能。

## 功能特性

- 🔍 自动发现和加载技能
- 🎯 智能过滤（依赖检查、操作系统兼容性）
- 📝 技能描述注入到 AI 提示词
- 🤖 **AI 自动执行技能**（新）
- ⚡ 异步执行，不阻塞对话
- ⚙️ 灵活的配置选项
- 🔒 安全的命令执行

## 快速开始

### 1. 安装依赖

```bash
cd youchen-fastapi-backend
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python server.py
```

### 3. 使用技能

1. 登录系统
2. 进入 AI 对话页面
3. 发送消息，AI 会自动加载可用技能
4. **AI 会根据你的问题自动选择和执行技能**

**示例对话**：

```
用户：北京的天气怎么样？
AI：让我帮你查询北京的天气...
    [自动调用 weather 技能]
    北京目前的天气是晴天，温度 15°C

用户：帮我总结一下这段文字：[长文本]
AI：好的，让我为你总结...
    [自动调用 summarize 技能]
    主要内容包括：1. ... 2. ... 3. ...
```

**完全自动化，无需手动操作！**

## 内置技能

系统自带以下技能：

### 🔊 Echo
- **描述**: 回显消息（测试技能）
- **用途**: 测试技能系统是否正常工作

### 🌤️ Weather
- **描述**: 获取天气信息
- **依赖**: curl
- **用途**: 查询任意地点的天气

### 📝 Summarize
- **描述**: 文本摘要
- **用途**: 总结长文本内容

## 添加自定义技能

### 1. 创建技能目录

```bash
mkdir -p ~/.youchen-fastapi/skills/my-skill
```

### 2. 创建 SKILL.md 文件

```bash
cat > ~/.youchen-fastapi/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: My custom skill description
metadata:
  openclaw:
    emoji: 🎯
    requires:
      bins:
        - curl
---

# My Skill

Detailed description of what this skill does...

## Usage

How to use this skill...

## Example

```bash
curl "https://api.example.com/{param}"
```
EOF
```

### 3. 重启服务

```bash
# 重启后端服务
python server.py
```

## 技能格式说明

### SKILL.md 结构

```markdown
---
name: skill-name
description: Short description
homepage: https://example.com
metadata:
  openclaw:
    emoji: 🎯
    primaryEnv: API_KEY
    requires:
      bins:
        - command1
        - command2
      env:
        - ENV_VAR1
    os:
      - linux
      - darwin
---

# Skill Title

Detailed description...

## Usage

Usage instructions...

## Example

Example code...
```

### 元数据字段说明

- `name`: 技能名称（必填）
- `description`: 简短描述（必填）
- `homepage`: 技能主页（可选）
- `metadata.openclaw.emoji`: 技能图标（可选）
- `metadata.openclaw.primaryEnv`: 主要环境变量（可选）
- `metadata.openclaw.requires.bins`: 需要的命令（可选）
- `metadata.openclaw.requires.env`: 需要的环境变量（可选）
- `metadata.openclaw.os`: 支持的操作系统（可选）

## 配置选项

在 `.env.*` 文件中配置：

```bash
# 技能目录（多个用逗号分隔）
SKILL_DIRS=~/.youchen-fastapi/skills,./module_ai/skills/bundled

# 技能限制
SKILL_MAX_SKILLS_IN_PROMPT=150
SKILL_MAX_SKILLS_PROMPT_CHARS=30000
SKILL_MAX_SKILL_FILE_BYTES=256000

# 执行配置
SKILL_EXECUTION_TIMEOUT=30

# 缓存配置
SKILL_CACHE_ENABLED=true
SKILL_CACHE_TTL=3600
```

## 技能目录优先级

技能从以下目录加载（优先级从低到高）：

1. 内置技能：`./module_ai/skills/bundled`
2. 用户技能：`~/.youchen-fastapi/skills`

后加载的技能会覆盖先加载的同名技能。

## 故障排除

### 技能未加载

1. 检查技能目录是否存在
2. 检查 SKILL.md 文件格式是否正确
3. 查看日志文件：`logs/app.log`

### 技能被过滤

技能可能因以下原因被过滤：

1. 缺少依赖命令（bins）
2. 缺少环境变量（env）
3. 操作系统不兼容
4. 文件大小超过限制

查看日志了解详细原因：

```bash
tail -f logs/app.log | grep "Skill.*filtered"
```

### 技能 Prompt 过长

如果技能数量过多，Prompt 可能被截断。可以：

1. 减少技能数量
2. 增加 `SKILL_MAX_SKILLS_PROMPT_CHARS` 配置
3. 禁用不需要的技能

## 最佳实践

1. **技能命名**: 使用小写字母和连字符，如 `my-skill`
2. **描述清晰**: 提供清晰的技能描述，帮助 AI 理解何时使用
3. **依赖声明**: 明确声明所需的命令和环境变量
4. **测试技能**: 创建技能后先手动测试命令是否正常
5. **文档完整**: 在 SKILL.md 中提供详细的使用说明和示例

## 示例：创建 GitHub 技能

```bash
# 1. 创建目录
mkdir -p ~/.youchen-fastapi/skills/github

# 2. 创建 SKILL.md
cat > ~/.youchen-fastapi/skills/github/SKILL.md << 'EOF'
---
name: github
description: Search GitHub repositories
homepage: https://github.com
metadata:
  openclaw:
    emoji: 🐙
    requires:
      bins:
        - curl
      env:
        - GITHUB_TOKEN
---

# GitHub Skill

Search and explore GitHub repositories.

## Usage

Search for repositories:

```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/search/repositories?q={query}"
```

## Example

Search for Python projects:

```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/search/repositories?q=language:python"
```
EOF

# 3. 设置环境变量
export GITHUB_TOKEN=your_token_here

# 4. 重启服务
```

## 下一步

- 查看 [技能开发文档](./SKILLS_DEVELOPMENT.md)（待编写）
- 查看 [API 文档](http://localhost:9099/docs)
- 加入社区讨论

## 常见问题

### Q: 技能会自动执行吗？

A: **是的！** AI 会根据你的问题自动选择和执行合适的技能。你只需要正常对话，AI 会在需要时自动调用技能。

### Q: 如何禁用某个技能？

A: 目前需要从技能目录中删除或重命名 SKILL.md 文件。未来版本会提供配置界面。

### Q: 技能支持哪些类型？

A: 目前主要支持 bash 命令。未来会支持 Python 函数和 HTTP API。

### Q: 技能执行是否安全？

A: 技能执行有超时控制和基本的参数转义，但建议只使用可信的技能。未来会添加沙箱隔离。

### Q: AI 如何知道何时使用技能？

A: AI 会根据技能的描述和你的问题自动判断。技能描述越清晰，AI 的判断就越准确。

### Q: 技能执行失败会怎样？

A: 如果技能执行失败，AI 会收到错误信息并告知你。对话不会中断。

## 反馈和贡献

如有问题或建议，请提交 Issue 或 Pull Request。
