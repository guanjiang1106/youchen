"""
AI 技能服务层

本模块提供技能管理的业务逻辑，包括加载、过滤、格式化和执行技能。
参考 OpenClaw 的 workspace.ts 实现。
"""

import os
from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from module_ai.skills.executor import SkillExecutor
from module_ai.skills.filter import SkillFilter
from module_ai.skills.loader import SkillLoader
from module_ai.skills.types import Skill, SkillResult
from utils.log_util import logger


class AiSkillService:
    """AI 技能服务层"""

    # 默认限制
    DEFAULT_MAX_SKILLS_IN_PROMPT = 150
    DEFAULT_MAX_SKILLS_PROMPT_CHARS = 30000

    @classmethod
    async def load_available_skills(
        cls,
        user_id: int,
        query_db: AsyncSession | None = None,
        skill_filter: list[str] | None = None,
    ) -> list[Skill]:
        """
        加载用户可用的技能

        :param user_id: 用户ID
        :param query_db: 数据库会话（可选，用于获取用户配置）
        :param skill_filter: 技能名称过滤列表（可选）
        :return: 可用技能列表
        """
        # 1. 获取技能目录
        skills_dirs = cls._get_skills_dirs()

        # 2. 加载所有技能
        loader = SkillLoader(skills_dirs)
        all_skills = loader.load_all_skills()

        logger.info(f'Loaded {len(all_skills)} skills from {len(skills_dirs)} directories')

        # 3. 获取用户配置（如果提供了数据库会话）
        user_config = None
        if query_db:
            user_config = await cls._get_user_skill_config(user_id, query_db)

        # 4. 过滤技能
        filter_engine = SkillFilter()

        # 应用技能名称过滤
        if skill_filter:
            normalized_filter = filter_engine.normalize_skill_filter(skill_filter)
            if normalized_filter:
                all_skills = [s for s in all_skills if s.name in normalized_filter]
                logger.debug(f'Applied skill filter: {normalized_filter}')

        available_skills = filter_engine.filter_skills(
            all_skills,
            user_config=user_config,
        )

        logger.info(f'Filtered to {len(available_skills)} available skills for user {user_id}')

        return available_skills

    @classmethod
    def format_skills_for_prompt(
        cls,
        skills: list[Skill],
        max_skills: int | None = None,
        max_chars: int | None = None,
    ) -> str:
        """
        将技能列表格式化为 Prompt（OpenClaw 方式：包含完整的 SKILL.md 内容）

        :param skills: 技能列表
        :param max_skills: 最大技能数量
        :param max_chars: 最大字符数
        :return: 格式化的 Prompt 字符串
        """
        if not skills:
            return ''

        max_skills = max_skills or cls.DEFAULT_MAX_SKILLS_IN_PROMPT
        max_chars = max_chars or cls.DEFAULT_MAX_SKILLS_PROMPT_CHARS

        # 限制技能数量
        limited_skills = skills[:max_skills]

        # 构建 Prompt - 包含完整的技能内容
        lines = ['# Available Skills\n']
        lines.append('You have access to the following skills:\n')

        for skill in limited_skills:
            # 压缩路径
            file_path = cls._compact_path(skill.file_path)

            # 添加技能标题和元数据
            lines.append(f'## {skill.name}')
            if skill.metadata.emoji:
                lines[-1] += f' {skill.metadata.emoji}'
            lines.append(f'**File:** {file_path}')
            
            # 添加依赖信息
            if skill.metadata.requires:
                bins = skill.metadata.requires.bins
                if bins:
                    lines.append(f'**Requires:** {", ".join(bins)}')

            # 添加主要环境变量
            if skill.metadata.primary_env:
                lines.append(f'**Primary Env:** {skill.metadata.primary_env}')

            lines.append('')
            
            # === 关键修改：包含完整的技能内容 ===
            # 移除 frontmatter（已经在元数据中显示）
            content = skill.content
            if content.startswith('---'):
                # 跳过 frontmatter
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    content = parts[2].strip()
            
            lines.append(content)
            lines.append('')  # 技能之间的分隔

        prompt = '\n'.join(lines)

        # 截断过长的 Prompt
        if len(prompt) > max_chars:
            # 二分查找最大可包含的技能数量
            lo = 0
            hi = len(limited_skills)
            while lo < hi:
                mid = (lo + hi + 1) // 2
                test_prompt = cls._build_full_prompt(limited_skills[:mid])
                if len(test_prompt) <= max_chars:
                    lo = mid
                else:
                    hi = mid - 1

            # 使用找到的最大数量重新构建 Prompt
            if lo > 0:
                prompt = cls._build_full_prompt(limited_skills[:lo])
                prompt += f'\n\n(Skills list truncated: showing {lo} of {len(skills)} skills)'
            else:
                prompt = '# Available Skills\n\n(Skills list too large to display)'

        return prompt

    @classmethod
    def _build_full_prompt(cls, skills: list[Skill]) -> str:
        """
        构建包含完整技能内容的提示词

        :param skills: 技能列表
        :return: 完整提示词
        """
        lines = ['# Available Skills\n']
        lines.append('You have access to the following skills:\n')

        for skill in skills:
            file_path = cls._compact_path(skill.file_path)
            lines.append(f'## {skill.name}')
            if skill.metadata.emoji:
                lines[-1] += f' {skill.metadata.emoji}'
            lines.append(f'**File:** {file_path}')
            if skill.metadata.requires and skill.metadata.requires.bins:
                lines.append(f'**Requires:** {", ".join(skill.metadata.requires.bins)}')
            if skill.metadata.primary_env:
                lines.append(f'**Primary Env:** {skill.metadata.primary_env}')
            lines.append('')
            
            # 包含完整内容（移除 frontmatter）
            content = skill.content
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    content = parts[2].strip()
            lines.append(content)
            lines.append('')

        return '\n'.join(lines)

    @classmethod
    def _build_prompt_lines(cls, skills: list[Skill]) -> list[str]:
        """
        构建 Prompt 行列表（已废弃，使用 _build_full_prompt 代替）

        :param skills: 技能列表
        :return: Prompt 行列表
        """
        # 为了向后兼容保留此方法，但直接返回完整提示词的行
        return cls._build_full_prompt(skills).split('\n')

    @classmethod
    def create_skill_tools(cls, skills: list[Skill], timeout: int = 30) -> list:
        """
        创建技能工具（Agno Tools）
        
        注意：根据 OpenClaw 的设计，技能不应该被包装为独立的工具。
        技能说明应该注入到系统提示词中，AI 通过通用的 exec 工具来执行命令。
        
        此方法保留用于向后兼容，但返回空列表。

        :param skills: 技能列表
        :param timeout: 执行超时时间（秒）
        :return: 空列表（技能通过 exec 工具执行）
        """
        # OpenClaw 方式：不包装技能为工具，而是通过 exec 工具执行
        # 技能说明已经注入到系统提示词中，AI 会读取并决定执行什么命令
        logger.info(f'Skills are available via exec tools, not as individual tool wrappers')
        return []

    @classmethod
    def _extract_command_from_skill(cls, skill: Skill) -> str | None:
        """
        从技能内容中提取命令模板

        :param skill: 技能对象
        :return: 命令模板字符串，如果未找到则返回 None
        """
        import re
        
        # 从 SKILL.md 内容中提取代码块中的命令
        content = skill.content
        
        # 1. 优先查找 bash/sh 代码块
        pattern = r'```(?:bash|sh)\n(.*?)\n```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        if matches:
            # 过滤掉不适合作为技能命令的代码块
            for match in matches:
                command = match.strip()
                
                # 跳过多行命令块（通常是示例或配置）
                lines = command.split('\n')
                non_comment_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
                
                # 如果只有一行有效命令，或者命令包含参数占位符 {param}，则认为是技能命令
                if len(non_comment_lines) == 1 or '{' in command:
                    # 移除注释行
                    clean_lines = [line for line in lines if not line.strip().startswith('#')]
                    return '\n'.join(clean_lines).strip()
            
            # 如果没有找到单行命令，尝试从第一个代码块中提取第一行简单命令
            if matches:
                first_block = matches[0].strip()
                lines = [line.strip() for line in first_block.split('\n') if line.strip() and not line.strip().startswith('#')]
                if lines:
                    # 取第一行非注释命令
                    first_cmd = lines[0]
                    # 如果是简单命令（不超过100字符），返回它
                    if len(first_cmd) <= 100:
                        return first_cmd
        
        # 2. 如果没有 bash 代码块，但技能需要特定的 CLI 工具，生成默认命令
        if skill.metadata.requires:
            bins = skill.metadata.requires.bins or skill.metadata.requires.any_bins
            if bins and len(bins) >= 1:
                # 单个或多个 CLI 工具，生成帮助命令
                cli_name = bins[0]
                # 排除一些通用工具
                if cli_name not in ['curl', 'git', 'jq', 'python', 'node', 'npm']:
                    return f'{cli_name} --help'
        
        return None

    @classmethod
    def _extract_parameters_from_command(cls, command: str) -> list[str]:
        """
        从命令模板中提取参数

        :param command: 命令模板
        :return: 参数名称列表
        """
        import re
        
        # 查找 {param} 格式的参数
        pattern = r'\{(\w+)\}'
        params = re.findall(pattern, command)
        
        return list(set(params))  # 去重

    @classmethod
    async def execute_skill(
        cls,
        skill: Skill,
        command: str,
        args: dict[str, Any] | None = None,
        timeout: int = 30,
    ) -> SkillResult:
        """
        执行技能

        :param skill: 技能对象
        :param command: 要执行的命令
        :param args: 命令参数
        :param timeout: 超时时间（秒）
        :return: 执行结果
        """
        executor = SkillExecutor(timeout=timeout)
        result = await executor.execute_skill(skill, command, args)

        # 更新技能使用统计
        skill.use_count += 1
        from datetime import datetime

        skill.last_used = datetime.now()

        return result

    @classmethod
    def _get_skills_dirs(cls) -> list[str]:
        """
        获取技能目录列表

        优先级（从低到高）：
        1. 内置技能目录
        2. 用户技能目录

        :return: 技能目录路径列表
        """
        home = Path.home()
        bundled_dir = Path(__file__).parent.parent / 'skills' / 'bundled'

        return [
            str(bundled_dir),  # 内置技能
            str(home / '.ruoyi-fastapi' / 'skills'),  # 用户技能
        ]

    @classmethod
    def _compact_path(cls, path: str) -> str:
        """
        压缩路径（使用 ~ 替代 home）

        :param path: 文件路径
        :return: 压缩后的路径
        """
        home = str(Path.home())
        if path.startswith(home):
            return path.replace(home, '~', 1)
        return path

    @classmethod
    async def _get_user_skill_config(cls, user_id: int, query_db: AsyncSession) -> dict | None:
        """
        获取用户技能配置

        :param user_id: 用户ID
        :param query_db: 数据库会话
        :return: 用户配置字典
        """
        # TODO: 从数据库加载用户技能配置
        # 目前返回 None，使用默认配置
        return None
