from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel




class WarehouseModel(BaseModel):
    """
    仓库表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: int | None = Field(default=None, description='主键 ID')
    id: int | None = Field(default=None, description='主键 ID')
    code: str | None = Field(default=None, description='仓库编码')
    name: str | None = Field(default=None, description='仓库名称')
    address: str | None = Field(default=None, description='仓库地址')
    contact_person: str | None = Field(default=None, description='联系人')
    contact_phone: str | None = Field(default=None, description='联系电话')
    capacity: Decimal | None = Field(default=None, description='仓库容量')
    status: int | None = Field(default=None, description='状态：1-启用，0-禁用')
    remark: str | None = Field(default=None, description='备注')
    create_time: datetime | None = Field(default=None, description='创建时间')
    update_time: datetime | None = Field(default=None, description='更新时间')






class WarehouseQueryModel(WarehouseModel):
    """
    仓库不分页查询模型
    """
    pass


class WarehousePageQueryModel(WarehouseQueryModel):
    """
    仓库分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteWarehouseModel(BaseModel):
    """
    删除仓库模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的主键 ID')
