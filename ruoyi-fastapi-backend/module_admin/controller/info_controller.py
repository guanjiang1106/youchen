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
from module_admin.service.info_service import InfoService
from module_admin.entity.vo.info_vo import DeleteInfoModel, InfoModel, InfoPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.response_util import ResponseUtil


info_controller = APIRouterPro(
    prefix='/module_admin/info', order_num=50, tags=['工艺信息'], dependencies=[PreAuthDependency()]
)


@info_controller.get(
    '/list',
    summary='获取工艺信息分页列表接口',
    description='用于获取工艺信息分页列表',
    response_model=PageResponseModel[InfoModel],
    dependencies=[UserInterfaceAuthDependency('module_admin:info:list')],
)
async def get_module_admin_info_list(
    request: Request,
    info_page_query: Annotated[InfoPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取分页数据
    info_page_query_result = await InfoService.get_info_list_services(query_db, info_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=info_page_query_result)


@info_controller.post(
    '',
    summary='新增工艺信息接口',
    description='用于新增工艺信息',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:info:add')],
)
@ValidateFields(validate_model='add_info')
@Log(title='工艺信息', business_type=BusinessType.INSERT)
async def add_module_admin_info(
    request: Request,
    add_info: InfoModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_info.create_time = datetime.now()
    add_info.update_time = datetime.now()
    add_info_result = await InfoService.add_info_services(query_db, add_info)
    logger.info(add_info_result.message)

    return ResponseUtil.success(msg=add_info_result.message)


@info_controller.put(
    '',
    summary='编辑工艺信息接口',
    description='用于编辑工艺信息',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:info:edit')],
)
@ValidateFields(validate_model='edit_info')
@Log(title='工艺信息', business_type=BusinessType.UPDATE)
async def edit_module_admin_info(
    request: Request,
    edit_info: InfoModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_info.update_time = datetime.now()
    edit_info_result = await InfoService.edit_info_services(query_db, edit_info)
    logger.info(edit_info_result.message)

    return ResponseUtil.success(msg=edit_info_result.message)


@info_controller.delete(
    '/{ids}',
    summary='删除工艺信息接口',
    description='用于删除工艺信息',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:info:remove')],
)
@Log(title='工艺信息', business_type=BusinessType.DELETE)
async def delete_module_admin_info(
    request: Request,
    ids: Annotated[str, Path(description='需要删除的主键 ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    delete_info = DeleteInfoModel(ids=ids)
    delete_info_result = await InfoService.delete_info_services(query_db, delete_info)
    logger.info(delete_info_result.message)

    return ResponseUtil.success(msg=delete_info_result.message)


@info_controller.get(
    '/{id}',
    summary='获取工艺信息详情接口',
    description='用于获取指定工艺信息的详细信息',
    response_model=DataResponseModel[InfoModel],
    dependencies=[UserInterfaceAuthDependency('module_admin:info:query')]
)
async def query_detail_module_admin_info(
    request: Request,
    id: Annotated[int, Path(description='主键 ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    info_detail_result = await InfoService.info_detail_services(query_db, id)
    logger.info(f'获取 id 为{id}的信息成功')

    return ResponseUtil.success(data=info_detail_result)


@info_controller.post(
    '/export',
    summary='导出工艺信息列表接口',
    description='用于导出当前符合查询条件的工艺信息列表数据',
    response_class=StreamingResponse,
    responses={
        200: {
            'description': '流式返回工艺信息列表 excel 文件',
            'content': {
                'application/octet-stream': {},
            },
        }
    },
    dependencies=[UserInterfaceAuthDependency('module_admin:info:export')],
)
@Log(title='工艺信息', business_type=BusinessType.EXPORT)
async def export_module_admin_info_list(
    request: Request,
    info_page_query: Annotated[InfoPageQueryModel, Form()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取全量数据
    info_query_result = await InfoService.get_info_list_services(query_db, info_page_query, is_page=False)
    info_export_result = await InfoService.export_info_list_services(info_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(info_export_result))


@info_controller.post(
    '/generate_random_data',
    summary='生成随机工艺信息接口',
    description='用于根据指定数量生成随机的工艺信息数据',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:info:generate_random_data')],
)
@Log(title='工艺信息', business_type=BusinessType.INSERT)
async def generate_random_module_admin_info(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    count: Annotated[int, Form(ge=1, le=100, description='生成数据数量')] = 10,
) -> Response:
    result = await InfoService.generate_random_data_services(query_db, count)
    logger.info(result.message)

    return ResponseUtil.success(msg=result.message)