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
from module_admin.system.service.students_service import StudentsService
from module_admin.system.entity.vo.students_vo import DeleteStudentsModel, StudentsModel, StudentsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.response_util import ResponseUtil


students_controller = APIRouterPro(
    prefix='/stu/students', order_num=50, tags=['学生信息'], dependencies=[PreAuthDependency()]
)


@students_controller.get(
    '/list',
    summary='获取学生信息分页列表接口',
    description='用于获取学生信息分页列表',
    response_model=PageResponseModel[StudentsModel],
    dependencies=[UserInterfaceAuthDependency('stu:students:list')],
)
async def get_stu_students_list(
    request: Request,
students_page_query: Annotated[StudentsPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取分页数据
    students_page_query_result = await StudentsService.get_students_list_services(query_db, students_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=students_page_query_result)


@students_controller.post(
    '',
    summary='新增学生信息接口',
    description='用于新增学生信息',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('stu:students:add')],
)
@ValidateFields(validate_model='add_students')
@Log(title='学生信息', business_type=BusinessType.INSERT)
async def add_stu_students(
    request: Request,
    add_students: StudentsModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_students.create_time = datetime.now()
    add_students.update_time = datetime.now()
    add_students_result = await StudentsService.add_students_services(query_db, add_students)
    logger.info(add_students_result.message)

    return ResponseUtil.success(msg=add_students_result.message)


@students_controller.put(
    '',
    summary='编辑学生信息接口',
    description='用于编辑学生信息',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('stu:students:edit')],
)
@ValidateFields(validate_model='edit_students')
@Log(title='学生信息', business_type=BusinessType.UPDATE)
async def edit_stu_students(
    request: Request,
    edit_students: StudentsModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_students.update_time = datetime.now()
    edit_students_result = await StudentsService.edit_students_services(query_db, edit_students)
    logger.info(edit_students_result.message)

    return ResponseUtil.success(msg=edit_students_result.message)


@students_controller.delete(
    '/{ids}',
    summary='删除学生信息接口',
    description='用于删除学生信息',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('stu:students:remove')],
)
@Log(title='学生信息', business_type=BusinessType.DELETE)
async def delete_stu_students(
    request: Request,
    ids: Annotated[str, Path(description='需要删除的主键 ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    delete_students = DeleteStudentsModel(ids=ids)
    delete_students_result = await StudentsService.delete_students_services(query_db, delete_students)
    logger.info(delete_students_result.message)

    return ResponseUtil.success(msg=delete_students_result.message)


@students_controller.get(
    '/{id}',
    summary='获取学生信息详情接口',
    description='用于获取指定学生信息的详细信息',
    response_model=DataResponseModel[StudentsModel],
    dependencies=[UserInterfaceAuthDependency('stu:students:query')]
)
async def query_detail_stu_students(
    request: Request,
    id: Annotated[int, Path(description='主键 ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    students_detail_result = await StudentsService.students_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=students_detail_result)


@students_controller.post(
    '/export',
    summary='导出学生信息列表接口',
    description='用于导出当前符合查询条件的学生信息列表数据',
    response_class=StreamingResponse,
    responses={
        200: {
            'description': '流式返回学生信息列表excel文件',
            'content': {
                'application/octet-stream': {},
            },
        }
    },
    dependencies=[UserInterfaceAuthDependency('stu:students:export')],
)
@Log(title='学生信息', business_type=BusinessType.EXPORT)
async def export_stu_students_list(
    request: Request,
    students_page_query: Annotated[StudentsPageQueryModel, Form()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取全量数据
    students_query_result = await StudentsService.get_students_list_services(query_db, students_page_query, is_page=False)
    students_export_result = await StudentsService.export_students_list_services(students_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(students_export_result))
