from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from common.constant import CommonConstant

from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException

from module_admin.dao.list_dao import ListDao
from module_admin.entity.vo.list_vo import (
    DeleteListModel,
    ListModel,
    ListPageQueryModel,
)

from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class ListService:
    """

    设备清单模块服务层

    """

    @classmethod
    async def get_list_list_services(
        cls,
        query_db: AsyncSession,
        query_object: ListPageQueryModel,
        is_page: bool = False,
    ) -> PageModel | list[dict[str, Any]]:
        """

        获取设备清单列表信息 service

        :param query_db: orm 对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 设备清单列表信息对象

        """
        list_list_result = await ListDao.get_list_list(query_db, query_object, is_page)

        return list_list_result

    @classmethod
    async def add_list_services(
        cls, query_db: AsyncSession, page_object: ListModel
    ) -> CrudResponseModel:
        """

        新增设备清单信息 service

        :param query_db: orm 对象
        :param page_object: 新增设备清单对象
        :return: 新增设备清单校验结果

        """
        try:
            await ListDao.add_list_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message="新增成功")
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_list_services(
        cls, query_db: AsyncSession, page_object: ListModel
    ) -> CrudResponseModel:
        """

        编辑设备清单信息 service

        :param query_db: orm 对象
        :param page_object: 编辑设备清单对象
        :return: 编辑设备清单校验结果

        """
        edit_list = page_object.model_dump(
            exclude_unset=True,
            exclude={
                "create_time",
            },
        )
        list_info = await cls.list_detail_services(query_db, page_object.id)
        if list_info.id:
            try:
                await ListDao.edit_list_dao(query_db, edit_list)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message="更新成功")
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message="设备清单不存在")

    @classmethod
    async def delete_list_services(
        cls, query_db: AsyncSession, page_object: DeleteListModel
    ) -> CrudResponseModel:
        """

        删除设备清单信息 service

        :param query_db: orm 对象
        :param page_object: 删除设备清单对象
        :return: 删除设备清单校验结果

        """
        if page_object.ids:
            id_list = page_object.ids.split(",")
            try:
                for id in id_list:
                    await ListDao.delete_list_dao(query_db, ListModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message="删除成功")
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message="传入主键 ID 为空")

    @classmethod
    async def list_detail_services(cls, query_db: AsyncSession, id: int) -> ListModel:
        """

        获取设备清单详细信息 service

        :param query_db: orm 对象
        :param id: 主键 ID
        :return: 主键 ID 对应的信息

        """
        list = await ListDao.get_list_detail_by_id(query_db, id=id)
        result = (
            ListModel(**CamelCaseUtil.transform_result(list)) if list else ListModel()
        )

        return result

    @staticmethod
    async def export_list_list_services(list_list: list) -> bytes:
        """

        导出设备清单信息 service

        :param list_list: 设备清单信息列表
        :return: 设备清单信息对应 excel 的二进制数据

        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            "id": "主键 ID",
            "deviceCode": "设备编码",
            "deviceName": "设备名称",
            "deviceType": "设备类型",
            "brand": "品牌",
            "model": "型号",
            "serialNumber": "序列号",
            "purchaseDate": "购买日期",
            "warrantyPeriod": "保修期",
            "status": "状态",
            "location": "存放位置",
            "department": "所属部门",
            "responsiblePerson": "责任人",
            "remarks": "备注",
            "createTime": "创建时间",
            "updateTime": "更新时间",
        }
        binary_data = ExcelUtil.export_list2excel(list_list, mapping_dict)

        return binary_data

    @classmethod
    async def generate_random_list_services(
        cls, query_db: AsyncSession, count: int
    ) -> CrudResponseModel:
        """

        生成随机设备清单数据 service

        :param query_db: orm 对象
        :param count: 生成数据数量
        :return: 生成结果

        """
        import random
        import string
        from datetime import datetime, timedelta

        try:
            # 定义随机数据选项
            device_types = [
                "服务器",
                "路由器",
                "交换机",
                "打印机",
                "扫描仪",
                "投影仪",
                "电脑",
                "笔记本",
            ]
            brands = ["华为", "小米", "联想", "戴尔", "惠普", "苹果", "三星", "索尼"]
            locations = [
                "机房 A",
                "机房 B",
                "办公室 1",
                "办公室 2",
                "仓库",
                "会议室",
                "前台",
            ]
            departments = [
                "技术部",
                "行政部",
                "财务部",
                "人事部",
                "市场部",
                "销售部",
                "研发部",
            ]
            statuses = [0, 1, 2]  # 0-闲置，1-使用中，2-维修中

            for i in range(count):
                # 生成随机设备编码（DEV+6 位随机数字）
                device_code = "DEV" + "".join(random.choices(string.digits, k=6))

                # 生成随机设备名称
                device_type = random.choice(device_types)
                device_name = (
                    f"{random.choice(brands)}{device_type}{random.randint(1, 999)}"
                )

                # 生成随机型号
                model = "M-" + "".join(
                    random.choices(string.ascii_uppercase + string.digits, k=8)
                )

                # 生成随机序列号
                serial_number = "SN-" + "".join(
                    random.choices(string.ascii_uppercase + string.digits, k=12)
                )

                # 生成随机购买日期（最近 3 年内）
                start_date = datetime.now() - timedelta(days=365 * 3)
                random_days = random.randint(0, 365 * 3)
                purchase_date = start_date + timedelta(days=random_days)

                # 生成随机保修期（12-36 个月）
                warranty_period = random.randint(12, 36)

                # 生成随机状态
                status = random.choice(statuses)

                # 生成随机责任人
                responsible_person = random.choice(
                    ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十"]
                )

                # 创建设备对象
                device = ListModel(
                    device_code=device_code,
                    device_name=device_name,
                    device_type=device_type,
                    brand=random.choice(brands),
                    model=model,
                    serial_number=serial_number,
                    purchase_date=purchase_date.date(),
                    warranty_period=warranty_period,
                    status=status,
                    location=random.choice(locations),
                    department=random.choice(departments),
                    responsible_person=responsible_person,
                    remarks=f"随机生成的设备数据{i+1}",
                    create_time=datetime.now(),
                    update_time=datetime.now(),
                )

                # 插入数据库
                await ListDao.add_list_dao(query_db, device)

            await query_db.commit()
            return CrudResponseModel(
                is_success=True, message=f"成功生成{count}条随机设备数据"
            )
        except Exception as e:
            await query_db.rollback()
            raise e
