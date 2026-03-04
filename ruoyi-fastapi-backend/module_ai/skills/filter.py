"""
AI 技能过滤器

本模块负责根据依赖、操作系统、用户配置等条件过滤技能。
参考 OpenClaw 的 workspace.ts 和 config.ts 实现。
"""

import os
import platform
import shutil

from module_ai.skills.types import Skill
from utils.log_util import logger


class SkillFilter:
    """技能过滤器 - 根据条件过滤技能"""

    def filter_skills(
        self,
        skills: list[Skill],
        user_config: dict | None = None,
        context: dict | None = None,
    ) -> list[Skill]:
        """
        过滤技能列表

        :param skills: 技能列表
        :param user_config: 用户配置
        :param context: 上下文信息
        :return: 过滤后的技能列表
        """
        filtered = skills

        # 1. 检查依赖
        filtered = self._filter_by_dependencies(filtered)

        # 2. 检查操作系统
        filtered = self._filter_by_os(filtered)

        # 3. 应用用户配置
        if user_config:
            filtered = self._filter_by_user_config(filtered, user_config)

        # 4. 检查启用状态
        filtered = [s for s in filtered if s.enabled]

        # 5. 检查调用策略（不包含禁用模型调用的技能）
        filtered = [s for s in filtered if not s.invocation.disable_model_invocation]

        return filtered

    def _filter_by_dependencies(self, skills: list[Skill]) -> list[Skill]:
        """
        检查依赖是否满足

        :param skills: 技能列表
        :return: 满足依赖的技能列表
        """
        result = []
        for skill in skills:
            if not skill.metadata.requires:
                result.append(skill)
                continue

            # 检查 bins（所有命令都必须存在）
            bins = skill.metadata.requires.bins
            if bins and not self._check_bins_available(bins):
                logger.debug(f'Skill {skill.name} filtered: missing bins {bins}')
                continue

            # 检查 any_bins（至少一个命令存在）
            any_bins = skill.metadata.requires.any_bins
            if any_bins and not self._check_any_bins_available(any_bins):
                logger.debug(f'Skill {skill.name} filtered: missing any of bins {any_bins}')
                continue

            # 检查 env（所有环境变量都必须存在）
            envs = skill.metadata.requires.env
            if envs and not self._check_env_available(envs):
                logger.debug(f'Skill {skill.name} filtered: missing env {envs}')
                continue

            result.append(skill)

        return result

    def _check_bins_available(self, bins: list[str]) -> bool:
        """
        检查所有命令是否可用

        :param bins: 命令列表
        :return: 所有命令都可用返回 True
        """
        return all(shutil.which(bin_name) for bin_name in bins)

    def _check_any_bins_available(self, bins: list[str]) -> bool:
        """
        检查是否至少有一个命令可用

        :param bins: 命令列表
        :return: 至少一个命令可用返回 True
        """
        return any(shutil.which(bin_name) for bin_name in bins)

    def _check_env_available(self, envs: list[str]) -> bool:
        """
        检查所有环境变量是否存在

        :param envs: 环境变量列表
        :return: 所有环境变量都存在返回 True
        """
        return all(os.getenv(env_name) for env_name in envs)

    def _filter_by_os(self, skills: list[Skill]) -> list[Skill]:
        """
        根据操作系统过滤

        :param skills: 技能列表
        :return: 支持当前操作系统的技能列表
        """
        current_os = platform.system().lower()

        result = []
        for skill in skills:
            if not skill.metadata.os:
                # 没有指定操作系统限制，支持所有系统
                result.append(skill)
                continue

            # 检查是否支持当前操作系统
            # 支持的格式：'darwin', 'linux', 'windows', 'win32' 等
            supported = False
            for os_name in skill.metadata.os:
                os_name_lower = os_name.lower()
                if os_name_lower in current_os or current_os in os_name_lower:
                    supported = True
                    break
                # 特殊处理：darwin = macos
                if os_name_lower == 'darwin' and current_os == 'darwin':
                    supported = True
                    break
                # 特殊处理：win32 = windows
                if os_name_lower in ('win32', 'windows') and current_os == 'windows':
                    supported = True
                    break

            if supported:
                result.append(skill)
            else:
                logger.debug(f'Skill {skill.name} filtered: not supported on {current_os}')

        return result

    def _filter_by_user_config(self, skills: list[Skill], user_config: dict) -> list[Skill]:
        """
        应用用户配置过滤

        :param skills: 技能列表
        :param user_config: 用户配置
        :return: 符合用户配置的技能列表
        """
        # 用户可以配置启用/禁用的技能列表
        enabled_skills = user_config.get('enabled_skills')
        disabled_skills = user_config.get('disabled_skills')

        result = []
        for skill in skills:
            # 如果配置了启用列表，只包含列表中的技能
            if enabled_skills is not None:
                if skill.name not in enabled_skills:
                    logger.debug(f'Skill {skill.name} filtered: not in enabled_skills')
                    continue

            # 如果配置了禁用列表，排除列表中的技能
            if disabled_skills is not None:
                if skill.name in disabled_skills:
                    logger.debug(f'Skill {skill.name} filtered: in disabled_skills')
                    continue

            result.append(skill)

        return result

    def normalize_skill_filter(self, skill_filter: list[str] | None) -> list[str] | None:
        """
        规范化技能过滤器

        :param skill_filter: 技能名称列表
        :return: 规范化后的技能名称列表
        """
        if skill_filter is None:
            return None

        # 去除空字符串和重复项
        normalized = list(set(name.strip() for name in skill_filter if name.strip()))
        return normalized if normalized else None
