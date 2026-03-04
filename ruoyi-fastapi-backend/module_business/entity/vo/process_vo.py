from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel




class ProcessModel(BaseModel):
    """
    工艺表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: int | None = Field(default=None, description='主键 ID')
    process_code: str | None = Field(default=None, description='工艺编码')
    process_name: str | None = Field(default=None, description='工艺名称')
    description: str | None = Field(default=None, description='工艺描述')
    category: str | None = Field(default=None, description='工艺分类')
    version: str | None = Field(default=None, description='版本号')
    status: int | None = Field(default=None, description='状态')
    sort_order: int | None = Field(default=None, description='排序顺序')
    create_time: datetime | None = Field(default=None, description='创建时间')
    update_time: datetime | None = Field(default=None, description='更新时间')






class ProcessQueryModel(ProcessModel):
    """
    工艺不分页查询模型
    """
    pass


class ProcessPageQueryModel(ProcessQueryModel):
    """
    工艺分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteProcessModel(BaseModel):
    """
    删除工艺模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的主键 ID')
