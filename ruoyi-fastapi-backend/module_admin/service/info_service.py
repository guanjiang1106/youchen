from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from common.constant import CommonConstant

from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException

from module_admin.dao.info_dao import InfoDao
from module_admin.entity.vo.info_vo import DeleteInfoModel, InfoModel, InfoPageQueryModel

from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil

class InfoService:
    """

    工艺信息模块服务层
    
"""

    @classmethod
    async def get_info_list_services(
        cls, query_db: AsyncSession, query_object: InfoPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """

        获取工艺信息列表信息 service

        :param query_db: orm 对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 工艺信息列表信息对象
        
"""
        info_list_result = await InfoDao.get_info_list(query_db, query_object, is_page)

        return info_list_result

    @classmethod
    async def add_info_services(cls, query_db: AsyncSession, page_object: InfoModel) -> CrudResponseModel:
        """

        新增工艺信息信息 service

        :param query_db: orm 对象
        :param page_object: 新增工艺信息对象
        :return: 新增工艺信息校验结果
        
"""
        try:
            await InfoDao.add_info_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_info_services(cls, query_db: AsyncSession, page_object: InfoModel) -> CrudResponseModel:
        """

        编辑工艺信息信息 service

        :param query_db: orm 对象
        :param page_object: 编辑工艺信息对象
        :return: 编辑工艺信息校验结果
        
"""
        edit_info = page_object.model_dump(exclude_unset=True, exclude={'create_time', })
        info_info = await cls.info_detail_services(query_db, page_object.id)
        if info_info.id:
            try:
                await InfoDao.edit_info_dao(query_db, edit_info)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='工艺信息不存在')

    @classmethod
    async def delete_info_services(cls, query_db: AsyncSession, page_object: DeleteInfoModel) -> CrudResponseModel:
        """

        删除工艺信息信息 service

        :param query_db: orm 对象
        :param page_object: 删除工艺信息对象
        :return: 删除工艺信息校验结果
        
"""
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await InfoDao.delete_info_dao(query_db, InfoModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键 ID 为空')

    @classmethod
    async def info_detail_services(cls, query_db: AsyncSession, id: int) -> InfoModel:
        """

        获取工艺信息详细信息 service

        :param query_db: orm 对象
        :param id: 主键 ID
        :return: 主键 ID 对应的信息
        
"""
        info = await InfoDao.get_info_detail_by_id(query_db, id=id)
        result = InfoModel(**CamelCaseUtil.transform_result(info)) if info else InfoModel()

        return result

    @staticmethod
    async def export_info_list_services(info_list: list) -> bytes:
        """

        导出工艺信息信息 service

        :param info_list: 工艺信息信息列表
        :return: 工艺信息信息对应 excel 的二进制数据
        
"""
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键 ID',
            'processCode': '工艺编码',
            'processName': '工艺名称',
            'processType': '工艺类型',
            'description': '工艺描述',
            'standardHours': '标准工时',
            'requiredEquipment': '所需设备',
            'operatorLevel': '操作员等级要求',
            'status': '状态',
            'version': '版本号',
            'createTime': '创建时间',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(info_list, mapping_dict)

        return binary_data

    @classmethod
    async def generate_random_data_services(cls, query_db: AsyncSession, count: int) -> CrudResponseModel:
        """

        生成随机工艺信息数据 service

        :param query_db: orm 对象
        :param count: 生成数据数量
        :return: 生成结果
        
"""
        import random
        import string
        from datetime import datetime
        from decimal import Decimal

        try:
            # 定义随机数据选项
            process_types = [1, 2, 3]
            statuses = ['0', '1']
            equipment_list = ['数控机床', '激光切割机', '焊接机器人', '注塑机', '冲压机', '装配线']
            descriptions = [
                '精密加工工艺，适用于高精度零件制造',
                '批量生产工艺，适用于大规模生产',
                '特殊材料处理工艺，需要专业设备',
                '自动化生产线工艺，效率高成本低',
                '手工精细加工工艺，适用于小批量定制'
            ]
            versions = ['V1.0', 'V1.1', 'V2.0', 'V2.1', 'V3.0']

            now = datetime.now()

            for i in range(count):
                # 生成工艺编码：PROC + 随机数字
                process_code = 'PROC' + ''.join(random.choices(string.digits, k=6))

                # 生成工艺名称
                process_name = f'工艺_{random.choice(["A", "B", "C", "D", "E"])}_{random.randint(100, 999)}'

                # 随机选择工艺类型
                process_type = random.choice(process_types)

                # 随机选择描述
                description = random.choice(descriptions)

                # 生成标准工时 (0.5 到 100 之间)
                standard_hours = Decimal(str(round(random.uniform(0.5, 100.0), 2)))

                # 随机选择所需设备 (1-3 个)
                required_equipment = ','.join(random.sample(equipment_list, random.randint(1, 3)))

                # 随机操作员等级 (1-5)
                operator_level = random.randint(1, 5)

                # 随机状态
                status = random.choice(statuses)

                # 随机版本号
                version = random.choice(versions)

                # 创建工艺信息对象
                info = InfoModel(
                    process_code=process_code,
                    process_name=process_name,
                    process_type=process_type,
                    description=description,
                    standard_hours=standard_hours,
                    required_equipment=required_equipment,
                    operator_level=operator_level,
                    status=status,
                    version=version,
                    create_time=now,
                    update_time=now,
                )

                # 插入数据库
                await InfoDao.add_info_dao(query_db, info)

            await query_db.commit()
            return CrudResponseModel(is_success=True, message=f'成功生成{count}条随机工艺信息数据')
        except Exception as e:
            await query_db.rollback()
            raise e