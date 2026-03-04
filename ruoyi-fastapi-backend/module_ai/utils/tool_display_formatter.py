"""
工具调用显示格式化器

将技术性的工具调用信息转换为业务友好的显示格式
"""
from typing import Any


class ToolDisplayFormatter:
    """工具调用显示格式化器"""
    
    # 工具名称映射（技术名称 -> 业务友好名称）
    TOOL_NAME_MAP = {
        'execute_command': '命令执行',
        'execute_python_code': 'Python 代码执行',
        'fetch_wikipedia_info': '维基百科查询',
        'search_web': '网页搜索',
        'web_search': '网页搜索',
        'web_fetch': '网页内容获取',
        'file_read': '文件读取',
        'file_write': '文件写入',
        'database_query': '数据库查询',
    }
    
    @classmethod
    def format_tool_call(cls, tool_name: str, tool_args: dict[str, Any]) -> str:
        """
        格式化工具调用信息为业务友好的显示
        
        Args:
            tool_name: 工具名称
            tool_args: 工具参数
            
        Returns:
            格式化后的显示文本
        """
        # 获取友好的工具名称
        friendly_name = cls.TOOL_NAME_MAP.get(tool_name, tool_name)
        
        # 根据不同工具类型格式化
        if tool_name == 'execute_command':
            return cls._format_execute_command(friendly_name, tool_args)
        elif tool_name == 'execute_python_code':
            return cls._format_execute_python(friendly_name, tool_args)
        elif tool_name == 'web_search':
            return cls._format_web_search(friendly_name, tool_args)
        elif tool_name == 'web_fetch':
            return cls._format_web_fetch(friendly_name, tool_args)
        else:
            return cls._format_generic(friendly_name, tool_args)
    
    @classmethod
    def _format_execute_command(cls, friendly_name: str, tool_args: dict) -> str:
        """格式化命令执行工具"""
        command = tool_args.get('command', '')
        cwd = tool_args.get('cwd')
        timeout = tool_args.get('timeout', 30)
        
        # 简化命令显示（截取前100个字符）
        display_command = command[:100] + '...' if len(command) > 100 else command
        
        lines = [
            f'🔧 正在调用工具：{friendly_name}',
            f'📝 执行命令：{display_command}',
        ]
        
        if cwd:
            lines.append(f'📁 工作目录：{cwd}')
        
        lines.append(f'⏱️  超时时间：{timeout}秒')
        lines.append('⏳ 执行中...')
        
        return '\n'.join(lines)
    
    @classmethod
    def _format_execute_python(cls, friendly_name: str, tool_args: dict) -> str:
        """格式化 Python 代码执行工具"""
        code = tool_args.get('code', '')
        timeout = tool_args.get('timeout', 30)
        
        # 显示代码的前3行
        code_lines = code.split('\n')
        preview_lines = code_lines[:3]
        preview = '\n  '.join(preview_lines)
        
        if len(code_lines) > 3:
            preview += f'\n  ... (共 {len(code_lines)} 行)'
        
        lines = [
            f'🐍 正在调用工具：{friendly_name}',
            f'📝 代码预览：',
            f'  {preview}',
            f'⏱️  超时时间：{timeout}秒',
            '⏳ 执行中...',
        ]
        
        return '\n'.join(lines)
    
    @classmethod
    def _format_web_search(cls, friendly_name: str, tool_args: dict) -> str:
        """格式化网页搜索工具"""
        query = tool_args.get('query', '')
        
        lines = [
            f'🔍 正在调用工具：{friendly_name}',
            f'📝 搜索关键词：{query}',
            '⏳ 搜索中...',
        ]
        
        return '\n'.join(lines)
    
    @classmethod
    def _format_web_fetch(cls, friendly_name: str, tool_args: dict) -> str:
        """格式化网页内容获取工具"""
        url = tool_args.get('url', '')
        
        lines = [
            f'🌐 正在调用工具：{friendly_name}',
            f'📝 目标网址：{url}',
            '⏳ 获取中...',
        ]
        
        return '\n'.join(lines)
    
    @classmethod
    def _format_generic(cls, friendly_name: str, tool_args: dict) -> str:
        """格式化通用工具"""
        lines = [
            f'🔧 正在调用工具：{friendly_name}',
        ]
        
        # 显示参数（最多显示3个）
        if tool_args:
            lines.append('📝 参数：')
            for i, (key, value) in enumerate(list(tool_args.items())[:3]):
                # 简化值的显示
                if isinstance(value, str) and len(value) > 50:
                    value = value[:50] + '...'
                lines.append(f'  - {key}: {value}')
            
            if len(tool_args) > 3:
                lines.append(f'  ... (共 {len(tool_args)} 个参数)')
        
        lines.append('⏳ 执行中...')
        
        return '\n'.join(lines)
    
    @classmethod
    def format_tool_result(cls, tool_name: str, result: str, success: bool = True) -> str:
        """
        格式化工具执行结果
        
        Args:
            tool_name: 工具名称
            result: 执行结果
            success: 是否成功
            
        Returns:
            格式化后的结果文本
        """
        friendly_name = cls.TOOL_NAME_MAP.get(tool_name, tool_name)
        
        if success:
            status_icon = '✅'
            status_text = '执行成功'
        else:
            status_icon = '❌'
            status_text = '执行失败'
        
        # 简化结果显示（最多显示前200个字符）
        display_result = result[:200] + '...' if len(result) > 200 else result
        
        lines = [
            f'{status_icon} {friendly_name} - {status_text}',
            f'📄 结果：',
            f'{display_result}',
        ]
        
        return '\n'.join(lines)


# 便捷函数
def format_tool_call(tool_name: str, tool_args: dict[str, Any]) -> str:
    """格式化工具调用（便捷函数）"""
    return ToolDisplayFormatter.format_tool_call(tool_name, tool_args)


def format_tool_result(tool_name: str, result: str, success: bool = True) -> str:
    """格式化工具结果（便捷函数）"""
    return ToolDisplayFormatter.format_tool_result(tool_name, result, success)
