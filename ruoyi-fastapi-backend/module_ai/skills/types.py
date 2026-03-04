"""
AI 技能系统类型定义

本模块定义了技能系统的核心数据类型，包括技能元数据、技能对象和执行结果。
参考 OpenClaw 的 TypeScript 实现进行 Python 移植。
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal


@dataclass
class SkillInstallSpec:
    """技能安装规范"""

    kind: Literal['brew', 'node', 'go', 'uv', 'download']
    id: str | None = None
    label: str | None = None
    bins: list[str] | None = None
    os: list[str] | None = None
    formula: str | None = None
    package: str | None = None
    module: str | None = None
    url: str | None = None
    archive: str | None = None
    extract: bool | None = None
    strip_components: int | None = None
    target_dir: str | None = None


@dataclass
class SkillRequirements:
    """技能依赖要求"""

    bins: list[str] | None = None
    any_bins: list[str] | None = None
    env: list[str] | None = None
    config: list[str] | None = None


@dataclass
class SkillMetadata:
    """
    技能元数据

    包含技能的配置信息、依赖要求、安装规范等。
    对应 OpenClaw 的 OpenClawSkillMetadata 类型。
    """

    always: bool = False
    skill_key: str | None = None
    primary_env: str | None = None
    emoji: str | None = None
    homepage: str | None = None
    os: list[str] | None = None
    requires: SkillRequirements | None = None
    install: list[SkillInstallSpec] | None = None


@dataclass
class SkillInvocationPolicy:
    """技能调用策略"""

    user_invocable: bool = True
    disable_model_invocation: bool = False


@dataclass
class Skill:
    """
    技能对象

    表示一个完整的技能，包含名称、描述、内容、文件路径等信息。
    对应 OpenClaw 的 Skill 类型（来自 @mariozechner/pi-coding-agent）。
    """

    name: str
    description: str
    content: str
    file_path: str
    base_dir: str
    source: str = 'unknown'
    frontmatter: dict[str, Any] = field(default_factory=dict)
    metadata: SkillMetadata = field(default_factory=SkillMetadata)
    invocation: SkillInvocationPolicy = field(default_factory=SkillInvocationPolicy)

    # 运行时状态
    enabled: bool = True
    last_used: datetime | None = None
    use_count: int = 0


@dataclass
class SkillResult:
    """
    技能执行结果

    包含执行成功状态、输出内容、错误信息和执行时长。
    """

    success: bool
    output: str
    error: str | None = None
    duration_ms: int = 0
    metadata: dict[str, Any] | None = None


@dataclass
class SkillEligibilityContext:
    """
    技能资格上下文

    用于在远程环境中检查技能是否可用。
    """

    remote: dict[str, Any] | None = None


@dataclass
class SkillSnapshot:
    """
    技能快照

    包含技能 Prompt、技能列表和过滤器配置。
    用于缓存和序列化技能状态。
    """

    prompt: str
    skills: list[dict[str, Any]]
    skill_filter: list[str] | None = None
    resolved_skills: list[Skill] | None = None
    version: int | None = None


@dataclass
class SkillCommandSpec:
    """
    技能命令规范

    用于定义技能的命令行接口。
    """

    name: str
    skill_name: str
    description: str
    dispatch: dict[str, Any] | None = None
