from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from common.constant import CommonConstant
from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_admin.dao.forecast_dao import ForecastDao
from module_admin.entity.vo.forecast_vo import DeleteForecastModel, ForecastModel, ForecastPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class ForecastService:
    """
    销售预测，存储各产品在各区域的销售预测数据模块服务层
    """

    @classmethod
    async def get_forecast_list_services(
        cls, query_db: AsyncSession, query_object: ForecastPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        获取销售预测，存储各产品在各区域的销售预测数据列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 销售预测，存储各产品在各区域的销售预测数据列表信息对象
        """
        forecast_list_result = await ForecastDao.get_forecast_list(query_db, query_object, is_page)

        return forecast_list_result


    @classmethod
    async def add_forecast_services(cls, query_db: AsyncSession, page_object: ForecastModel) -> CrudResponseModel:
        """
        新增销售预测，存储各产品在各区域的销售预测数据信息service

        :param query_db: orm对象
        :param page_object: 新增销售预测，存储各产品在各区域的销售预测数据对象
        :return: 新增销售预测，存储各产品在各区域的销售预测数据校验结果
        """
        try:
            await ForecastDao.add_forecast_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_forecast_services(cls, query_db: AsyncSession, page_object: ForecastModel) -> CrudResponseModel:
        """
        编辑销售预测，存储各产品在各区域的销售预测数据信息service

        :param query_db: orm对象
        :param page_object: 编辑销售预测，存储各产品在各区域的销售预测数据对象
        :return: 编辑销售预测，存储各产品在各区域的销售预测数据校验结果
        """
        edit_forecast = page_object.model_dump(exclude_unset=True, exclude={})
        forecast_info = await cls.forecast_detail_services(query_db, page_object.id)
        if forecast_info.id:
            try:
                await ForecastDao.edit_forecast_dao(query_db, edit_forecast)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='销售预测，存储各产品在各区域的销售预测数据不存在')

    @classmethod
    async def delete_forecast_services(cls, query_db: AsyncSession, page_object: DeleteForecastModel) -> CrudResponseModel:
        """
        删除销售预测，存储各产品在各区域的销售预测数据信息service

        :param query_db: orm对象
        :param page_object: 删除销售预测，存储各产品在各区域的销售预测数据对象
        :return: 删除销售预测，存储各产品在各区域的销售预测数据校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await ForecastDao.delete_forecast_dao(query_db, ForecastModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键 ID，自增序列为空')

    @classmethod
    async def forecast_detail_services(cls, query_db: AsyncSession, id: int) -> ForecastModel:
        """
        获取销售预测，存储各产品在各区域的销售预测数据详细信息service

        :param query_db: orm对象
        :param id: 主键 ID，自增序列
        :return: 主键 ID，自增序列对应的信息
        """
        forecast = await ForecastDao.get_forecast_detail_by_id(query_db, id=id)
        result = ForecastModel(**CamelCaseUtil.transform_result(forecast)) if forecast else ForecastModel()

        return result

    @staticmethod
    async def export_forecast_list_services(forecast_list: list) -> bytes:
        """
        导出销售预测，存储各产品在各区域的销售预测数据信息service

        :param forecast_list: 销售预测，存储各产品在各区域的销售预测数据信息列表
        :return: 销售预测，存储各产品在各区域的销售预测数据信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键 ID，自增序列',
            'productId': '关联的产品 ID',
            'regionCode': '区域代码，标识销售区域',
            'forecastDate': '预测日期，指预测对应的业务日期',
            'predictedAmount': '预测销售额，单位为元',
            'confidenceLevel': '置信度等级，0-100 表示预测的可信程度',
            'modelVersion': '生成该预测的算法模型版本',
            'createdAt': '记录创建时间',
            'updatedAt': '记录最后更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(forecast_list, mapping_dict)

        return binary_data
