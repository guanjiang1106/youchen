from sqlalchemy import String, BigInteger, SmallInteger, Text, Column, Numeric, DateTime, Integer

from config.database import Base


class Process(Base):
    """
    工艺表
    """

    __tablename__ = 'process'
    __table_args__ = {'comment': '工艺表'}

    id = Column(BigInteger, primary_key=True, nullable=False, comment='主键 ID')
    id = Column(BigInteger, primary_key=True, nullable=False, comment='主键 ID')
    process_code = Column(String, primary_key=True, nullable=False, comment='工艺编码')
    process_name = Column(String, primary_key=True, nullable=False, comment='工艺名称')
    description = Column(Text, nullable=True, comment='工艺描述')
    sequence_order = Column(Integer, primary_key=True, nullable=False, comment='工序顺序')
    standard_time = Column(Numeric, nullable=True, comment='标准工时（分钟）')
    required_tooling = Column(String, nullable=True, comment='所需工装夹具')
    status = Column(SmallInteger, primary_key=True, nullable=False, comment='状态：1-启用，0-禁用')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



