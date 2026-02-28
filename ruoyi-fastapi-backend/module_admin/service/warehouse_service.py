from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from common.constant import CommonConstant
from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_admin.dao.warehouse_dao import WarehouseDao
from module_admin.entity.vo.warehouse_vo import DeleteWarehouseModel, WarehouseModel, WarehousePageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class WarehouseService:
    """
    仓库模块服务层
    """

    @classmethod
    async def get_warehouse_list_services(
        cls, query_db: AsyncSession, query_object: WarehousePageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        获取仓库列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 仓库列表信息对象
        """
        warehouse_list_result = await WarehouseDao.get_warehouse_list(query_db, query_object, is_page)

        return warehouse_list_result


    @classmethod
    async def add_warehouse_services(cls, query_db: AsyncSession, page_object: WarehouseModel) -> CrudResponseModel:
        """
        新增仓库信息service

        :param query_db: orm对象
        :param page_object: 新增仓库对象
        :return: 新增仓库校验结果
        """
        try:
            await WarehouseDao.add_warehouse_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_warehouse_services(cls, query_db: AsyncSession, page_object: WarehouseModel) -> CrudResponseModel:
        """
        编辑仓库信息service

        :param query_db: orm对象
        :param page_object: 编辑仓库对象
        :return: 编辑仓库校验结果
        """
        edit_warehouse = page_object.model_dump(exclude_unset=True, exclude={'create_time', })
        warehouse_info = await cls.warehouse_detail_services(query_db, page_object.id)
        if warehouse_info.id:
            try:
                await WarehouseDao.edit_warehouse_dao(query_db, edit_warehouse)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='仓库不存在')

    @classmethod
    async def delete_warehouse_services(cls, query_db: AsyncSession, page_object: DeleteWarehouseModel) -> CrudResponseModel:
        """
        删除仓库信息service

        :param query_db: orm对象
        :param page_object: 删除仓库对象
        :return: 删除仓库校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await WarehouseDao.delete_warehouse_dao(query_db, WarehouseModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键 ID为空')

    @classmethod
    async def warehouse_detail_services(cls, query_db: AsyncSession, id: int) -> WarehouseModel:
        """
        获取仓库详细信息service

        :param query_db: orm对象
        :param id: 主键 ID
        :return: 主键 ID对应的信息
        """
        warehouse = await WarehouseDao.get_warehouse_detail_by_id(query_db, id=id)
        result = WarehouseModel(**CamelCaseUtil.transform_result(warehouse)) if warehouse else WarehouseModel()

        return result

    @staticmethod
    async def export_warehouse_list_services(warehouse_list: list) -> bytes:
        """
        导出仓库信息service

        :param warehouse_list: 仓库信息列表
        :return: 仓库信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键 ID',
            'id': '主键 ID',
            'code': '仓库编码',
            'name': '仓库名称',
            'address': '仓库地址',
            'contactPerson': '联系人',
            'contactPhone': '联系电话',
            'capacity': '仓库容量',
            'status': '状态：1-启用，0-禁用',
            'remark': '备注',
            'createTime': '创建时间',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(warehouse_list, mapping_dict)

        return binary_data
