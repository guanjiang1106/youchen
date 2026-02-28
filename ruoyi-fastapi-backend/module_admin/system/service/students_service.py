from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from common.constant import CommonConstant
from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_admin.system.dao.students_dao import StudentsDao
from module_admin.system.entity.vo.students_vo import DeleteStudentsModel, StudentsModel, StudentsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class StudentsService:
    """
    学生信息模块服务层
    """

    @classmethod
    async def get_students_list_services(
        cls, query_db: AsyncSession, query_object: StudentsPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        获取学生信息列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 学生信息列表信息对象
        """
        students_list_result = await StudentsDao.get_students_list(query_db, query_object, is_page)

        return students_list_result


    @classmethod
    async def add_students_services(cls, query_db: AsyncSession, page_object: StudentsModel) -> CrudResponseModel:
        """
        新增学生信息信息service

        :param query_db: orm对象
        :param page_object: 新增学生信息对象
        :return: 新增学生信息校验结果
        """
        try:
            await StudentsDao.add_students_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_students_services(cls, query_db: AsyncSession, page_object: StudentsModel) -> CrudResponseModel:
        """
        编辑学生信息信息service

        :param query_db: orm对象
        :param page_object: 编辑学生信息对象
        :return: 编辑学生信息校验结果
        """
        edit_students = page_object.model_dump(exclude_unset=True, exclude={'create_time', })
        students_info = await cls.students_detail_services(query_db, page_object.id)
        if students_info.id:
            try:
                await StudentsDao.edit_students_dao(query_db, edit_students)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='学生信息不存在')

    @classmethod
    async def delete_students_services(cls, query_db: AsyncSession, page_object: DeleteStudentsModel) -> CrudResponseModel:
        """
        删除学生信息信息service

        :param query_db: orm对象
        :param page_object: 删除学生信息对象
        :return: 删除学生信息校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await StudentsDao.delete_students_dao(query_db, StudentsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键 ID为空')

    @classmethod
    async def students_detail_services(cls, query_db: AsyncSession, id: int) -> StudentsModel:
        """
        获取学生信息详细信息service

        :param query_db: orm对象
        :param id: 主键 ID
        :return: 主键 ID对应的信息
        """
        students = await StudentsDao.get_students_detail_by_id(query_db, id=id)
        result = StudentsModel(**CamelCaseUtil.transform_result(students)) if students else StudentsModel()

        return result

    @staticmethod
    async def export_students_list_services(students_list: list) -> bytes:
        """
        导出学生信息信息service

        :param students_list: 学生信息信息列表
        :return: 学生信息信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键 ID',
            'id': '主键 ID',
            'studentNo': '学号',
            'studentNo': '学号',
            'name': '姓名',
            'gender': '性别：0-未知，1-男，2-女',
            'birthDate': '出生日期',
            'phone': '联系电话',
            'email': '电子邮箱',
            'address': '家庭住址',
            'classId': '班级 ID',
            'status': '状态：0-禁用，1-正常',
            'createTime': '创建时间',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(students_list, mapping_dict)

        return binary_data
