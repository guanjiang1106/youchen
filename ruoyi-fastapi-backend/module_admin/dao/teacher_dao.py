from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_admin.entity.do.teacher_do import Teacher
from module_admin.entity.vo.teacher_vo import TeacherModel, TeacherPageQueryModel
from utils.page_util import PageUtil


class TeacherDao:
    """
    老师维护模块数据库操作层
    """

    @classmethod
    async def get_teacher_detail_by_id(cls, db: AsyncSession, id: int) -> Teacher | None:
        """
        根据主键 ID获取老师维护详细信息

        :param db: orm对象
        :param id: 主键 ID
        :return: 老师维护信息对象
        """
        teacher_info = (
            (
                await db.execute(
                    select(Teacher)
                    .where(
                        Teacher.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return teacher_info

    @classmethod
    async def get_teacher_detail_by_info(cls, db: AsyncSession, teacher: TeacherModel) -> Teacher | None:
        """
        根据老师维护参数获取老师维护信息

        :param db: orm对象
        :param teacher: 老师维护参数对象
        :return: 老师维护信息对象
        """
        teacher_info = (
            (
                await db.execute(
                    select(Teacher).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return teacher_info

    @classmethod
    async def get_teacher_list(
        cls, db: AsyncSession, query_object: TeacherPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        根据查询参数获取老师维护列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 老师维护列表信息对象
        """
        query = (
            select(Teacher)
            .where(
                Teacher.teacher_no == query_object.teacher_no if query_object.teacher_no else True,
                Teacher.name.like(f'%{query_object.name}%') if query_object.name else True,
                Teacher.gender == query_object.gender if query_object.gender else True,
                Teacher.birth_date == query_object.birth_date if query_object.birth_date else True,
                Teacher.phone == query_object.phone if query_object.phone else True,
                Teacher.email == query_object.email if query_object.email else True,
                Teacher.department == query_object.department if query_object.department else True,
                Teacher.title == query_object.title if query_object.title else True,
                Teacher.status == query_object.status if query_object.status else True,
            )
            .order_by(Teacher.id)
            .distinct()
        )
        teacher_list: PageModel | list[dict[str, Any]] = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )

        return teacher_list

    @classmethod
    async def add_teacher_dao(cls, db: AsyncSession, teacher: TeacherModel) -> Teacher:
        """
        新增老师维护数据库操作

        :param db: orm对象
        :param teacher: 老师维护对象
        :return:
        """
        db_teacher = Teacher(**teacher.model_dump(exclude={}))
        db.add(db_teacher)
        await db.flush()

        return db_teacher

    @classmethod
    async def edit_teacher_dao(cls, db: AsyncSession, teacher: dict) -> None:
        """
        编辑老师维护数据库操作

        :param db: orm对象
        :param teacher: 需要更新的老师维护字典
        :return:
        """
        await db.execute(update(Teacher), [teacher])

    @classmethod
    async def delete_teacher_dao(cls, db: AsyncSession, teacher: TeacherModel) -> None:
        """
        删除老师维护数据库操作

        :param db: orm对象
        :param teacher: 老师维护对象
        :return:
        """
        await db.execute(delete(Teacher).where(Teacher.id.in_([teacher.id])))

