"""
AI 技能执行器

本模块负责执行技能命令，支持 bash 命令执行。
参考 OpenClaw 的执行逻辑实现。
"""

import asyncio
import time
from typing import Any

from module_ai.skills.types import Skill, SkillResult
from utils.log_util import logger


class SkillExecutor:
    """技能执行器 - 执行技能命令"""

    def __init__(self, timeout: int = 30):
        """
        初始化技能执行器

        :param timeout: 命令执行超时时间（秒）
        """
        self.timeout = timeout

    async def execute_skill(
        self,
        skill: Skill,
        command: str,
        args: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
    ) -> SkillResult:
        """
        执行技能

        :param skill: 技能对象
        :param command: 要执行的命令
        :param args: 命令参数
        :param context: 执行上下文
        :return: 技能执行结果
        """
        start_time = time.time()

        try:
            # 目前只支持 bash 命令执行
            output = await self._execute_bash(command, args, skill.base_dir)

            duration_ms = int((time.time() - start_time) * 1000)

            logger.info(f'Skill {skill.name} executed successfully in {duration_ms}ms')

            return SkillResult(
                success=True,
                output=output,
                duration_ms=duration_ms,
            )

        except asyncio.TimeoutError:
            duration_ms = int((time.time() - start_time) * 1000)
            error_msg = f'Command timeout after {self.timeout}s'
            logger.error(f'Skill {skill.name} execution timeout: {error_msg}')

            return SkillResult(
                success=False,
                output='',
                error=error_msg,
                duration_ms=duration_ms,
            )

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            error_msg = str(e)
            logger.error(f'Skill {skill.name} execution failed: {error_msg}')

            return SkillResult(
                success=False,
                output='',
                error=error_msg,
                duration_ms=duration_ms,
            )

    async def _execute_bash(self, command: str, args: dict[str, Any] | None, cwd: str | None = None) -> str:
        """
        执行 bash 命令

        :param command: 命令字符串
        :param args: 命令参数
        :param cwd: 工作目录
        :return: 命令输出
        """
        # 构建完整命令
        full_command = self._build_command(command, args)

        logger.debug(f'Executing bash command: {full_command}')

        # 创建子进程执行命令
        process = await asyncio.create_subprocess_shell(
            full_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
        )

        try:
            # 等待命令执行完成（带超时）
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.timeout,
            )

            # 检查返回码
            if process.returncode != 0:
                error_output = stderr.decode('utf-8', errors='replace')
                raise RuntimeError(f'Command failed with exit code {process.returncode}: {error_output}')

            # 返回标准输出
            return stdout.decode('utf-8', errors='replace')

        except asyncio.TimeoutError:
            # 超时，杀死进程
            try:
                process.kill()
                await process.wait()
            except Exception:
                pass
            raise

    def _build_command(self, command: str, args: dict[str, Any] | None) -> str:
        """
        构建命令字符串

        支持简单的参数替换：{arg_name} -> arg_value

        :param command: 命令模板
        :param args: 参数字典
        :return: 完整命令字符串
        """
        if not args:
            return command

        # 简单的参数替换
        result = command
        for key, value in args.items():
            placeholder = f'{{{key}}}'
            if placeholder in result:
                # 对参数值进行简单的转义（防止命令注入）
                safe_value = self._escape_shell_arg(str(value))
                result = result.replace(placeholder, safe_value)

        return result

    def _escape_shell_arg(self, arg: str) -> str:
        """
        转义 shell 参数（简单实现）

        :param arg: 参数值
        :return: 转义后的参数值
        """
        # 如果参数包含空格或特殊字符，用引号包裹
        if ' ' in arg or any(c in arg for c in ['$', '`', '"', "'", '\\', '|', '&', ';', '<', '>', '(', ')']):
            # 转义单引号
            escaped = arg.replace("'", "'\\''")
            return f"'{escaped}'"
        return arg
