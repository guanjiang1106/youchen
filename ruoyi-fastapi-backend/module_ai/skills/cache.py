"""
AI 技能缓存机制

本模块提供技能加载的缓存功能，提升性能。
Task 3.1: 添加技能缓存机制
"""

import time
from typing import Any

from module_ai.skills.types import Skill
from utils.log_util import logger


class SkillCache:
    """技能缓存类 - 提供内存缓存和 TTL 支持"""

    def __init__(self, ttl: int = 300):
        """
        初始化技能缓存

        :param ttl: 缓存过期时间（秒），默认 5 分钟
        """
        self.ttl = ttl
        self._cache: dict[str, dict[str, Any]] = {}
        self._stats = {'hits': 0, 'misses': 0, 'evictions': 0}

    def get(self, key: str) -> list[Skill] | None:
        """
        从缓存获取技能列表

        :param key: 缓存键（通常是技能目录路径）
        :return: 技能列表，如果不存在或已过期则返回 None
        """
        if key not in self._cache:
            self._stats['misses'] += 1
            return None

        entry = self._cache[key]
        current_time = time.time()

        # 检查是否过期
        if current_time - entry['timestamp'] > self.ttl:
            logger.debug(f'缓存已过期: {key}')
            self.invalidate(key)
            self._stats['misses'] += 1
            self._stats['evictions'] += 1
            return None

        self._stats['hits'] += 1
        logger.debug(f'缓存命中: {key}')
        return entry['skills']

    def set(self, key: str, skills: list[Skill]) -> None:
        """
        设置缓存

        :param key: 缓存键
        :param skills: 技能列表
        """
        self._cache[key] = {'skills': skills, 'timestamp': time.time()}
        logger.debug(f'缓存已设置: {key}, 技能数量: {len(skills)}')

    def invalidate(self, key: str) -> None:
        """
        使指定缓存失效

        :param key: 缓存键
        """
        if key in self._cache:
            del self._cache[key]
            logger.debug(f'缓存已失效: {key}')

    def invalidate_all(self) -> None:
        """清空所有缓存"""
        count = len(self._cache)
        self._cache.clear()
        logger.info(f'已清空所有缓存，共 {count} 项')

    def get_stats(self) -> dict[str, int]:
        """
        获取缓存统计信息

        :return: 包含 hits, misses, evictions 的字典
        """
        total = self._stats['hits'] + self._stats['misses']
        hit_rate = (self._stats['hits'] / total * 100) if total > 0 else 0

        return {
            'hits': self._stats['hits'],
            'misses': self._stats['misses'],
            'evictions': self._stats['evictions'],
            'hit_rate': round(hit_rate, 2),
            'total_requests': total,
            'cached_items': len(self._cache),
        }

    def reset_stats(self) -> None:
        """重置统计信息"""
        self._stats = {'hits': 0, 'misses': 0, 'evictions': 0}
        logger.debug('缓存统计已重置')

    def cleanup_expired(self) -> int:
        """
        清理所有过期的缓存项

        :return: 清理的项数
        """
        current_time = time.time()
        expired_keys = [
            key for key, entry in self._cache.items() if current_time - entry['timestamp'] > self.ttl
        ]

        for key in expired_keys:
            self.invalidate(key)

        if expired_keys:
            logger.info(f'已清理 {len(expired_keys)} 个过期缓存项')

        return len(expired_keys)


# 全局缓存实例
_global_cache: SkillCache | None = None


def get_skill_cache(ttl: int = 300) -> SkillCache:
    """
    获取全局技能缓存实例

    :param ttl: 缓存过期时间（秒）
    :return: SkillCache 实例
    """
    global _global_cache
    if _global_cache is None:
        _global_cache = SkillCache(ttl=ttl)
        logger.info(f'初始化全局技能缓存，TTL: {ttl}秒')
    return _global_cache
