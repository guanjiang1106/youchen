from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank




class TableModel(BaseModel):
    """
    质量检验记录表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: int | None = Field(default=None, description='主键 ID')
    product_code: str | None = Field(default=None, description='产品编码')
    batch_number: str | None = Field(default=None, description='生产批次号')
    inspection_result: int | None = Field(default=None, description='检验结果 (0:待检，1:合格，2:不合格)')
    defect_count: int | None = Field(default=None, description='缺陷数量')
    inspector_name: str | None = Field(default=None, description='检验员姓名')
    remarks: str | None = Field(default=None, description='备注说明')
    create_time: datetime | None = Field(default=None, description='创建时间')
    update_time: datetime | None = Field(default=None, description='更新时间')

    @NotBlank(field_name='product_code', message='产品编码不能为空')
    def get_product_code(self) -> str | None:
        return self.product_code

    @NotBlank(field_name='batch_number', message='生产批次号不能为空')
    def get_batch_number(self) -> str | None:
        return self.batch_number

    @NotBlank(field_name='inspection_result', message='检验结果 (0:待检，1:合格，2:不合格)不能为空')
    def get_inspection_result(self) -> int | None:
        return self.inspection_result

    @NotBlank(field_name='defect_count', message='缺陷数量不能为空')
    def get_defect_count(self) -> int | None:
        return self.defect_count


    def validate_fields(self) -> None:
        self.get_product_code()
        self.get_batch_number()
        self.get_inspection_result()
        self.get_defect_count()




class TableQueryModel(TableModel):
    """
    质量检验记录不分页查询模型
    """
    pass


class TablePageQueryModel(TableQueryModel):
    """
    质量检验记录分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteTableModel(BaseModel):
    """
    删除质量检验记录模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的主键 ID')
