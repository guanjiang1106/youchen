from sqlalchemy import Text, DateTime, SmallInteger, Column, BigInteger, Numeric, String

from config.database import Base


class Material(Base):
    """
    物料表
    """

    __tablename__ = 'material'
    __table_args__ = {'comment': '物料表'}

    id = Column(BigInteger, primary_key=True, nullable=False, comment='主键 ID')
    material_code = Column(String, nullable=True, comment='物料编码')
    material_name = Column(String, nullable=True, comment='物料名称')
    specification = Column(String, nullable=True, comment='规格型号')
    unit = Column(String, nullable=True, comment='计量单位')
    category_id = Column(BigInteger, nullable=True, comment='分类 ID')
    stock_quantity = Column(Numeric, nullable=True, comment='库存数量')
    safety_stock = Column(Numeric, nullable=True, comment='安全库存')
    price = Column(Numeric, nullable=True, comment='参考单价')
    status = Column(SmallInteger, nullable=True, comment='状态：1-启用，0-禁用')
    remark = Column(Text, nullable=True, comment='备注')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



