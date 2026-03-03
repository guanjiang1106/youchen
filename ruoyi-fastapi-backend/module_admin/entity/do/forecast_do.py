from sqlalchemy import Numeric, SmallInteger, String, BigInteger, Column, Date, DateTime

from config.database import Base


class SalesForecast(Base):
    """
    销售预测，存储各产品在各区域的销售预测数据表
    """

    __tablename__ = 'sales_forecast'
    __table_args__ = {'comment': '销售预测表，存储各产品在各区域的销售预测数据'}

    id = Column(BigInteger, primary_key=True, nullable=False, comment='主键 ID，自增序列')
    product_id = Column(BigInteger, nullable=False, comment='关联的产品 ID')
    region_code = Column(String, nullable=False, comment='区域代码，标识销售区域')
    forecast_date = Column(Date, nullable=False, comment='预测日期，指预测对应的业务日期')
    predicted_amount = Column(Numeric, nullable=False, comment='预测销售额，单位为元')
    confidence_level = Column(SmallInteger, nullable=False, comment='置信度等级，0-100 表示预测的可信程度')
    model_version = Column(String, nullable=True, comment='生成该预测的算法模型版本')
    created_at = Column(DateTime, nullable=True, comment='记录创建时间')
    updated_at = Column(DateTime, nullable=True, comment='记录最后更新时间')



