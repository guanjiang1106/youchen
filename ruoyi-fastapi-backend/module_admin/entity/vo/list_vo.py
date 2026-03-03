from datetime import datetime, date

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel




class ListModel(BaseModel):
    """
    设备清单表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: int | None = Field(default=None, description='主键 ID')
    device_code: str | None = Field(default=None, description='设备编码')
    device_name: str | None = Field(default=None, description='设备名称')
    device_type: str | None = Field(default=None, description='设备类型')
    brand: str | None = Field(default=None, description='品牌')
    model: str | None = Field(default=None, description='型号')
    serial_number: str | None = Field(default=None, description='序列号')
    purchase_date: date | None = Field(default=None, description='购买日期')
    warranty_period: int | None = Field(default=None, description='保修期（月）')
    status: int | None = Field(default=None, description='状态')
    location: str | None = Field(default=None, description='存放位置')
    department: str | None = Field(default=None, description='所属部门')
    responsible_person: str | None = Field(default=None, description='责任人')
    remarks: str | None = Field(default=None, description='备注')
    create_time: datetime | None = Field(default=None, description='创建时间')
    update_time: datetime | None = Field(default=None, description='更新时间')






class ListQueryModel(ListModel):
    """
    设备清单不分页查询模型
    """
    pass


class ListPageQueryModel(ListQueryModel):
    """
    设备清单分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteListModel(BaseModel):
    """
    删除设备清单模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的主键 ID')
