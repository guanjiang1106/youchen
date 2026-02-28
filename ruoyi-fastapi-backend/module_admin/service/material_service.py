from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from common.constant import CommonConstant
from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_admin.dao.material_dao import MaterialDao
from module_admin.entity.vo.material_vo import DeleteMaterialModel, MaterialModel, MaterialPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class MaterialService:
    """
    物料模块服务层
    """

    @classmethod
    async def get_material_list_services(
        cls, query_db: AsyncSession, query_object: MaterialPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        获取物料列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 物料列表信息对象
        """
        material_list_result = await MaterialDao.get_material_list(query_db, query_object, is_page)

        return material_list_result


    @classmethod
    async def add_material_services(cls, query_db: AsyncSession, page_object: MaterialModel) -> CrudResponseModel:
        """
        新增物料信息service

        :param query_db: orm对象
        :param page_object: 新增物料对象
        :return: 新增物料校验结果
        """
        try:
            await MaterialDao.add_material_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_material_services(cls, query_db: AsyncSession, page_object: MaterialModel) -> CrudResponseModel:
        """
        编辑物料信息service

        :param query_db: orm对象
        :param page_object: 编辑物料对象
        :return: 编辑物料校验结果
        """
        edit_material = page_object.model_dump(exclude_unset=True, exclude={'create_time', })
        material_info = await cls.material_detail_services(query_db, page_object.id)
        if material_info.id:
            try:
                await MaterialDao.edit_material_dao(query_db, edit_material)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='物料不存在')

    @classmethod
    async def delete_material_services(cls, query_db: AsyncSession, page_object: DeleteMaterialModel) -> CrudResponseModel:
        """
        删除物料信息service

        :param query_db: orm对象
        :param page_object: 删除物料对象
        :return: 删除物料校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await MaterialDao.delete_material_dao(query_db, MaterialModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键 ID为空')

    @classmethod
    async def material_detail_services(cls, query_db: AsyncSession, id: int) -> MaterialModel:
        """
        获取物料详细信息service

        :param query_db: orm对象
        :param id: 主键 ID
        :return: 主键 ID对应的信息
        """
        material = await MaterialDao.get_material_detail_by_id(query_db, id=id)
        result = MaterialModel(**CamelCaseUtil.transform_result(material)) if material else MaterialModel()

        return result

    @staticmethod
    async def export_material_list_services(material_list: list) -> bytes:
        """
        导出物料信息service

        :param material_list: 物料信息列表
        :return: 物料信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键 ID',
            'materialCode': '物料编码',
            'materialName': '物料名称',
            'specification': '规格型号',
            'unit': '计量单位',
            'categoryId': '分类 ID',
            'stockQuantity': '库存数量',
            'safetyStock': '安全库存',
            'price': '参考单价',
            'status': '状态：1-启用，0-禁用',
            'remark': '备注',
            'createTime': '创建时间',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(material_list, mapping_dict)

        return binary_data
