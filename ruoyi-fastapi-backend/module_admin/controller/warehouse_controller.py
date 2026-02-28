from datetime import datetime
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
from module_admin.service.warehouse_service import WarehouseService
from module_admin.entity.vo.warehouse_vo import DeleteWarehouseModel, WarehouseModel, WarehousePageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.response_util import ResponseUtil


warehouse_controller = APIRouterPro(
    prefix='/system/warehouse', order_num=50, tags=['仓库'], dependencies=[PreAuthDependency()]
)


@warehouse_controller.get(
    '/list',
    summary='获取仓库分页列表接口',
    description='用于获取仓库分页列表',
    response_model=PageResponseModel[WarehouseModel],
    dependencies=[UserInterfaceAuthDependency('system:warehouse:list')],
)
async def get_system_warehouse_list(
    request: Request,
    warehouse_page_query: Annotated[WarehousePageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取分页数据
    warehouse_page_query_result = await WarehouseService.get_warehouse_list_services(query_db, warehouse_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=warehouse_page_query_result)


@warehouse_controller.post(
    '',
    summary='新增仓库接口',
    description='用于新增仓库',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('system:warehouse:add')],
)
@ValidateFields(validate_model='add_warehouse')
@Log(title='仓库', business_type=BusinessType.INSERT)
async def add_system_warehouse(
    request: Request,
    add_warehouse: WarehouseModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_warehouse.create_time = datetime.now()
    add_warehouse.update_time = datetime.now()
    add_warehouse_result = await WarehouseService.add_warehouse_services(query_db, add_warehouse)
    logger.info(add_warehouse_result.message)

    return ResponseUtil.success(msg=add_warehouse_result.message)


@warehouse_controller.put(
    '',
    summary='编辑仓库接口',
    description='用于编辑仓库',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('system:warehouse:edit')],
)
@ValidateFields(validate_model='edit_warehouse')
@Log(title='仓库', business_type=BusinessType.UPDATE)
async def edit_system_warehouse(
    request: Request,
    edit_warehouse: WarehouseModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_warehouse.update_time = datetime.now()
    edit_warehouse_result = await WarehouseService.edit_warehouse_services(query_db, edit_warehouse)
    logger.info(edit_warehouse_result.message)

    return ResponseUtil.success(msg=edit_warehouse_result.message)


@warehouse_controller.delete(
    '/{ids}',
    summary='删除仓库接口',
    description='用于删除仓库',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('system:warehouse:remove')],
)
@Log(title='仓库', business_type=BusinessType.DELETE)
async def delete_system_warehouse(
    request: Request,
    ids: Annotated[str, Path(description='需要删除的主键 ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    delete_warehouse = DeleteWarehouseModel(ids=ids)
    delete_warehouse_result = await WarehouseService.delete_warehouse_services(query_db, delete_warehouse)
    logger.info(delete_warehouse_result.message)

    return ResponseUtil.success(msg=delete_warehouse_result.message)


@warehouse_controller.get(
    '/{id}',
    summary='获取仓库详情接口',
    description='用于获取指定仓库的详细信息',
    response_model=DataResponseModel[WarehouseModel],
    dependencies=[UserInterfaceAuthDependency('system:warehouse:query')]
)
async def query_detail_system_warehouse(
    request: Request,
    id: Annotated[int, Path(description='主键 ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    warehouse_detail_result = await WarehouseService.warehouse_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=warehouse_detail_result)


@warehouse_controller.post(
    '/export',
    summary='导出仓库列表接口',
    description='用于导出当前符合查询条件的仓库列表数据',
    response_class=StreamingResponse,
    responses={
        200: {
            'description': '流式返回仓库列表excel文件',
            'content': {
                'application/octet-stream': {},
            },
        }
    },
    dependencies=[UserInterfaceAuthDependency('system:warehouse:export')],
)
@Log(title='仓库', business_type=BusinessType.EXPORT)
async def export_system_warehouse_list(
    request: Request,
    warehouse_page_query: Annotated[WarehousePageQueryModel, Form()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取全量数据
    warehouse_query_result = await WarehouseService.get_warehouse_list_services(query_db, warehouse_page_query, is_page=False)
    warehouse_export_result = await WarehouseService.export_warehouse_list_services(warehouse_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(warehouse_export_result))
