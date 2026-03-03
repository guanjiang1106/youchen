from typing import Any

import random

import string
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from common.constant import CommonConstant

from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException

from module_admin.dao.table_dao import TableDao
from module_admin.entity.vo.table_vo import (
    DeleteTableModel,
    TableModel,
    TablePageQueryModel,
)

from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class TableService:
    """

    质量检验记录模块服务层

    """

    @classmethod
    async def get_table_list_services(
        cls,
        query_db: AsyncSession,
        query_object: TablePageQueryModel,
        is_page: bool = False,
    ) -> PageModel | list[dict[str, Any]]:
        """

        获取质量检验记录列表信息 service

        :param query_db: orm 对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 质量检验记录列表信息对象

        """
        table_list_result = await TableDao.get_table_list(
            query_db, query_object, is_page
        )

        return table_list_result

    @classmethod
    async def add_table_services(
        cls, query_db: AsyncSession, page_object: TableModel
    ) -> CrudResponseModel:
        """

        新增质量检验记录信息 service

        :param query_db: orm 对象
        :param page_object: 新增质量检验记录对象
        :return: 新增质量检验记录校验结果

        """
        try:
            await TableDao.add_table_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message="新增成功")
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_table_services(
        cls, query_db: AsyncSession, page_object: TableModel
    ) -> CrudResponseModel:
        """

        编辑质量检验记录信息 service

        :param query_db: orm 对象
        :param page_object: 编辑质量检验记录对象
        :return: 编辑质量检验记录校验结果

        """
        edit_table = page_object.model_dump(
            exclude_unset=True,
            exclude={
                "create_time",
            },
        )
        table_info = await cls.table_detail_services(query_db, page_object.id)
        if table_info.id:
            try:
                await TableDao.edit_table_dao(query_db, edit_table)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message="更新成功")
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message="质量检验记录不存在")

    @classmethod
    async def delete_table_services(
        cls, query_db: AsyncSession, page_object: DeleteTableModel
    ) -> CrudResponseModel:
        """

        删除质量检验记录信息 service

        :param query_db: orm 对象
        :param page_object: 删除质量检验记录对象
        :return: 删除质量检验记录校验结果

        """
        if page_object.ids:
            id_list = page_object.ids.split(",")
            try:
                for id in id_list:
                    await TableDao.delete_table_dao(query_db, TableModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message="删除成功")
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message="传入主键 ID 为空")

    @classmethod
    async def table_detail_services(cls, query_db: AsyncSession, id: int) -> TableModel:
        """

        获取质量检验记录详细信息 service

        :param query_db: orm 对象
        :param id: 主键 ID
        :return: 主键 ID 对应的信息

        """
        table = await TableDao.get_table_detail_by_id(query_db, id=id)
        result = (
            TableModel(**CamelCaseUtil.transform_result(table))
            if table
            else TableModel()
        )

        return result

    @staticmethod
    async def export_table_list_services(table_list: list) -> bytes:
        """

        导出质量检验记录信息 service

        :param table_list: 质量检验记录信息列表
        :return: 质量检验记录信息对应 excel 的二进制数据

        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            "id": "主键 ID",
            "productCode": "产品编码",
            "batchNumber": "生产批次号",
            "inspectionResult": "检验结果 (0:待检，1:合格，2:不合格)",
            "defectCount": "缺陷数量",
            "inspectorName": "检验员姓名",
            "remarks": "备注说明",
            "createTime": "创建时间",
            "updateTime": "更新时间",
        }
        binary_data = ExcelUtil.export_list2excel(table_list, mapping_dict)

        return binary_data

    @classmethod
    async def generate_random_data_services(
        cls, query_db: AsyncSession
    ) -> CrudResponseModel:
        """

        生成随机质量检验记录数据 service

        :param query_db: orm 对象
        :return: 生成结果校验结果

        """
        try:
            # 生成 10 条随机数据
            random_count = 10
            inspectors = ["张三", "李四", "王五", "赵六", "钱七"]

            for _ in range(random_count):
                # 生成随机产品编码 (格式：PROD-XXXX)
                product_code = "PROD-" + "".join(random.choices(string.digits, k=4))

                # 生成随机批次号 (格式：BATCH-YYYYMMDD-XXX)
                batch_number = (
                    "BATCH-"
                    + datetime.now().strftime("%Y%m%d")
                    + "-"
                    + "".join(random.choices(string.digits, k=3))
                )

                # 随机检验结果 (0:待检，1:合格，2:不合格)
                inspection_result = str(random.randint(0, 2))

                # 随机缺陷数量 (0-10)
                defect_count = random.randint(0, 10)

                # 随机检验员
                inspector_name = random.choice(inspectors)

                # 随机备注
                remarks = f"自动生成的测试数据-{random.randint(1000, 9999)}"

                # 创建数据对象
                random_data = TableModel(
                    productCode=product_code,
                    batchNumber=batch_number,
                    inspectionResult=inspection_result,
                    defectCount=defect_count,
                    inspectorName=inspector_name,
                    remarks=remarks,
                    createTime=datetime.now(),
                    updateTime=datetime.now(),
                )

                # 插入数据库
                await TableDao.add_table_dao(query_db, random_data)

            await query_db.commit()
            return CrudResponseModel(
                is_success=True, message=f"成功生成{random_count}条随机数据"
            )
        except Exception as e:
            await query_db.rollback()
            raise e
