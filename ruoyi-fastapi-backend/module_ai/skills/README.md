# AI 技能系统

这是宥辰开发平台(YouChen-FastAPI)项目的 AI 技能系统，参考 OpenClaw 的 Skills 实现。

## 目录结构

```
skills/
├── __init__.py           # 模块初始化
├── types.py              # 类型定义
├── loader.py             # 技能加载器
├── filter.py             # 技能过滤器
├── executor.py           # 技能执行器
├── bundled/              # 内置技能
│   ├── echo/             # 回显技能（测试）
│   ├── weather/          # 天气查询技能
│   └── summarize/        # 文本摘要技能
└── README.md             # 本文件
```

## 核心模块

### types.py - 类型定义

定义了技能系统的核心数据类型：

- `Skill`: 技能对象
- `SkillMetadata`: 技能元数据
- `SkillResult`: 技能执行结果
- `SkillRequirements`: 技能依赖要求
- `SkillInstallSpec`: 技能安装规范
- `SkillInvocationPolicy`: 技能调用策略

### loader.py - 技能加载器

负责从文件系统加载技能：

- 扫描技能目录
- 解析 SKILL.md 文件
- 解析 YAML frontmatter
- 构建 Skill 对象
- 支持嵌套目录检测
- 文件大小和数量限制

### filter.py - 技能过滤器

根据条件过滤技能：

- 依赖检查（bins, env）
- 操作系统兼容性检查
- 用户配置过滤
- 调用策略过滤

### executor.py - 技能执行器

执行技能命令：

- 异步 bash 命令执行
- 超时控制
- 参数替换和转义
- 错误处理

## 使用示例

### 加载技能

```python
from module_ai.skills.loader import SkillLoader

loader = SkillLoader([
    '~/.youchen-fastapi/skills',
    './module_ai/skills/bundled',
])
skills = loader.load_all_skills()
```

### 过滤技能

```python
from module_ai.skills.filter import SkillFilter

filter_engine = SkillFilter()
available_skills = filter_engine.filter_skills(
    skills,
    user_config={'enabled_skills': ['weather', 'echo']},
)
```

### 执行技能

```python
from module_ai.skills.executor import SkillExecutor

executor = SkillExecutor(timeout=30)
result = await executor.execute_skill(
    skill,
    command='curl "wttr.in/London?format=3"',
)
print(result.output)
```

### 服务层使用

```python
from module_ai.service.ai_skill_service import AiSkillService

# 加载可用技能
skills = await AiSkillService.load_available_skills(user_id, query_db)

# 格式化为 Prompt
prompt = AiSkillService.format_skills_for_prompt(skills)

# 执行技能
result = await AiSkillService.execute_skill(skill, command, args)
```

## 内置技能

### echo - 回显技能

测试技能，回显输入的消息。

- **依赖**: 无
- **用途**: 测试技能系统

### weather - 天气查询

使用 wttr.in 服务查询天气。

- **依赖**: curl
- **用途**: 查询任意地点的天气信息

### summarize - 文本摘要

总结文本内容。

- **依赖**: 无
- **用途**: 提取文本的关键信息

## 添加新技能

1. 在 `bundled/` 目录下创建技能目录
2. 创建 `SKILL.md` 文件
3. 按照格式编写技能描述和元数据

示例：

```markdown
---
name: my-skill
description: My skill description
metadata:
  openclaw:
    emoji: 🎯
    requires:
      bins:
        - curl
---

# My Skill

Description...
```

## 配置

在 `config/env.py` 中的 `SkillSettings` 类配置：

```python
class SkillSettings(BaseSettings):
    skill_dirs: str = '~/.youchen-fastapi/skills,./module_ai/skills/bundled'
    skill_max_skills_in_prompt: int = 150
    skill_max_skills_prompt_chars: int = 30000
    skill_execution_timeout: int = 30
    # ...
```

## 技术参考

- OpenClaw Skills: https://github.com/openclaw/openclaw
- pi-coding-agent: https://github.com/mariozechner/pi-coding-agent
- Agno Framework: https://github.com/agno-ai/agno

## 开发状态

- ✅ 核心基础设施（MVP）
- ⏳ 工具集成（将技能包装为 Agno Tools）
- ⏳ 单元测试
- ⏳ 技能缓存
- ⏳ 使用统计
- ⏳ 管理 API

## 贡献

欢迎贡献新的技能或改进现有功能！
