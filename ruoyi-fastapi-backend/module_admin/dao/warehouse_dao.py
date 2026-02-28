from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_admin.entity.do.warehouse_do import Warehouse
from module_admin.entity.vo.warehouse_vo import WarehouseModel, WarehousePageQueryModel
from utils.page_util import PageUtil


class WarehouseDao:
    """
    仓库模块数据库操作层
    """

    @classmethod
    async def get_warehouse_detail_by_id(cls, db: AsyncSession, id: int) -> Warehouse | None:
        """
        根据主键 ID获取仓库详细信息

        :param db: orm对象
        :param id: 主键 ID
        :return: 仓库信息对象
        """
        warehouse_info = (
            (
                await db.execute(
                    select(Warehouse)
                    .where(
                        Warehouse.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return warehouse_info

    @classmethod
    async def get_warehouse_detail_by_info(cls, db: AsyncSession, warehouse: WarehouseModel) -> Warehouse | None:
        """
        根据仓库参数获取仓库信息

        :param db: orm对象
        :param warehouse: 仓库参数对象
        :return: 仓库信息对象
        """
        warehouse_info = (
            (
                await db.execute(
                    select(Warehouse).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return warehouse_info

    @classmethod
    async def get_warehouse_list(
        cls, db: AsyncSession, query_object: WarehousePageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        根据查询参数获取仓库列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 仓库列表信息对象
        """
        query = (
            select(Warehouse)
            .where(
                Warehouse.address == query_object.address if query_object.address else True,
                Warehouse.contact_person == query_object.contact_person if query_object.contact_person else True,
                Warehouse.contact_phone == query_object.contact_phone if query_object.contact_phone else True,
                Warehouse.capacity == query_object.capacity if query_object.capacity else True,
            )
            .order_by(Warehouse.id)
            .distinct()
        )
        warehouse_list: PageModel | list[dict[str, Any]] = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )

        return warehouse_list

    @classmethod
    async def add_warehouse_dao(cls, db: AsyncSession, warehouse: WarehouseModel) -> Warehouse:
        """
        新增仓库数据库操作

        :param db: orm对象
        :param warehouse: 仓库对象
        :return:
        """
        db_warehouse = Warehouse(**warehouse.model_dump(exclude={}))
        db.add(db_warehouse)
        await db.flush()

        return db_warehouse

    @classmethod
    async def edit_warehouse_dao(cls, db: AsyncSession, warehouse: dict) -> None:
        """
        编辑仓库数据库操作

        :param db: orm对象
        :param warehouse: 需要更新的仓库字典
        :return:
        """
        await db.execute(update(Warehouse), [warehouse])

    @classmethod
    async def delete_warehouse_dao(cls, db: AsyncSession, warehouse: WarehouseModel) -> None:
        """
        删除仓库数据库操作

        :param db: orm对象
        :param warehouse: 仓库对象
        :return:
        """
        await db.execute(delete(Warehouse).where(Warehouse.id.in_([warehouse.id])))

