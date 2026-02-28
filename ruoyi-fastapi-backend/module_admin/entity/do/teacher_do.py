from sqlalchemy import Date, BigInteger, SmallInteger, String, DateTime, Column

from config.database import Base


class Teacher(Base):
    """
    老师维护表
    """

    __tablename__ = 'teacher'
    __table_args__ = {'comment': '老师维护表'}

    id = Column(BigInteger, primary_key=True, nullable=False, comment='主键 ID')
    teacher_no = Column(String, nullable=False, comment='教师编号')
    name = Column(String, nullable=False, comment='姓名')
    gender = Column(SmallInteger, nullable=False, comment='性别：0-未知，1-男，2-女')
    birth_date = Column(Date, nullable=True, comment='出生日期')
    phone = Column(String, nullable=True, comment='联系电话')
    email = Column(String, nullable=True, comment='电子邮箱')
    department = Column(String, nullable=True, comment='所属部门')
    title = Column(String, nullable=True, comment='职称')
    status = Column(SmallInteger, nullable=False, comment='状态：0-禁用，1-启用')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



