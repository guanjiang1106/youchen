from sqlalchemy import BigInteger, String, Column, Text, SmallInteger, Date, DateTime

from config.database import Base


class Students(Base):
    """
    学生信息表
    """

    __tablename__ = 'students'
    __table_args__ = {'comment': '学生信息表'}

    id = Column(BigInteger, primary_key=True, nullable=False, comment='主键 ID')
    id = Column(BigInteger, primary_key=True, nullable=False, comment='主键 ID')
    student_no = Column(String, primary_key=True, nullable=False, comment='学号')
    student_no = Column(String, primary_key=True, nullable=False, comment='学号')
    name = Column(String, primary_key=True, nullable=False, comment='姓名')
    gender = Column(SmallInteger, primary_key=True, nullable=False, comment='性别：0-未知，1-男，2-女')
    birth_date = Column(Date, nullable=True, comment='出生日期')
    phone = Column(String, nullable=True, comment='联系电话')
    email = Column(String, nullable=True, comment='电子邮箱')
    address = Column(Text, nullable=True, comment='家庭住址')
    class_id = Column(BigInteger, nullable=True, comment='班级 ID')
    status = Column(SmallInteger, primary_key=True, nullable=False, comment='状态：0-禁用，1-正常')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



