from sqlalchemy import Integer, BigInteger, SmallInteger, String, DateTime, Column, Text

from config.database import Base


class QualityTable(Base):
    """
    质量检验记录表
    """

    __tablename__ = 'quality_table'
    __table_args__ = {'comment': '质量检验记录表'}

    id = Column(BigInteger, primary_key=True, nullable=False, comment='主键 ID')
    product_code = Column(String, nullable=False, comment='产品编码')
    batch_number = Column(String, nullable=False, comment='生产批次号')
    inspection_result = Column(SmallInteger, nullable=False, comment='检验结果 (0:待检，1:合格，2:不合格)')
    defect_count = Column(Integer, nullable=False, comment='缺陷数量')
    inspector_name = Column(String, nullable=True, comment='检验员姓名')
    remarks = Column(Text, nullable=True, comment='备注说明')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



