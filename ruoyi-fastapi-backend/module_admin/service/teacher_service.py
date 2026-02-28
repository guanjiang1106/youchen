from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from common.constant import CommonConstant
from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_admin.dao.teacher_dao import TeacherDao
from module_admin.entity.vo.teacher_vo import DeleteTeacherModel, TeacherModel, TeacherPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class TeacherService:
    """
    老师维护模块服务层
    """

    @classmethod
    async def get_teacher_list_services(
        cls, query_db: AsyncSession, query_object: TeacherPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        获取老师维护列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 老师维护列表信息对象
        """
        teacher_list_result = await TeacherDao.get_teacher_list(query_db, query_object, is_page)

        return teacher_list_result


    @classmethod
    async def add_teacher_services(cls, query_db: AsyncSession, page_object: TeacherModel) -> CrudResponseModel:
        """
        新增老师维护信息service

        :param query_db: orm对象
        :param page_object: 新增老师维护对象
        :return: 新增老师维护校验结果
        """
        try:
            await TeacherDao.add_teacher_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_teacher_services(cls, query_db: AsyncSession, page_object: TeacherModel) -> CrudResponseModel:
        """
        编辑老师维护信息service

        :param query_db: orm对象
        :param page_object: 编辑老师维护对象
        :return: 编辑老师维护校验结果
        """
        edit_teacher = page_object.model_dump(exclude_unset=True, exclude={'create_time', })
        teacher_info = await cls.teacher_detail_services(query_db, page_object.id)
        if teacher_info.id:
            try:
                await TeacherDao.edit_teacher_dao(query_db, edit_teacher)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='老师维护不存在')

    @classmethod
    async def delete_teacher_services(cls, query_db: AsyncSession, page_object: DeleteTeacherModel) -> CrudResponseModel:
        """
        删除老师维护信息service

        :param query_db: orm对象
        :param page_object: 删除老师维护对象
        :return: 删除老师维护校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await TeacherDao.delete_teacher_dao(query_db, TeacherModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键 ID为空')

    @classmethod
    async def teacher_detail_services(cls, query_db: AsyncSession, id: int) -> TeacherModel:
        """
        获取老师维护详细信息service

        :param query_db: orm对象
        :param id: 主键 ID
        :return: 主键 ID对应的信息
        """
        teacher = await TeacherDao.get_teacher_detail_by_id(query_db, id=id)
        result = TeacherModel(**CamelCaseUtil.transform_result(teacher)) if teacher else TeacherModel()

        return result

    @staticmethod
    async def export_teacher_list_services(teacher_list: list) -> bytes:
        """
        导出老师维护信息service

        :param teacher_list: 老师维护信息列表
        :return: 老师维护信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键 ID',
            'id': '主键 ID',
            'teacherNo': '教师编号',
            'name': '姓名',
            'gender': '性别：0-未知，1-男，2-女',
            'birthDate': '出生日期',
            'phone': '联系电话',
            'email': '电子邮箱',
            'department': '所属部门',
            'title': '职称',
            'status': '状态：0-禁用，1-启用',
            'createTime': '创建时间',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(teacher_list, mapping_dict)

        return binary_data
