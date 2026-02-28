from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel




class MaterialModel(BaseModel):
    """
    物料表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: int | None = Field(default=None, description='主键 ID')
    material_code: str | None = Field(default=None, description='物料编码')
    material_name: str | None = Field(default=None, description='物料名称')
    specification: str | None = Field(default=None, description='规格型号')
    unit: str | None = Field(default=None, description='计量单位')
    category_id: int | None = Field(default=None, description='分类 ID')
    stock_quantity: Decimal | None = Field(default=None, description='库存数量')
    safety_stock: Decimal | None = Field(default=None, description='安全库存')
    price: Decimal | None = Field(default=None, description='参考单价')
    status: int | None = Field(default=None, description='状态：1-启用，0-禁用')
    remark: str | None = Field(default=None, description='备注')
    create_time: datetime | None = Field(default=None, description='创建时间')
    update_time: datetime | None = Field(default=None, description='更新时间')






class MaterialQueryModel(MaterialModel):
    """
    物料不分页查询模型
    """
    pass


class MaterialPageQueryModel(MaterialQueryModel):
    """
    物料分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteMaterialModel(BaseModel):
    """
    删除物料模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的主键 ID')
