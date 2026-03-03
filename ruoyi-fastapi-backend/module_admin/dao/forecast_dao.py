from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_admin.entity.do.forecast_do import SalesForecast
from module_admin.entity.vo.forecast_vo import ForecastModel, ForecastPageQueryModel
from utils.page_util import PageUtil


class ForecastDao:
    """
    销售预测，存储各产品在各区域的销售预测数据模块数据库操作层
    """

    @classmethod
    async def get_forecast_detail_by_id(cls, db: AsyncSession, id: int) -> SalesForecast | None:
        """
        根据主键 ID，自增序列获取销售预测，存储各产品在各区域的销售预测数据详细信息

        :param db: orm对象
        :param id: 主键 ID，自增序列
        :return: 销售预测，存储各产品在各区域的销售预测数据信息对象
        """
        forecast_info = (
            (
                await db.execute(
                    select(SalesForecast)
                    .where(
                        SalesForecast.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return forecast_info

    @classmethod
    async def get_forecast_detail_by_info(cls, db: AsyncSession, forecast: ForecastModel) -> SalesForecast | None:
        """
        根据销售预测，存储各产品在各区域的销售预测数据参数获取销售预测，存储各产品在各区域的销售预测数据信息

        :param db: orm对象
        :param forecast: 销售预测，存储各产品在各区域的销售预测数据参数对象
        :return: 销售预测，存储各产品在各区域的销售预测数据信息对象
        """
        forecast_info = (
            (
                await db.execute(
                    select(SalesForecast).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return forecast_info

    @classmethod
    async def get_forecast_list(
        cls, db: AsyncSession, query_object: ForecastPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        根据查询参数获取销售预测，存储各产品在各区域的销售预测数据列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 销售预测，存储各产品在各区域的销售预测数据列表信息对象
        """
        query = (
            select(SalesForecast)
            .where(
                SalesForecast.product_id == query_object.product_id if query_object.product_id else True,
                SalesForecast.region_code == query_object.region_code if query_object.region_code else True,
                SalesForecast.forecast_date == query_object.forecast_date if query_object.forecast_date else True,
                SalesForecast.predicted_amount == query_object.predicted_amount if query_object.predicted_amount else True,
                SalesForecast.confidence_level == query_object.confidence_level if query_object.confidence_level else True,
                SalesForecast.model_version == query_object.model_version if query_object.model_version else True,
                SalesForecast.created_at == query_object.created_at if query_object.created_at else True,
                SalesForecast.updated_at == query_object.updated_at if query_object.updated_at else True,
            )
            .order_by(SalesForecast.id)
            .distinct()
        )
        forecast_list: PageModel | list[dict[str, Any]] = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )

        return forecast_list

    @classmethod
    async def add_forecast_dao(cls, db: AsyncSession, forecast: ForecastModel) -> SalesForecast:
        """
        新增销售预测，存储各产品在各区域的销售预测数据数据库操作

        :param db: orm对象
        :param forecast: 销售预测，存储各产品在各区域的销售预测数据对象
        :return:
        """
        db_forecast = SalesForecast(**forecast.model_dump(exclude={}))
        db.add(db_forecast)
        await db.flush()

        return db_forecast

    @classmethod
    async def edit_forecast_dao(cls, db: AsyncSession, forecast: dict) -> None:
        """
        编辑销售预测，存储各产品在各区域的销售预测数据数据库操作

        :param db: orm对象
        :param forecast: 需要更新的销售预测，存储各产品在各区域的销售预测数据字典
        :return:
        """
        await db.execute(update(SalesForecast), [forecast])

    @classmethod
    async def delete_forecast_dao(cls, db: AsyncSession, forecast: ForecastModel) -> None:
        """
        删除销售预测，存储各产品在各区域的销售预测数据数据库操作

        :param db: orm对象
        :param forecast: 销售预测，存储各产品在各区域的销售预测数据对象
        :return:
        """
        await db.execute(delete(SalesForecast).where(SalesForecast.id.in_([forecast.id])))

