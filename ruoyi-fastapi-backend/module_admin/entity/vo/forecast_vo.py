from decimal import Decimal
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank




class ForecastModel(BaseModel):
    """
    销售预测，存储各产品在各区域的销售预测数据表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: int | None = Field(default=None, description='主键 ID，自增序列')
    product_id: int | None = Field(default=None, description='关联的产品 ID')
    region_code: str | None = Field(default=None, description='区域代码，标识销售区域')
    forecast_date: date | None = Field(default=None, description='预测日期，指预测对应的业务日期')
    predicted_amount: Decimal | None = Field(default=None, description='预测销售额，单位为元')
    confidence_level: int | None = Field(default=None, description='置信度等级，0-100 表示预测的可信程度')
    model_version: str | None = Field(default=None, description='生成该预测的算法模型版本')
    created_at: datetime | None = Field(default=None, description='记录创建时间')
    updated_at: datetime | None = Field(default=None, description='记录最后更新时间')

    @NotBlank(field_name='product_id', message='关联的产品 ID不能为空')
    def get_product_id(self) -> int | None:
        return self.product_id

    @NotBlank(field_name='region_code', message='区域代码，标识销售区域不能为空')
    def get_region_code(self) -> str | None:
        return self.region_code

    @NotBlank(field_name='forecast_date', message='预测日期，指预测对应的业务日期不能为空')
    def get_forecast_date(self) -> date | None:
        return self.forecast_date

    @NotBlank(field_name='predicted_amount', message='预测销售额，单位为元不能为空')
    def get_predicted_amount(self) -> Decimal | None:
        return self.predicted_amount

    @NotBlank(field_name='confidence_level', message='置信度等级，0-100 表示预测的可信程度不能为空')
    def get_confidence_level(self) -> int | None:
        return self.confidence_level


    def validate_fields(self) -> None:
        self.get_product_id()
        self.get_region_code()
        self.get_forecast_date()
        self.get_predicted_amount()
        self.get_confidence_level()




class ForecastQueryModel(ForecastModel):
    """
    销售预测，存储各产品在各区域的销售预测数据不分页查询模型
    """
    pass


class ForecastPageQueryModel(ForecastQueryModel):
    """
    销售预测，存储各产品在各区域的销售预测数据分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteForecastModel(BaseModel):
    """
    删除销售预测，存储各产品在各区域的销售预测数据模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的主键 ID，自增序列')
