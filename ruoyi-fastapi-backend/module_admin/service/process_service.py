from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from common.constant import CommonConstant
from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_admin.dao.process_dao import ProcessDao
from module_admin.entity.vo.process_vo import DeleteProcessModel, ProcessModel, ProcessPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class ProcessService:
    """
    工艺模块服务层
    """

    @classmethod
    async def get_process_list_services(
        cls, query_db: AsyncSession, query_object: ProcessPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        获取工艺列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 工艺列表信息对象
        """
        process_list_result = await ProcessDao.get_process_list(query_db, query_object, is_page)

        return process_list_result


    @classmethod
    async def add_process_services(cls, query_db: AsyncSession, page_object: ProcessModel) -> CrudResponseModel:
        """
        新增工艺信息service

        :param query_db: orm对象
        :param page_object: 新增工艺对象
        :return: 新增工艺校验结果
        """
        try:
            await ProcessDao.add_process_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_process_services(cls, query_db: AsyncSession, page_object: ProcessModel) -> CrudResponseModel:
        """
        编辑工艺信息service

        :param query_db: orm对象
        :param page_object: 编辑工艺对象
        :return: 编辑工艺校验结果
        """
        edit_process = page_object.model_dump(exclude_unset=True, exclude={'create_time', })
        process_info = await cls.process_detail_services(query_db, page_object.id)
        if process_info.id:
            try:
                await ProcessDao.edit_process_dao(query_db, edit_process)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='工艺不存在')

    @classmethod
    async def delete_process_services(cls, query_db: AsyncSession, page_object: DeleteProcessModel) -> CrudResponseModel:
        """
        删除工艺信息service

        :param query_db: orm对象
        :param page_object: 删除工艺对象
        :return: 删除工艺校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await ProcessDao.delete_process_dao(query_db, ProcessModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键 ID为空')

    @classmethod
    async def process_detail_services(cls, query_db: AsyncSession, id: int) -> ProcessModel:
        """
        获取工艺详细信息service

        :param query_db: orm对象
        :param id: 主键 ID
        :return: 主键 ID对应的信息
        """
        process = await ProcessDao.get_process_detail_by_id(query_db, id=id)
        result = ProcessModel(**CamelCaseUtil.transform_result(process)) if process else ProcessModel()

        return result

    @staticmethod
    async def export_process_list_services(process_list: list) -> bytes:
        """
        导出工艺信息service

        :param process_list: 工艺信息列表
        :return: 工艺信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键 ID',
            'id': '主键 ID',
            'processCode': '工艺编码',
            'processName': '工艺名称',
            'description': '工艺描述',
            'sequenceOrder': '工序顺序',
            'standardTime': '标准工时',
            'requiredTooling': '所需工装夹具',
            'status': '状态：1-启用，0-禁用',
            'createTime': '创建时间',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(process_list, mapping_dict)

        return binary_data
