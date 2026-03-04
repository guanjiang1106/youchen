"""
网页工具

提供网页搜索和内容获取功能
"""
import json
from typing import Any

import httpx
from agno.tools import tool

from utils.log_util import logger


@tool
async def fetch_wikipedia_info(
    title: str,
    language: str = 'zh',
) -> str:
    """
    从维基百科获取信息
    
    Use this tool to fetch information from Wikipedia.
    
    Args:
        title: 要查询的标题（例如：公司名称、人物名称等）
        language: 语言代码（zh=中文, en=英文）
    
    Returns:
        维基百科的摘要信息
    
    Examples:
        - fetch_wikipedia_info("博威合金材料股份有限公司")
        - fetch_wikipedia_info("Python", language="en")
    """
    try:
        logger.info(f'🌐 [工具调用] fetch_wikipedia_info')
        logger.info(f'📝 [标题] {title}')
        logger.info(f'🌍 [语言] {language}')
        
        # 构建 API URL
        api_url = f'https://{language}.wikipedia.org/w/api.php'
        params = {
            'action': 'query',
            'format': 'json',
            'prop': 'extracts',
            'titles': title,
            'exintro': True,
            'explaintext': True,
            'formatversion': '2',
        }
        
        logger.info(f'⏳ [执行中] 正在获取维基百科信息...')
        
        # 使用 httpx 发送请求
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(api_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # 提取内容
            pages = data.get('query', {}).get('pages', [])
            if not pages:
                return f'未找到关于 "{title}" 的信息'
            
            page = pages[0]
            extract = page.get('extract', '')
            
            if not extract:
                return f'未找到关于 "{title}" 的详细信息'
            
            # 截取前500个字符
            if len(extract) > 500:
                extract = extract[:500] + '...'
            
            logger.info(f'✅ [成功] 获取到 {len(extract)} 字符的信息')
            return extract
            
    except httpx.HTTPError as e:
        error_msg = f'HTTP 请求失败: {str(e)}'
        logger.error(f'❌ [HTTP错误] {error_msg}')
        return f'Error: {error_msg}'
    except Exception as e:
        error_msg = f'获取维基百科信息失败: {type(e).__name__}: {str(e)}'
        logger.error(f'❌ [异常] {error_msg}')
        return f'Error: {error_msg}'


@tool
async def search_web(
    query: str,
    max_results: int = 5,
) -> str:
    """
    搜索网页信息
    
    Use this tool to search for information on the web.
    
    Args:
        query: 搜索关键词
        max_results: 最多返回的结果数量（默认5条）
    
    Returns:
        搜索结果摘要
    
    Examples:
        - search_web("博威合金材料股份有限公司 最新财报")
        - search_web("Python 教程")
    """
    try:
        logger.info(f'🔍 [工具调用] search_web')
        logger.info(f'📝 [关键词] {query}')
        logger.info(f'📊 [结果数] {max_results}')
        
        # TODO: 这里可以集成真实的搜索 API（如 Google、Bing、DuckDuckGo）
        # 目前返回提示信息
        return f'搜索功能开发中，请使用 fetch_wikipedia_info 工具获取维基百科信息，或使用 execute_python_code 工具执行自定义搜索代码。'
        
    except Exception as e:
        error_msg = f'搜索失败: {type(e).__name__}: {str(e)}'
        logger.error(f'❌ [异常] {error_msg}')
        return f'Error: {error_msg}'
