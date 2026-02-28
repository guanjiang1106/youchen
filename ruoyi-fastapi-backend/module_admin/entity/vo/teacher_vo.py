from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank




class TeacherModel(BaseModel):
    """
    老师维护表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: int | None = Field(default=None, description='主键 ID')
    teacher_no: str | None = Field(default=None, description='教师编号')
    name: str | None = Field(default=None, description='姓名')
    gender: int | None = Field(default=None, description='性别：0-未知，1-男，2-女')
    birth_date: date | None = Field(default=None, description='出生日期')
    phone: str | None = Field(default=None, description='联系电话')
    email: str | None = Field(default=None, description='电子邮箱')
    department: str | None = Field(default=None, description='所属部门')
    title: str | None = Field(default=None, description='职称')
    status: int | None = Field(default=None, description='状态：0-禁用，1-启用')
    create_time: datetime | None = Field(default=None, description='创建时间')
    update_time: datetime | None = Field(default=None, description='更新时间')

    @NotBlank(field_name='teacher_no', message='教师编号不能为空')
    def get_teacher_no(self) -> str | None:
        return self.teacher_no

    @NotBlank(field_name='name', message='姓名不能为空')
    def get_name(self) -> str | None:
        return self.name

    @NotBlank(field_name='gender', message='性别：0-未知，1-男，2-女不能为空')
    def get_gender(self) -> int | None:
        return self.gender

    @NotBlank(field_name='status', message='状态：0-禁用，1-启用不能为空')
    def get_status(self) -> int | None:
        return self.status


    def validate_fields(self) -> None:
        self.get_teacher_no()
        self.get_name()
        self.get_gender()
        self.get_status()




class TeacherQueryModel(TeacherModel):
    """
    老师维护不分页查询模型
    """
    pass


class TeacherPageQueryModel(TeacherQueryModel):
    """
    老师维护分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteTeacherModel(BaseModel):
    """
    删除老师维护模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的主键 ID')
