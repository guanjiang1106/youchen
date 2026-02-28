from datetime import datetime, date

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel




class StudentsModel(BaseModel):
    """
    学生信息表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: int | None = Field(default=None, description='主键 ID')
    id: int | None = Field(default=None, description='主键 ID')
    student_no: str | None = Field(default=None, description='学号')
    student_no: str | None = Field(default=None, description='学号')
    name: str | None = Field(default=None, description='姓名')
    gender: int | None = Field(default=None, description='性别：0-未知，1-男，2-女')
    birth_date: date | None = Field(default=None, description='出生日期')
    phone: str | None = Field(default=None, description='联系电话')
    email: str | None = Field(default=None, description='电子邮箱')
    address: str | None = Field(default=None, description='家庭住址')
    class_id: int | None = Field(default=None, description='班级 ID')
    status: int | None = Field(default=None, description='状态：0-禁用，1-正常')
    create_time: datetime | None = Field(default=None, description='创建时间')
    update_time: datetime | None = Field(default=None, description='更新时间')






class StudentsQueryModel(StudentsModel):
    """
    学生信息不分页查询模型
    """
    pass


class StudentsPageQueryModel(StudentsQueryModel):
    """
    学生信息分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteStudentsModel(BaseModel):
    """
    删除学生信息模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的主键 ID')
