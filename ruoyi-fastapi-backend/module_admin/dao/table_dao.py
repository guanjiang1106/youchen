from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_admin.entity.do.table_do import QualityTable
from module_admin.entity.vo.table_vo import TableModel, TablePageQueryModel
from utils.page_util import PageUtil


class TableDao:
    """
    质量检验记录模块数据库操作层
    """

    @classmethod
    async def get_table_detail_by_id(cls, db: AsyncSession, id: int) -> QualityTable | None:
        """
        根据主键 ID获取质量检验记录详细信息

        :param db: orm对象
        :param id: 主键 ID
        :return: 质量检验记录信息对象
        """
        table_info = (
            (
                await db.execute(
                    select(QualityTable)
                    .where(
                        QualityTable.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return table_info

    @classmethod
    async def get_table_detail_by_info(cls, db: AsyncSession, table: TableModel) -> QualityTable | None:
        """
        根据质量检验记录参数获取质量检验记录信息

        :param db: orm对象
        :param table: 质量检验记录参数对象
        :return: 质量检验记录信息对象
        """
        table_info = (
            (
                await db.execute(
                    select(QualityTable).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return table_info

    @classmethod
    async def get_table_list(
        cls, db: AsyncSession, query_object: TablePageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        根据查询参数获取质量检验记录列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 质量检验记录列表信息对象
        """
        query = (
            select(QualityTable)
            .where(
                QualityTable.product_code == query_object.product_code if query_object.product_code else True,
                QualityTable.batch_number == query_object.batch_number if query_object.batch_number else True,
                QualityTable.inspection_result == query_object.inspection_result if query_object.inspection_result else True,
                QualityTable.defect_count == query_object.defect_count if query_object.defect_count else True,
                QualityTable.inspector_name.like(f'%{query_object.inspector_name}%') if query_object.inspector_name else True,
                QualityTable.remarks == query_object.remarks if query_object.remarks else True,
            )
            .order_by(QualityTable.id)
            .distinct()
        )
        table_list: PageModel | list[dict[str, Any]] = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )

        return table_list

    @classmethod
    async def add_table_dao(cls, db: AsyncSession, table: TableModel) -> QualityTable:
        """
        新增质量检验记录数据库操作

        :param db: orm对象
        :param table: 质量检验记录对象
        :return:
        """
        db_table = QualityTable(**table.model_dump(exclude={}))
        db.add(db_table)
        await db.flush()

        return db_table

    @classmethod
    async def edit_table_dao(cls, db: AsyncSession, table: dict) -> None:
        """
        编辑质量检验记录数据库操作

        :param db: orm对象
        :param table: 需要更新的质量检验记录字典
        :return:
        """
        await db.execute(update(QualityTable), [table])

    @classmethod
    async def delete_table_dao(cls, db: AsyncSession, table: TableModel) -> None:
        """
        删除质量检验记录数据库操作

        :param db: orm对象
        :param table: 质量检验记录对象
        :return:
        """
        await db.execute(delete(QualityTable).where(QualityTable.id.in_([table.id])))

