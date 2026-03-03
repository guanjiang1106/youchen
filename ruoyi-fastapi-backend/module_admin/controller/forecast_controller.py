from typing import Annotated

from fastapi import Form, Path, Query, Request, Response
from fastapi.responses import StreamingResponse
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession

from common.annotation.log_annotation import Log
from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.enums import BusinessType
from common.router import APIRouterPro
from common.vo import DataResponseModel, PageResponseModel, ResponseBaseModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.forecast_service import ForecastService
from module_admin.entity.vo.forecast_vo import DeleteForecastModel, ForecastModel, ForecastPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.response_util import ResponseUtil


forecast_controller = APIRouterPro(
    prefix='/module_admin/forecast', order_num=50, tags=['销售预测，存储各产品在各区域的销售预测数据'], dependencies=[PreAuthDependency()]
)


@forecast_controller.get(
    '/list',
    summary='获取销售预测，存储各产品在各区域的销售预测数据分页列表接口',
    description='用于获取销售预测，存储各产品在各区域的销售预测数据分页列表',
    response_model=PageResponseModel[ForecastModel],
    dependencies=[UserInterfaceAuthDependency('module_admin:forecast:list')],
)
async def get_module_admin_forecast_list(
    request: Request,
forecast_page_query: Annotated[ForecastPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取分页数据
    forecast_page_query_result = await ForecastService.get_forecast_list_services(query_db, forecast_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=forecast_page_query_result)


@forecast_controller.post(
    '',
    summary='新增销售预测，存储各产品在各区域的销售预测数据接口',
    description='用于新增销售预测，存储各产品在各区域的销售预测数据',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:forecast:add')],
)
@ValidateFields(validate_model='add_forecast')
@Log(title='销售预测，存储各产品在各区域的销售预测数据', business_type=BusinessType.INSERT)
async def add_module_admin_forecast(
    request: Request,
    add_forecast: ForecastModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_forecast_result = await ForecastService.add_forecast_services(query_db, add_forecast)
    logger.info(add_forecast_result.message)

    return ResponseUtil.success(msg=add_forecast_result.message)


@forecast_controller.put(
    '',
    summary='编辑销售预测，存储各产品在各区域的销售预测数据接口',
    description='用于编辑销售预测，存储各产品在各区域的销售预测数据',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:forecast:edit')],
)
@ValidateFields(validate_model='edit_forecast')
@Log(title='销售预测，存储各产品在各区域的销售预测数据', business_type=BusinessType.UPDATE)
async def edit_module_admin_forecast(
    request: Request,
    edit_forecast: ForecastModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_forecast_result = await ForecastService.edit_forecast_services(query_db, edit_forecast)
    logger.info(edit_forecast_result.message)

    return ResponseUtil.success(msg=edit_forecast_result.message)


@forecast_controller.delete(
    '/{ids}',
    summary='删除销售预测，存储各产品在各区域的销售预测数据接口',
    description='用于删除销售预测，存储各产品在各区域的销售预测数据',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:forecast:remove')],
)
@Log(title='销售预测，存储各产品在各区域的销售预测数据', business_type=BusinessType.DELETE)
async def delete_module_admin_forecast(
    request: Request,
    ids: Annotated[str, Path(description='需要删除的主键 ID，自增序列')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    delete_forecast = DeleteForecastModel(ids=ids)
    delete_forecast_result = await ForecastService.delete_forecast_services(query_db, delete_forecast)
    logger.info(delete_forecast_result.message)

    return ResponseUtil.success(msg=delete_forecast_result.message)


@forecast_controller.get(
    '/{id}',
    summary='获取销售预测，存储各产品在各区域的销售预测数据详情接口',
    description='用于获取指定销售预测，存储各产品在各区域的销售预测数据的详细信息',
    response_model=DataResponseModel[ForecastModel],
    dependencies=[UserInterfaceAuthDependency('module_admin:forecast:query')]
)
async def query_detail_module_admin_forecast(
    request: Request,
    id: Annotated[int, Path(description='主键 ID，自增序列')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    forecast_detail_result = await ForecastService.forecast_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=forecast_detail_result)


@forecast_controller.post(
    '/export',
    summary='导出销售预测，存储各产品在各区域的销售预测数据列表接口',
    description='用于导出当前符合查询条件的销售预测，存储各产品在各区域的销售预测数据列表数据',
    response_class=StreamingResponse,
    responses={
        200: {
            'description': '流式返回销售预测，存储各产品在各区域的销售预测数据列表excel文件',
            'content': {
                'application/octet-stream': {},
            },
        }
    },
    dependencies=[UserInterfaceAuthDependency('module_admin:forecast:export')],
)
@Log(title='销售预测，存储各产品在各区域的销售预测数据', business_type=BusinessType.EXPORT)
async def export_module_admin_forecast_list(
    request: Request,
    forecast_page_query: Annotated[ForecastPageQueryModel, Form()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取全量数据
    forecast_query_result = await ForecastService.get_forecast_list_services(query_db, forecast_page_query, is_page=False)
    forecast_export_result = await ForecastService.export_forecast_list_services(forecast_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(forecast_export_result))
