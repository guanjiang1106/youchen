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
from module_admin.service.teacher_service import TeacherService
from module_admin.entity.vo.teacher_vo import DeleteTeacherModel, TeacherModel, TeacherPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.response_util import ResponseUtil


teacher_controller = APIRouterPro(
    prefix='/module_admin/teacher', order_num=50, tags=['老师维护'], dependencies=[PreAuthDependency()]
)


@teacher_controller.get(
    '/list',
    summary='获取老师维护分页列表接口',
    description='用于获取老师维护分页列表',
    response_model=PageResponseModel[TeacherModel],
    dependencies=[UserInterfaceAuthDependency('module_admin:teacher:list')],
)
async def get_module_admin_teacher_list(
    request: Request,
teacher_page_query: Annotated[TeacherPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取分页数据
    teacher_page_query_result = await TeacherService.get_teacher_list_services(query_db, teacher_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=teacher_page_query_result)


@teacher_controller.post(
    '',
    summary='新增老师维护接口',
    description='用于新增老师维护',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:teacher:add')],
)
@ValidateFields(validate_model='add_teacher')
@Log(title='老师维护', business_type=BusinessType.INSERT)
async def add_module_admin_teacher(
    request: Request,
    add_teacher: TeacherModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_teacher.create_time = datetime.now()
    add_teacher.update_time = datetime.now()
    add_teacher_result = await TeacherService.add_teacher_services(query_db, add_teacher)
    logger.info(add_teacher_result.message)

    return ResponseUtil.success(msg=add_teacher_result.message)


@teacher_controller.put(
    '',
    summary='编辑老师维护接口',
    description='用于编辑老师维护',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:teacher:edit')],
)
@ValidateFields(validate_model='edit_teacher')
@Log(title='老师维护', business_type=BusinessType.UPDATE)
async def edit_module_admin_teacher(
    request: Request,
    edit_teacher: TeacherModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_teacher.update_time = datetime.now()
    edit_teacher_result = await TeacherService.edit_teacher_services(query_db, edit_teacher)
    logger.info(edit_teacher_result.message)

    return ResponseUtil.success(msg=edit_teacher_result.message)


@teacher_controller.delete(
    '/{ids}',
    summary='删除老师维护接口',
    description='用于删除老师维护',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:teacher:remove')],
)
@Log(title='老师维护', business_type=BusinessType.DELETE)
async def delete_module_admin_teacher(
    request: Request,
    ids: Annotated[str, Path(description='需要删除的主键 ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    delete_teacher = DeleteTeacherModel(ids=ids)
    delete_teacher_result = await TeacherService.delete_teacher_services(query_db, delete_teacher)
    logger.info(delete_teacher_result.message)

    return ResponseUtil.success(msg=delete_teacher_result.message)


@teacher_controller.get(
    '/{id}',
    summary='获取老师维护详情接口',
    description='用于获取指定老师维护的详细信息',
    response_model=DataResponseModel[TeacherModel],
    dependencies=[UserInterfaceAuthDependency('module_admin:teacher:query')]
)
async def query_detail_module_admin_teacher(
    request: Request,
    id: Annotated[int, Path(description='主键 ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    teacher_detail_result = await TeacherService.teacher_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=teacher_detail_result)


@teacher_controller.post(
    '/export',
    summary='导出老师维护列表接口',
    description='用于导出当前符合查询条件的老师维护列表数据',
    response_class=StreamingResponse,
    responses={
        200: {
            'description': '流式返回老师维护列表excel文件',
            'content': {
                'application/octet-stream': {},
            },
        }
    },
    dependencies=[UserInterfaceAuthDependency('module_admin:teacher:export')],
)
@Log(title='老师维护', business_type=BusinessType.EXPORT)
async def export_module_admin_teacher_list(
    request: Request,
    teacher_page_query: Annotated[TeacherPageQueryModel, Form()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取全量数据
    teacher_query_result = await TeacherService.get_teacher_list_services(query_db, teacher_page_query, is_page=False)
    teacher_export_result = await TeacherService.export_teacher_list_services(teacher_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(teacher_export_result))
