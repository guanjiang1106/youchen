from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_admin.entity.do.material_do import Material
from module_admin.entity.vo.material_vo import MaterialModel, MaterialPageQueryModel
from utils.page_util import PageUtil


class MaterialDao:
    """
    物料模块数据库操作层
    """

    @classmethod
    async def get_material_detail_by_id(cls, db: AsyncSession, id: int) -> Material | None:
        """
        根据主键 ID获取物料详细信息

        :param db: orm对象
        :param id: 主键 ID
        :return: 物料信息对象
        """
        material_info = (
            (
                await db.execute(
                    select(Material)
                    .where(
                        Material.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return material_info

    @classmethod
    async def get_material_detail_by_info(cls, db: AsyncSession, material: MaterialModel) -> Material | None:
        """
        根据物料参数获取物料信息

        :param db: orm对象
        :param material: 物料参数对象
        :return: 物料信息对象
        """
        material_info = (
            (
                await db.execute(
                    select(Material).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return material_info

    @classmethod
    async def get_material_list(
        cls, db: AsyncSession, query_object: MaterialPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        根据查询参数获取物料列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 物料列表信息对象
        """
        query = (
            select(Material)
            .where(
                Material.material_code == query_object.material_code if query_object.material_code else True,
                Material.material_name.like(f'%{query_object.material_name}%') if query_object.material_name else True,
                Material.specification == query_object.specification if query_object.specification else True,
                Material.unit == query_object.unit if query_object.unit else True,
                Material.category_id == query_object.category_id if query_object.category_id else True,
                Material.stock_quantity == query_object.stock_quantity if query_object.stock_quantity else True,
                Material.safety_stock == query_object.safety_stock if query_object.safety_stock else True,
                Material.price == query_object.price if query_object.price else True,
                Material.status == query_object.status if query_object.status else True,
            )
            .order_by(Material.id)
            .distinct()
        )
        material_list: PageModel | list[dict[str, Any]] = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )

        return material_list

    @classmethod
    async def add_material_dao(cls, db: AsyncSession, material: MaterialModel) -> Material:
        """
        新增物料数据库操作

        :param db: orm对象
        :param material: 物料对象
        :return:
        """
        db_material = Material(**material.model_dump(exclude={'unit', 'category_id', 'safety_stock', }))
        db.add(db_material)
        await db.flush()

        return db_material

    @classmethod
    async def edit_material_dao(cls, db: AsyncSession, material: dict) -> None:
        """
        编辑物料数据库操作

        :param db: orm对象
        :param material: 需要更新的物料字典
        :return:
        """
        await db.execute(update(Material), [material])

    @classmethod
    async def delete_material_dao(cls, db: AsyncSession, material: MaterialModel) -> None:
        """
        删除物料数据库操作

        :param db: orm对象
        :param material: 物料对象
        :return:
        """
        await db.execute(delete(Material).where(Material.id.in_([material.id])))

