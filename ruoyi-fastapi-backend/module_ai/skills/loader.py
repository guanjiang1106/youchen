"""
AI 技能加载器

本模块负责从文件系统加载技能，解析 SKILL.md 文件和 frontmatter 元数据。
参考 OpenClaw 的 workspace.ts 实现。
"""

import os
from pathlib import Path
from typing import Any

import frontmatter

from module_ai.skills.types import (
    Skill,
    SkillInstallSpec,
    SkillInvocationPolicy,
    SkillMetadata,
    SkillRequirements,
)
from utils.log_util import logger


class SkillLoader:
    """技能加载器 - 负责从文件系统加载技能"""

    # 默认限制
    DEFAULT_MAX_CANDIDATES_PER_ROOT = 300
    DEFAULT_MAX_SKILLS_LOADED_PER_SOURCE = 200
    DEFAULT_MAX_SKILL_FILE_BYTES = 256000  # 256KB

    def __init__(
        self,
        skills_dirs: list[str],
        max_candidates_per_root: int | None = None,
        max_skills_loaded_per_source: int | None = None,
        max_skill_file_bytes: int | None = None,
    ):
        """
        初始化技能加载器

        :param skills_dirs: 技能目录列表
        :param max_candidates_per_root: 每个根目录最多扫描的候选数
        :param max_skills_loaded_per_source: 每个来源最多加载的技能数
        :param max_skill_file_bytes: 技能文件最大字节数
        """
        self.skills_dirs = skills_dirs
        self.max_candidates_per_root = max_candidates_per_root or self.DEFAULT_MAX_CANDIDATES_PER_ROOT
        self.max_skills_loaded_per_source = max_skills_loaded_per_source or self.DEFAULT_MAX_SKILLS_LOADED_PER_SOURCE
        self.max_skill_file_bytes = max_skill_file_bytes or self.DEFAULT_MAX_SKILL_FILE_BYTES
        self._cache: dict[str, Skill] = {}

    def load_all_skills(self) -> list[Skill]:
        """
        加载所有技能

        :return: 技能列表
        """
        all_skills: dict[str, Skill] = {}

        for dir_path in self.skills_dirs:
            try:
                skills = self._load_from_dir(dir_path)
                # 后加载的技能会覆盖先加载的同名技能（优先级）
                for skill in skills:
                    all_skills[skill.name] = skill
            except Exception as e:
                logger.warning(f'Failed to load skills from {dir_path}: {e}')
                continue

        return list(all_skills.values())

    def _load_from_dir(self, dir_path: str, source: str = 'unknown') -> list[Skill]:
        """
        从目录加载技能

        :param dir_path: 目录路径
        :param source: 技能来源标识
        :return: 技能列表
        """
        dir_path = os.path.expanduser(dir_path)
        if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
            logger.debug(f'Skills directory does not exist: {dir_path}')
            return []

        # 检查是否是嵌套的 skills 目录
        resolved = self._resolve_nested_skills_root(dir_path)
        base_dir = resolved['base_dir']
        if resolved.get('note'):
            logger.debug(resolved['note'])

        # 检查根目录本身是否是技能目录
        root_skill_md = os.path.join(base_dir, 'SKILL.md')
        if os.path.exists(root_skill_md):
            try:
                size = os.path.getsize(root_skill_md)
                if size > self.max_skill_file_bytes:
                    logger.warning(
                        f'Skipping skills root due to oversized SKILL.md: {root_skill_md} ({size} bytes)'
                    )
                    return []
                skill = self.parse_skill_file(root_skill_md, source)
                return [skill] if skill else []
            except Exception as e:
                logger.warning(f'Failed to parse skill from {root_skill_md}: {e}')
                return []

        # 扫描子目录
        child_dirs = self._list_child_directories(base_dir)
        if len(child_dirs) > self.max_candidates_per_root:
            logger.warning(
                f'Skills root looks suspiciously large, truncating discovery: '
                f'{base_dir} ({len(child_dirs)} dirs)'
            )

        # 限制扫描数量
        max_candidates = min(len(child_dirs), self.max_skills_loaded_per_source)
        limited_children = sorted(child_dirs)[:max_candidates]

        loaded_skills: list[Skill] = []

        for name in limited_children:
            skill_dir = os.path.join(base_dir, name)
            skill_md = os.path.join(skill_dir, 'SKILL.md')

            if not os.path.exists(skill_md):
                continue

            try:
                size = os.path.getsize(skill_md)
                if size > self.max_skill_file_bytes:
                    logger.warning(f'Skipping skill due to oversized SKILL.md: {skill_md} ({size} bytes)')
                    continue

                skill = self.parse_skill_file(skill_md, source)
                if skill:
                    loaded_skills.append(skill)

                if len(loaded_skills) >= self.max_skills_loaded_per_source:
                    break

            except Exception as e:
                logger.warning(f'Failed to parse skill from {skill_md}: {e}')
                continue

        return loaded_skills

    def parse_skill_file(self, file_path: str, source: str = 'unknown') -> Skill | None:
        """
        解析 SKILL.md 文件

        :param file_path: 文件路径
        :param source: 技能来源标识
        :return: 技能对象，解析失败返回 None
        """
        try:
            with open(file_path, encoding='utf-8') as f:
                content = f.read()

            # 解析 frontmatter
            post = frontmatter.loads(content)
            fm = post.metadata
            body = post.content

            # 提取基本信息
            name = fm.get('name', '')
            if not name:
                # 如果没有 name，使用目录名
                name = Path(file_path).parent.name

            description = fm.get('description', '')
            base_dir = str(Path(file_path).parent)

            # 解析元数据
            metadata = self._parse_metadata(fm)
            invocation = self._parse_invocation_policy(fm)

            return Skill(
                name=name,
                description=description,
                content=content,
                file_path=file_path,
                base_dir=base_dir,
                source=source,
                frontmatter=fm,
                metadata=metadata,
                invocation=invocation,
            )

        except Exception as e:
            logger.error(f'Failed to parse skill file {file_path}: {e}')
            return None

    def _parse_metadata(self, frontmatter: dict[str, Any]) -> SkillMetadata:
        """
        解析 OpenClaw 元数据

        :param frontmatter: frontmatter 字典
        :return: 技能元数据对象
        """
        # OpenClaw 元数据在 metadata.openclaw 字段中
        openclaw_meta = frontmatter.get('metadata', {}).get('openclaw', {})

        # 解析依赖要求
        requires_data = openclaw_meta.get('requires', {})
        requires = None
        if requires_data:
            requires = SkillRequirements(
                bins=requires_data.get('bins'),
                any_bins=requires_data.get('anyBins'),
                env=requires_data.get('env'),
                config=requires_data.get('config'),
            )

        # 解析安装规范
        install_data = openclaw_meta.get('install', [])
        install = None
        if install_data:
            install = []
            for spec in install_data:
                install.append(
                    SkillInstallSpec(
                        kind=spec.get('kind', 'download'),
                        id=spec.get('id'),
                        label=spec.get('label'),
                        bins=spec.get('bins'),
                        os=spec.get('os'),
                        formula=spec.get('formula'),
                        package=spec.get('package'),
                        module=spec.get('module'),
                        url=spec.get('url'),
                        archive=spec.get('archive'),
                        extract=spec.get('extract'),
                        strip_components=spec.get('stripComponents'),
                        target_dir=spec.get('targetDir'),
                    )
                )

        return SkillMetadata(
            always=openclaw_meta.get('always', False),
            skill_key=openclaw_meta.get('skillKey'),
            primary_env=openclaw_meta.get('primaryEnv'),
            emoji=openclaw_meta.get('emoji'),
            homepage=frontmatter.get('homepage'),
            os=openclaw_meta.get('os'),
            requires=requires,
            install=install,
        )

    def _parse_invocation_policy(self, frontmatter: dict[str, Any]) -> SkillInvocationPolicy:
        """
        解析技能调用策略

        :param frontmatter: frontmatter 字典
        :return: 调用策略对象
        """
        invocation_data = frontmatter.get('invocation', {})
        return SkillInvocationPolicy(
            user_invocable=invocation_data.get('userInvocable', True),
            disable_model_invocation=invocation_data.get('disableModelInvocation', False),
        )

    def _resolve_nested_skills_root(self, dir_path: str) -> dict[str, Any]:
        """
        解析嵌套的 skills 根目录

        如果目录下有 skills 子目录，并且该子目录包含技能，则使用子目录作为根目录。

        :param dir_path: 目录路径
        :return: 包含 base_dir 和可选 note 的字典
        """
        nested = os.path.join(dir_path, 'skills')
        if not os.path.exists(nested) or not os.path.isdir(nested):
            return {'base_dir': dir_path}

        # 启发式检查：如果 dir/skills/*/SKILL.md 存在，则使用 dir/skills 作为根目录
        nested_dirs = self._list_child_directories(nested)
        scan_limit = min(len(nested_dirs), 100)

        for name in nested_dirs[:scan_limit]:
            skill_md = os.path.join(nested, name, 'SKILL.md')
            if os.path.exists(skill_md):
                return {'base_dir': nested, 'note': f'Detected nested skills root at {nested}'}

        return {'base_dir': dir_path}

    def _list_child_directories(self, dir_path: str) -> list[str]:
        """
        列出目录下的子目录

        :param dir_path: 目录路径
        :return: 子目录名称列表
        """
        try:
            entries = os.listdir(dir_path)
            dirs = []
            for name in entries:
                if name.startswith('.') or name == 'node_modules':
                    continue
                full_path = os.path.join(dir_path, name)
                if os.path.isdir(full_path):
                    dirs.append(name)
            return dirs
        except Exception:
            return []
