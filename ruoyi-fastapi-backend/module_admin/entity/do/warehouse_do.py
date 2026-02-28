from sqlalchemy import BigInteger, DateTime, SmallInteger, Column, Text, Numeric, String

from config.database import Base


class Warehouse(Base):
    """
    仓库表
    """

    __tablename__ = 'warehouse'
    __table_args__ = {'comment': '仓库表'}

    id = Column(BigInteger, primary_key=True, nullable=False, comment='主键 ID')
    id = Column(BigInteger, primary_key=True, nullable=False, comment='主键 ID')
    code = Column(String, primary_key=True, nullable=False, comment='仓库编码')
    name = Column(String, primary_key=True, nullable=False, comment='仓库名称')
    address = Column(Text, nullable=True, comment='仓库地址')
    contact_person = Column(String, nullable=True, comment='联系人')
    contact_phone = Column(String, nullable=True, comment='联系电话')
    capacity = Column(Numeric, nullable=True, comment='仓库容量')
    status = Column(SmallInteger, primary_key=True, nullable=False, comment='状态：1-启用，0-禁用')
    remark = Column(Text, nullable=True, comment='备注')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



