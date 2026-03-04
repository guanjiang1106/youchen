from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_business.entity.do.process_do import Process
from module_business.entity.vo.process_vo import ProcessModel, ProcessPageQueryModel
from utils.page_util import PageUtil


class ProcessDao:
    """
    工艺模块数据库操作层
    """

    @classmethod
    async def get_process_detail_by_id(cls, db: AsyncSession, id: int) -> Process | None:
        """
        根据主键 ID获取工艺详细信息

        :param db: orm对象
        :param id: 主键 ID
        :return: 工艺信息对象
        """
        process_info = (
            (
                await db.execute(
                    select(Process)
                    .where(
                        Process.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return process_info

    @classmethod
    async def get_process_detail_by_info(cls, db: AsyncSession, process: ProcessModel) -> Process | None:
        """
        根据工艺参数获取工艺信息

        :param db: orm对象
        :param process: 工艺参数对象
        :return: 工艺信息对象
        """
        process_info = (
            (
                await db.execute(
                    select(Process).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return process_info

    @classmethod
    async def get_process_list(
        cls, db: AsyncSession, query_object: ProcessPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        根据查询参数获取工艺列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 工艺列表信息对象
        """
        query = (
            select(Process)
            .where(
                Process.process_code == query_object.process_code if query_object.process_code else True,
                Process.process_name.like(f'%{query_object.process_name}%') if query_object.process_name else True,
                Process.description == query_object.description if query_object.description else True,
                Process.category == query_object.category if query_object.category else True,
                Process.version == query_object.version if query_object.version else True,
                Process.status == query_object.status if query_object.status else True,
                Process.sort_order == query_object.sort_order if query_object.sort_order else True,
            )
            .order_by(Process.id)
            .distinct()
        )
        process_list: PageModel | list[dict[str, Any]] = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )

        return process_list

    @classmethod
    async def add_process_dao(cls, db: AsyncSession, process: ProcessModel) -> Process:
        """
        新增工艺数据库操作

        :param db: orm对象
        :param process: 工艺对象
        :return:
        """
        db_process = Process(**process.model_dump(exclude={}))
        db.add(db_process)
        await db.flush()

        return db_process

    @classmethod
    async def edit_process_dao(cls, db: AsyncSession, process: dict) -> None:
        """
        编辑工艺数据库操作

        :param db: orm对象
        :param process: 需要更新的工艺字典
        :return:
        """
        await db.execute(update(Process), [process])

    @classmethod
    async def delete_process_dao(cls, db: AsyncSession, process: ProcessModel) -> None:
        """
        删除工艺数据库操作

        :param db: orm对象
        :param process: 工艺对象
        :return:
        """
        await db.execute(delete(Process).where(Process.id.in_([process.id])))

