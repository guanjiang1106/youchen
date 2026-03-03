from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel




class InfoModel(BaseModel):
    """
    工艺信息表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: int | None = Field(default=None, description='主键 ID')
    process_code: str | None = Field(default=None, description='工艺编码')
    process_name: str | None = Field(default=None, description='工艺名称')
    process_type: int | None = Field(default=None, description='工艺类型')
    description: str | None = Field(default=None, description='工艺描述')
    standard_hours: Decimal | None = Field(default=None, description='标准工时')
    required_equipment: str | None = Field(default=None, description='所需设备')
    operator_level: int | None = Field(default=None, description='操作员等级要求')
    status: int | None = Field(default=None, description='状态')
    version: str | None = Field(default=None, description='版本号')
    create_time: datetime | None = Field(default=None, description='创建时间')
    update_time: datetime | None = Field(default=None, description='更新时间')






class InfoQueryModel(InfoModel):
    """
    工艺信息不分页查询模型
    """
    pass


class InfoPageQueryModel(InfoQueryModel):
    """
    工艺信息分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteInfoModel(BaseModel):
    """
    删除工艺信息模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的主键 ID')
