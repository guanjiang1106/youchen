from datetime import datetime
from typing import Annotated
import random
import string

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
from module_admin.service.table_service import TableService
from module_admin.entity.vo.table_vo import DeleteTableModel, TableModel, TablePageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.response_util import ResponseUtil


table_controller = APIRouterPro(
    prefix='/module_admin/table', order_num=50, tags=['质量检验记录'], dependencies=[PreAuthDependency()]
)


@table_controller.get(
    '/list',
    summary='获取质量检验记录分页列表接口',
    description='用于获取质量检验记录分页列表',
    response_model=PageResponseModel[TableModel],
    dependencies=[UserInterfaceAuthDependency('module_admin:table:list')],
)
async def get_module_admin_table_list(
    request: Request,
    table_page_query: Annotated[TablePageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取分页数据
    table_page_query_result = await TableService.get_table_list_services(query_db, table_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=table_page_query_result)


@table_controller.post(
    '',
    summary='新增质量检验记录接口',
    description='用于新增质量检验记录',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:table:add')],
)
@ValidateFields(validate_model='add_table')
@Log(title='质量检验记录', business_type=BusinessType.INSERT)
async def add_module_admin_table(
    request: Request,
    add_table: TableModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_table.create_time = datetime.now()
    add_table.update_time = datetime.now()
    add_table_result = await TableService.add_table_services(query_db, add_table)
    logger.info(add_table_result.message)

    return ResponseUtil.success(msg=add_table_result.message)


@table_controller.put(
    '',
    summary='编辑质量检验记录接口',
    description='用于编辑质量检验记录',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:table:edit')],
)
@ValidateFields(validate_model='edit_table')
@Log(title='质量检验记录', business_type=BusinessType.UPDATE)
async def edit_module_admin_table(
    request: Request,
    edit_table: TableModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_table.update_time = datetime.now()
    edit_table_result = await TableService.edit_table_services(query_db, edit_table)
    logger.info(edit_table_result.message)

    return ResponseUtil.success(msg=edit_table_result.message)


@table_controller.delete(
    '/{ids}',
    summary='删除质量检验记录接口',
    description='用于删除质量检验记录',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:table:remove')],
)
@Log(title='质量检验记录', business_type=BusinessType.DELETE)
async def delete_module_admin_table(
    request: Request,
    ids: Annotated[str, Path(description='需要删除的主键 ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    delete_table = DeleteTableModel(ids=ids)
    delete_table_result = await TableService.delete_table_services(query_db, delete_table)
    logger.info(delete_table_result.message)

    return ResponseUtil.success(msg=delete_table_result.message)


@table_controller.get(
    '/{id}',
    summary='获取质量检验记录详情接口',
    description='用于获取指定质量检验记录的详细信息',
    response_model=DataResponseModel[TableModel],
    dependencies=[UserInterfaceAuthDependency('module_admin:table:query')]
)
async def query_detail_module_admin_table(
    request: Request,
    id: Annotated[int, Path(description='主键 ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    table_detail_result = await TableService.table_detail_services(query_db, id)
    logger.info(f'获取 id 为{id}的信息成功')

    return ResponseUtil.success(data=table_detail_result)


@table_controller.post(
    '/export',
    summary='导出质量检验记录列表接口',
    description='用于导出当前符合查询条件的质量检验记录列表数据',
    response_class=StreamingResponse,
    responses={
        200: {
            'description': '流式返回质量检验记录列表 excel 文件',
            'content': {
                'application/octet-stream': {},
            },
        }
    },
    dependencies=[UserInterfaceAuthDependency('module_admin:table:export')],
)
@Log(title='质量检验记录', business_type=BusinessType.EXPORT)
async def export_module_admin_table_list(
    request: Request,
    table_page_query: Annotated[TablePageQueryModel, Form()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取全量数据
    table_query_result = await TableService.get_table_list_services(query_db, table_page_query, is_page=False)
    table_export_result = await TableService.export_table_list_services(table_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(table_export_result))


@table_controller.post(
    '/random',
    summary='生成随机质量检验记录接口',
    description='用于生成随机的质量检验记录数据并插入系统',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:table:random')],
)
@Log(title='质量检验记录', business_type=BusinessType.INSERT)
async def generate_random_module_admin_table(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    generate_result = await TableService.generate_random_data_services(query_db)
    logger.info(generate_result.message)

    return ResponseUtil.success(msg=generate_result.message)