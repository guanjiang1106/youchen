from typing import Any

from fastapi import Request

from sqlalchemy.ext.asyncio import AsyncSession

from common.constant import CommonConstant

from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException

from module_admin.dao.teacher_dao import TeacherDao
from module_admin.entity.vo.teacher_vo import DeleteTeacherModel, TeacherModel, TeacherPageQueryModel

from module_admin.service.dict_service import DictDataService
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

        获取老师维护列表信息 service

        :param query_db: orm 对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 老师维护列表信息对象
        
"""
        teacher_list_result = await TeacherDao.get_teacher_list(query_db, query_object, is_page)

        return teacher_list_result

    @classmethod
    async def add_teacher_services(cls, query_db: AsyncSession, page_object: TeacherModel) -> CrudResponseModel:
        """

        新增老师维护信息 service

        :param query_db: orm 对象
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

        编辑老师维护信息 service

        :param query_db: orm 对象
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

        删除老师维护信息 service

        :param query_db: orm 对象
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
            raise ServiceException(message='传入主键 ID 为空')

    @classmethod
    async def teacher_detail_services(cls, query_db: AsyncSession, id: int) -> TeacherModel:
        """

        获取老师维护详细信息 service

        :param query_db: orm 对象
        :param id: 主键 ID
        :return: 主键 ID 对应的信息
        
"""
        teacher = await TeacherDao.get_teacher_detail_by_id(query_db, id=id)
        result = TeacherModel(**CamelCaseUtil.transform_result(teacher)) if teacher else TeacherModel()

        return result

    @staticmethod
    async def export_teacher_list_services(request: Request, teacher_list: list) -> bytes:
        """

        导出老师维护信息 service

        :param teacher_list: 老师维护信息列表
        :return: 老师维护信息对应 excel 的二进制数据
        
"""
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键 ID',
            'teacherNo': '教师编号',
            'name': '姓名',
            'gender': '性别',
            'birthDate': '出生日期',
            'phone': '联系电话',
            'email': '电子邮箱',
            'department': '所属部门',
            'title': '职称',
            'status': '状态',
            'createTime': '创建时间',
            'updateTime': '更新时间',
        }
        sys_user_sex_list = await DictDataService.query_dict_data_list_from_cache_services(
            request.app.state.redis, dict_type='sys_user_sex'
        )
        sys_user_sex_option = [{'label': item.get('dictLabel'), 'value': item.get('dictValue')} for item in sys_user_sex_list]
        sys_user_sex_option_dict = {item.get('value'): item for item in sys_user_sex_option}
        for item in teacher_list:
            if str(item.get('gender')) in sys_user_sex_option_dict:
                item['gender'] = sys_user_sex_option_dict.get(str(item.get('gender'))).get('label')
            if str(item.get('status')) in sys_user_sex_option_dict:
                item['status'] = sys_user_sex_option_dict.get(str(item.get('status'))).get('label')
        binary_data = ExcelUtil.export_list2excel(teacher_list, mapping_dict)

        return binary_data

    @classmethod
    async def generate_random_teacher_services(cls, query_db: AsyncSession, count: int) -> CrudResponseModel:
        """

        随机生成老师维护数据 service

        :param query_db: orm 对象
        :param count: 生成数据数量
        :return: 生成结果
        
"""
        import random
        import string
        from datetime import datetime, timedelta

        try:
            # 定义随机数据源
            first_names = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨']
            last_names = ['伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '军', '洋', '勇', '艳', '杰', '娟', '涛']
            departments = ['计算机学院', '数学学院', '物理学院', '化学学院', '生物学院', '文学院', '历史学院', '哲学院']
            titles = ['助教', '讲师', '副教授', '教授', '特聘教授']
            
            # 性别选项：0-女，1-男
            genders = [0, 1]
            # 状态选项：0-停用，1-正常
            statuses = [0, 1]

            for i in range(count):
                # 生成教师编号：T + 6 位随机数字
                teacher_no = 'T' + ''.join(random.choices(string.digits, k=6))
                
                # 生成姓名
                name = random.choice(first_names) + random.choice(last_names)
                
                # 生成性别
                gender = random.choice(genders)
                
                # 生成出生日期（1960-2000 年之间）
                start_date = datetime(1960, 1, 1)
                end_date = datetime(2000, 12, 31)
                delta = end_date - start_date
                random_days = random.randint(0, delta.days)
                birth_date = start_date + timedelta(days=random_days)
                
                # 生成联系电话：13/14/15/17/18/19 + 9 位数字
                phone_prefix = random.choice(['13', '14', '15', '17', '18', '19'])
                phone = phone_prefix + ''.join(random.choices(string.digits, k=9))
                
                # 生成邮箱
                email_domains = ['example.com', 'school.edu.cn', 'university.edu.cn']
                email = f"{teacher_no.lower()}@{random.choice(email_domains)}"
                
                # 生成部门
                department = random.choice(departments)
                
                # 生成职称
                title = random.choice(titles)
                
                # 生成状态
                status = random.choice(statuses)
                
                # 创建时间
                create_time = datetime.now()
                update_time = datetime.now()
                
                # 构建教师对象
                teacher = TeacherModel(
                    teacher_no=teacher_no,
                    name=name,
                    gender=gender,
                    birth_date=birth_date.date(),
                    phone=phone,
                    email=email,
                    department=department,
                    title=title,
                    status=status,
                    create_time=create_time,
                    update_time=update_time,
                )
                
                # 插入数据库
                await TeacherDao.add_teacher_dao(query_db, teacher)
            
            await query_db.commit()
            return CrudResponseModel(is_success=True, message=f'成功生成{count}条随机数据')
        except Exception as e:
            await query_db.rollback()
            raise e