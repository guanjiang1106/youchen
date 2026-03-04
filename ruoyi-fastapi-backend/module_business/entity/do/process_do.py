from sqlalchemy import Column, BigInteger, Integer, SmallInteger, Text, String, DateTime

from config.database import Base


class Process(Base):
    """
    工艺表
    """

    __tablename__ = 'process'
    __table_args__ = {'comment': '工艺表'}

    id = Column(BigInteger, primary_key=True, nullable=False, comment='主键 ID')
    process_code = Column(String, nullable=True, comment='工艺编码')
    process_name = Column(String, nullable=True, comment='工艺名称')
    description = Column(Text, nullable=True, comment='工艺描述')
    category = Column(String, nullable=True, comment='工艺分类')
    version = Column(String, nullable=True, comment='版本号')
    status = Column(SmallInteger, nullable=True, comment='状态')
    sort_order = Column(Integer, nullable=True, comment='排序顺序')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



