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
from module_admin.service.process_service import ProcessService
from module_admin.entity.vo.process_vo import DeleteProcessModel, ProcessModel, ProcessPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.response_util import ResponseUtil


process_controller = APIRouterPro(
    prefix='/module_admin/process', order_num=50, tags=['工艺'], dependencies=[PreAuthDependency()]
)


@process_controller.get(
    '/list',
    summary='获取工艺分页列表接口',
    description='用于获取工艺分页列表',
    response_model=PageResponseModel[ProcessModel],
    dependencies=[UserInterfaceAuthDependency('module_admin:process:list')],
)
async def get_module_admin_process_list(
    request: Request,
process_page_query: Annotated[ProcessPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取分页数据
    process_page_query_result = await ProcessService.get_process_list_services(query_db, process_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=process_page_query_result)


@process_controller.post(
    '',
    summary='新增工艺接口',
    description='用于新增工艺',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:process:add')],
)
@ValidateFields(validate_model='add_process')
@Log(title='工艺', business_type=BusinessType.INSERT)
async def add_module_admin_process(
    request: Request,
    add_process: ProcessModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_process.create_time = datetime.now()
    add_process.update_time = datetime.now()
    add_process_result = await ProcessService.add_process_services(query_db, add_process)
    logger.info(add_process_result.message)

    return ResponseUtil.success(msg=add_process_result.message)


@process_controller.put(
    '',
    summary='编辑工艺接口',
    description='用于编辑工艺',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:process:edit')],
)
@ValidateFields(validate_model='edit_process')
@Log(title='工艺', business_type=BusinessType.UPDATE)
async def edit_module_admin_process(
    request: Request,
    edit_process: ProcessModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_process.update_time = datetime.now()
    edit_process_result = await ProcessService.edit_process_services(query_db, edit_process)
    logger.info(edit_process_result.message)

    return ResponseUtil.success(msg=edit_process_result.message)


@process_controller.delete(
    '/{ids}',
    summary='删除工艺接口',
    description='用于删除工艺',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:process:remove')],
)
@Log(title='工艺', business_type=BusinessType.DELETE)
async def delete_module_admin_process(
    request: Request,
    ids: Annotated[str, Path(description='需要删除的主键 ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    delete_process = DeleteProcessModel(ids=ids)
    delete_process_result = await ProcessService.delete_process_services(query_db, delete_process)
    logger.info(delete_process_result.message)

    return ResponseUtil.success(msg=delete_process_result.message)


@process_controller.get(
    '/{id}',
    summary='获取工艺详情接口',
    description='用于获取指定工艺的详细信息',
    response_model=DataResponseModel[ProcessModel],
    dependencies=[UserInterfaceAuthDependency('module_admin:process:query')]
)
async def query_detail_module_admin_process(
    request: Request,
    id: Annotated[int, Path(description='主键 ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    process_detail_result = await ProcessService.process_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=process_detail_result)


@process_controller.post(
    '/export',
    summary='导出工艺列表接口',
    description='用于导出当前符合查询条件的工艺列表数据',
    response_class=StreamingResponse,
    responses={
        200: {
            'description': '流式返回工艺列表excel文件',
            'content': {
                'application/octet-stream': {},
            },
        }
    },
    dependencies=[UserInterfaceAuthDependency('module_admin:process:export')],
)
@Log(title='工艺', business_type=BusinessType.EXPORT)
async def export_module_admin_process_list(
    request: Request,
    process_page_query: Annotated[ProcessPageQueryModel, Form()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取全量数据
    process_query_result = await ProcessService.get_process_list_services(query_db, process_page_query, is_page=False)
    process_export_result = await ProcessService.export_process_list_services(process_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(process_export_result))
