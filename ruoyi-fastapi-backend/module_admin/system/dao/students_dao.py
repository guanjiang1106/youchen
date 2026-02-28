from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_admin.system.entity.do.students_do import Students
from module_admin.system.entity.vo.students_vo import StudentsModel, StudentsPageQueryModel
from utils.page_util import PageUtil


class StudentsDao:
    """
    学生信息模块数据库操作层
    """

    @classmethod
    async def get_students_detail_by_id(cls, db: AsyncSession, id: int) -> Students | None:
        """
        根据主键 ID获取学生信息详细信息

        :param db: orm对象
        :param id: 主键 ID
        :return: 学生信息信息对象
        """
        students_info = (
            (
                await db.execute(
                    select(Students)
                    .where(
                        Students.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return students_info

    @classmethod
    async def get_students_detail_by_info(cls, db: AsyncSession, students: StudentsModel) -> Students | None:
        """
        根据学生信息参数获取学生信息信息

        :param db: orm对象
        :param students: 学生信息参数对象
        :return: 学生信息信息对象
        """
        students_info = (
            (
                await db.execute(
                    select(Students).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return students_info

    @classmethod
    async def get_students_list(
        cls, db: AsyncSession, query_object: StudentsPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        根据查询参数获取学生信息列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 学生信息列表信息对象
        """
        query = (
            select(Students)
            .where(
                Students.birth_date == query_object.birth_date if query_object.birth_date else True,
                Students.phone == query_object.phone if query_object.phone else True,
                Students.email == query_object.email if query_object.email else True,
                Students.address == query_object.address if query_object.address else True,
                Students.class_id == query_object.class_id if query_object.class_id else True,
            )
            .order_by(Students.id)
            .distinct()
        )
        students_list: PageModel | list[dict[str, Any]] = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )

        return students_list

    @classmethod
    async def add_students_dao(cls, db: AsyncSession, students: StudentsModel) -> Students:
        """
        新增学生信息数据库操作

        :param db: orm对象
        :param students: 学生信息对象
        :return:
        """
        db_students = Students(**students.model_dump(exclude={}))
        db.add(db_students)
        await db.flush()

        return db_students

    @classmethod
    async def edit_students_dao(cls, db: AsyncSession, students: dict) -> None:
        """
        编辑学生信息数据库操作

        :param db: orm对象
        :param students: 需要更新的学生信息字典
        :return:
        """
        await db.execute(update(Students), [students])

    @classmethod
    async def delete_students_dao(cls, db: AsyncSession, students: StudentsModel) -> None:
        """
        删除学生信息数据库操作

        :param db: orm对象
        :param students: 学生信息对象
        :return:
        """
        await db.execute(delete(Students).where(Students.id.in_([students.id])))

