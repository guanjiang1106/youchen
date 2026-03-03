from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_admin.entity.do.list_do import DeviceList
from module_admin.entity.vo.list_vo import ListModel, ListPageQueryModel
from utils.page_util import PageUtil


class ListDao:
    """
    设备清单模块数据库操作层
    """

    @classmethod
    async def get_list_detail_by_id(cls, db: AsyncSession, id: int) -> DeviceList | None:
        """
        根据主键 ID获取设备清单详细信息

        :param db: orm对象
        :param id: 主键 ID
        :return: 设备清单信息对象
        """
        list_info = (
            (
                await db.execute(
                    select(DeviceList)
                    .where(
                        DeviceList.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return list_info

    @classmethod
    async def get_list_detail_by_info(cls, db: AsyncSession, list: ListModel) -> DeviceList | None:
        """
        根据设备清单参数获取设备清单信息

        :param db: orm对象
        :param list: 设备清单参数对象
        :return: 设备清单信息对象
        """
        list_info = (
            (
                await db.execute(
                    select(DeviceList).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return list_info

    @classmethod
    async def get_list_list(
        cls, db: AsyncSession, query_object: ListPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        根据查询参数获取设备清单列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 设备清单列表信息对象
        """
        query = (
            select(DeviceList)
            .where(
                DeviceList.device_code == query_object.device_code if query_object.device_code else True,
                DeviceList.device_name.like(f'%{query_object.device_name}%') if query_object.device_name else True,
                DeviceList.device_type == query_object.device_type if query_object.device_type else True,
                DeviceList.brand == query_object.brand if query_object.brand else True,
                DeviceList.model == query_object.model if query_object.model else True,
                DeviceList.serial_number == query_object.serial_number if query_object.serial_number else True,
                DeviceList.purchase_date == query_object.purchase_date if query_object.purchase_date else True,
                DeviceList.warranty_period == query_object.warranty_period if query_object.warranty_period else True,
                DeviceList.status == query_object.status if query_object.status else True,
                DeviceList.location == query_object.location if query_object.location else True,
                DeviceList.department == query_object.department if query_object.department else True,
                DeviceList.responsible_person == query_object.responsible_person if query_object.responsible_person else True,
                DeviceList.remarks == query_object.remarks if query_object.remarks else True,
            )
            .order_by(DeviceList.id)
            .distinct()
        )
        list_list: PageModel | list[dict[str, Any]] = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )

        return list_list

    @classmethod
    async def add_list_dao(cls, db: AsyncSession, list: ListModel) -> DeviceList:
        """
        新增设备清单数据库操作

        :param db: orm对象
        :param list: 设备清单对象
        :return:
        """
        db_list = DeviceList(**list.model_dump(exclude={}))
        db.add(db_list)
        await db.flush()

        return db_list

    @classmethod
    async def edit_list_dao(cls, db: AsyncSession, list: dict) -> None:
        """
        编辑设备清单数据库操作

        :param db: orm对象
        :param list: 需要更新的设备清单字典
        :return:
        """
        await db.execute(update(DeviceList), [list])

    @classmethod
    async def delete_list_dao(cls, db: AsyncSession, list: ListModel) -> None:
        """
        删除设备清单数据库操作

        :param db: orm对象
        :param list: 设备清单对象
        :return:
        """
        await db.execute(delete(DeviceList).where(DeviceList.id.in_([list.id])))

