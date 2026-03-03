from sqlalchemy import DateTime, Date, String, Column, SmallInteger, Integer, BigInteger, Text

from config.database import Base


class DeviceList(Base):
    """
    设备清单表
    """

    __tablename__ = 'device_list'
    __table_args__ = {'comment': '设备清单表'}

    id = Column(BigInteger, primary_key=True, nullable=False, comment='主键 ID')
    device_code = Column(String, nullable=True, comment='设备编码')
    device_name = Column(String, nullable=True, comment='设备名称')
    device_type = Column(String, nullable=True, comment='设备类型')
    brand = Column(String, nullable=True, comment='品牌')
    model = Column(String, nullable=True, comment='型号')
    serial_number = Column(String, nullable=True, comment='序列号')
    purchase_date = Column(Date, nullable=True, comment='购买日期')
    warranty_period = Column(Integer, nullable=True, comment='保修期（月）')
    status = Column(SmallInteger, nullable=True, comment='状态')
    location = Column(String, nullable=True, comment='存放位置')
    department = Column(String, nullable=True, comment='所属部门')
    responsible_person = Column(String, nullable=True, comment='责任人')
    remarks = Column(Text, nullable=True, comment='备注')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



