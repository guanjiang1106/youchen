"""
AI 技能视图对象

Task 3.4: 添加技能视图对象
"""

from datetime import datetime

from pydantic import BaseModel, Field


class SkillModel(BaseModel):
    """技能详情模型"""

    name: str = Field(description='技能名称')
    description: str = Field(description='技能描述')
    content: str | None = Field(default=None, description='技能内容（Markdown）')
    file_path: str | None = Field(default=None, description='技能文件路径')
    base_dir: str | None = Field(default=None, description='技能基础目录')
    source: str = Field(default='unknown', description='技能来源')
    enabled: bool = Field(default=True, description='是否启用')
    
    # 元数据
    emoji: str | None = Field(default=None, description='技能图标')
    homepage: str | None = Field(default=None, description='技能主页')
    os: list[str] | None = Field(default=None, description='支持的操作系统')
    
    # 依赖信息
    bins: list[str] | None = Field(default=None, description='必需的命令')
    any_bins: list[str] | None = Field(default=None, description='可选的命令（至少一个）')
    env: list[str] | None = Field(default=None, description='必需的环境变量')
    
    class Config:
        json_schema_extra = {
            'example': {
                'name': 'weather',
                'description': 'Get weather information',
                'enabled': True,
                'emoji': '🌤️',
                'os': ['linux', 'darwin', 'win32'],
                'bins': ['curl'],
            }
        }


class SkillListModel(BaseModel):
    """技能列表模型"""

    name: str = Field(description='技能名称')
    description: str = Field(description='技能描述')
    enabled: bool = Field(default=True, description='是否启用')
    emoji: str | None = Field(default=None, description='技能图标')
    source: str = Field(default='unknown', description='技能来源')
    
    class Config:
        json_schema_extra = {
            'example': {
                'name': 'weather',
                'description': 'Get weather information',
                'enabled': True,
                'emoji': '🌤️',
                'source': 'bundled',
            }
        }


class SkillStatsModel(BaseModel):
    """技能统计模型"""

    skill_name: str = Field(description='技能名称')
    total_invocations: int = Field(default=0, description='总调用次数')
    success_count: int = Field(default=0, description='成功次数')
    failure_count: int = Field(default=0, description='失败次数')
    avg_execution_time: float = Field(default=0.0, description='平均执行时间（秒）')
    last_invoked_at: datetime | None = Field(default=None, description='最后调用时间')
    
    class Config:
        json_schema_extra = {
            'example': {
                'skill_name': 'weather',
                'total_invocations': 150,
                'success_count': 145,
                'failure_count': 5,
                'avg_execution_time': 1.23,
                'last_invoked_at': '2026-03-03T10:30:00',
            }
        }


class SkillExecutionModel(BaseModel):
    """技能执行结果模型"""

    skill_name: str = Field(description='技能名称')
    success: bool = Field(description='是否成功')
    output: str = Field(default='', description='执行输出')
    error: str = Field(default='', description='错误信息')
    execution_time: float = Field(default=0.0, description='执行时间（秒）')
    timestamp: datetime = Field(default_factory=datetime.now, description='执行时间戳')
    
    class Config:
        json_schema_extra = {
            'example': {
                'skill_name': 'weather',
                'success': True,
                'output': 'Beijing: ☀️  +15°C',
                'error': '',
                'execution_time': 1.23,
                'timestamp': '2026-03-03T10:30:00',
            }
        }


class SkillPageQueryModel(BaseModel):
    """技能分页查询模型"""

    page_num: int = Field(default=1, ge=1, description='页码')
    page_size: int = Field(default=10, ge=1, le=100, description='每页数量')
    name: str | None = Field(default=None, description='技能名称（模糊查询）')
    enabled: bool | None = Field(default=None, description='是否启用')
    source: str | None = Field(default=None, description='技能来源')
    
    class Config:
        json_schema_extra = {
            'example': {
                'page_num': 1,
                'page_size': 10,
                'name': 'weather',
                'enabled': True,
                'source': 'bundled',
            }
        }


class SkillEnableModel(BaseModel):
    """技能启用/禁用模型"""

    enabled: bool = Field(description='是否启用')
    
    class Config:
        json_schema_extra = {'example': {'enabled': True}}


class CacheStatsModel(BaseModel):
    """缓存统计模型"""

    hits: int = Field(description='缓存命中次数')
    misses: int = Field(description='缓存未命中次数')
    evictions: int = Field(description='缓存驱逐次数')
    hit_rate: float = Field(description='缓存命中率（%）')
    total_requests: int = Field(description='总请求次数')
    cached_items: int = Field(description='缓存项数量')
    
    class Config:
        json_schema_extra = {
            'example': {
                'hits': 850,
                'misses': 150,
                'evictions': 20,
                'hit_rate': 85.0,
                'total_requests': 1000,
                'cached_items': 45,
            }
        }
