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
from module_admin.service.list_service import ListService
from module_admin.entity.vo.list_vo import DeleteListModel, ListModel, ListPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.response_util import ResponseUtil


list_controller = APIRouterPro(
    prefix='/module_admin/list', order_num=50, tags=['设备清单'], dependencies=[PreAuthDependency()]
)


@list_controller.get(
    '/list',
    summary='获取设备清单分页列表接口',
    description='用于获取设备清单分页列表',
    response_model=PageResponseModel[ListModel],
    dependencies=[UserInterfaceAuthDependency('module_admin:list:list')],
)
async def get_module_admin_list_list(
    request: Request,
    list_page_query: Annotated[ListPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取分页数据
    list_page_query_result = await ListService.get_list_list_services(query_db, list_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=list_page_query_result)


@list_controller.post(
    '',
    summary='新增设备清单接口',
    description='用于新增设备清单',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:list:add')],
)
@ValidateFields(validate_model='add_list')
@Log(title='设备清单', business_type=BusinessType.INSERT)
async def add_module_admin_list(
    request: Request,
    add_list: ListModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_list.create_time = datetime.now()
    add_list.update_time = datetime.now()
    add_list_result = await ListService.add_list_services(query_db, add_list)
    logger.info(add_list_result.message)

    return ResponseUtil.success(msg=add_list_result.message)


@list_controller.put(
    '',
    summary='编辑设备清单接口',
    description='用于编辑设备清单',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:list:edit')],
)
@ValidateFields(validate_model='edit_list')
@Log(title='设备清单', business_type=BusinessType.UPDATE)
async def edit_module_admin_list(
    request: Request,
    edit_list: ListModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_list.update_time = datetime.now()
    edit_list_result = await ListService.edit_list_services(query_db, edit_list)
    logger.info(edit_list_result.message)

    return ResponseUtil.success(msg=edit_list_result.message)


@list_controller.delete(
    '/{ids}',
    summary='删除设备清单接口',
    description='用于删除设备清单',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:list:remove')],
)
@Log(title='设备清单', business_type=BusinessType.DELETE)
async def delete_module_admin_list(
    request: Request,
    ids: Annotated[str, Path(description='需要删除的主键 ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    delete_list = DeleteListModel(ids=ids)
    delete_list_result = await ListService.delete_list_services(query_db, delete_list)
    logger.info(delete_list_result.message)

    return ResponseUtil.success(msg=delete_list_result.message)


@list_controller.get(
    '/{id}',
    summary='获取设备清单详情接口',
    description='用于获取指定设备清单的详细信息',
    response_model=DataResponseModel[ListModel],
    dependencies=[UserInterfaceAuthDependency('module_admin:list:query')]
)
async def query_detail_module_admin_list(
    request: Request,
    id: Annotated[int, Path(description='主键 ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    list_detail_result = await ListService.list_detail_services(query_db, id)
    logger.info(f'获取 id 为{id}的信息成功')

    return ResponseUtil.success(data=list_detail_result)


@list_controller.post(
    '/export',
    summary='导出设备清单列表接口',
    description='用于导出当前符合查询条件的设备清单列表数据',
    response_class=StreamingResponse,
    responses={
        200: {
            'description': '流式返回设备清单列表 excel 文件',
            'content': {
                'application/octet-stream': {},
            },
        }
    },
    dependencies=[UserInterfaceAuthDependency('module_admin:list:export')],
)
@Log(title='设备清单', business_type=BusinessType.EXPORT)
async def export_module_admin_list_list(
    request: Request,
    list_page_query: Annotated[ListPageQueryModel, Form()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取全量数据
    list_query_result = await ListService.get_list_list_services(query_db, list_page_query, is_page=False)
    list_export_result = await ListService.export_list_list_services(list_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(list_export_result))


@list_controller.post(
    '/generate',
    summary='生成随机设备清单数据接口',
    description='用于生成指定数量的随机设备清单数据',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:list:random')],
)
@Log(title='设备清单', business_type=BusinessType.INSERT)
async def generate_random_module_admin_list(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    count: Annotated[int, Form(ge=1, le=100, description='生成数据数量')] = 10,
) -> Response:
    result = await ListService.generate_random_list_services(query_db, count)
    logger.info(result.message)

    return ResponseUtil.success(msg=result.message)