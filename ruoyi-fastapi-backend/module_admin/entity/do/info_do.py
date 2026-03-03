from sqlalchemy import Column, BigInteger, Numeric, SmallInteger, Text, String, DateTime

from config.database import Base


class ProcessInfo(Base):
    """
    工艺信息表
    """

    __tablename__ = 'process_info'
    __table_args__ = {'comment': '工艺信息表'}

    id = Column(BigInteger, primary_key=True, nullable=False, comment='主键 ID')
    process_code = Column(String, nullable=True, comment='工艺编码')
    process_name = Column(String, nullable=True, comment='工艺名称')
    process_type = Column(SmallInteger, nullable=True, comment='工艺类型')
    description = Column(Text, nullable=True, comment='工艺描述')
    standard_hours = Column(Numeric, nullable=True, comment='标准工时')
    required_equipment = Column(String, nullable=True, comment='所需设备')
    operator_level = Column(SmallInteger, nullable=True, comment='操作员等级要求')
    status = Column(SmallInteger, nullable=True, comment='状态')
    version = Column(String, nullable=True, comment='版本号')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



