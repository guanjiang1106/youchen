from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_admin.entity.do.info_do import ProcessInfo
from module_admin.entity.vo.info_vo import InfoModel, InfoPageQueryModel
from utils.page_util import PageUtil


class InfoDao:
    """
    工艺信息模块数据库操作层
    """

    @classmethod
    async def get_info_detail_by_id(cls, db: AsyncSession, id: int) -> ProcessInfo | None:
        """
        根据主键 ID获取工艺信息详细信息

        :param db: orm对象
        :param id: 主键 ID
        :return: 工艺信息信息对象
        """
        info_info = (
            (
                await db.execute(
                    select(ProcessInfo)
                    .where(
                        ProcessInfo.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return info_info

    @classmethod
    async def get_info_detail_by_info(cls, db: AsyncSession, info: InfoModel) -> ProcessInfo | None:
        """
        根据工艺信息参数获取工艺信息信息

        :param db: orm对象
        :param info: 工艺信息参数对象
        :return: 工艺信息信息对象
        """
        info_info = (
            (
                await db.execute(
                    select(ProcessInfo).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return info_info

    @classmethod
    async def get_info_list(
        cls, db: AsyncSession, query_object: InfoPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        根据查询参数获取工艺信息列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 工艺信息列表信息对象
        """
        query = (
            select(ProcessInfo)
            .where(
                ProcessInfo.process_code == query_object.process_code if query_object.process_code else True,
                ProcessInfo.process_name.like(f'%{query_object.process_name}%') if query_object.process_name else True,
                ProcessInfo.process_type == query_object.process_type if query_object.process_type else True,
                ProcessInfo.description == query_object.description if query_object.description else True,
                ProcessInfo.standard_hours == query_object.standard_hours if query_object.standard_hours else True,
                ProcessInfo.required_equipment == query_object.required_equipment if query_object.required_equipment else True,
                ProcessInfo.operator_level == query_object.operator_level if query_object.operator_level else True,
                ProcessInfo.status == query_object.status if query_object.status else True,
                ProcessInfo.version == query_object.version if query_object.version else True,
            )
            .order_by(ProcessInfo.id)
            .distinct()
        )
        info_list: PageModel | list[dict[str, Any]] = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )

        return info_list

    @classmethod
    async def add_info_dao(cls, db: AsyncSession, info: InfoModel) -> ProcessInfo:
        """
        新增工艺信息数据库操作

        :param db: orm对象
        :param info: 工艺信息对象
        :return:
        """
        db_info = ProcessInfo(**info.model_dump(exclude={}))
        db.add(db_info)
        await db.flush()

        return db_info

    @classmethod
    async def edit_info_dao(cls, db: AsyncSession, info: dict) -> None:
        """
        编辑工艺信息数据库操作

        :param db: orm对象
        :param info: 需要更新的工艺信息字典
        :return:
        """
        await db.execute(update(ProcessInfo), [info])

    @classmethod
    async def delete_info_dao(cls, db: AsyncSession, info: InfoModel) -> None:
        """
        删除工艺信息数据库操作

        :param db: orm对象
        :param info: 工艺信息对象
        :return:
        """
        await db.execute(delete(ProcessInfo).where(ProcessInfo.id.in_([info.id])))

