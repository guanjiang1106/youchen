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
from module_admin.service.material_service import MaterialService
from module_admin.entity.vo.material_vo import DeleteMaterialModel, MaterialModel, MaterialPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.response_util import ResponseUtil


material_controller = APIRouterPro(
    prefix='/module_admin/material', order_num=50, tags=['物料'], dependencies=[PreAuthDependency()]
)


@material_controller.get(
    '/list',
    summary='获取物料分页列表接口',
    description='用于获取物料分页列表',
    response_model=PageResponseModel[MaterialModel],
    dependencies=[UserInterfaceAuthDependency('module_admin:material:list')],
)
async def get_module_admin_material_list(
    request: Request,
material_page_query: Annotated[MaterialPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取分页数据
    material_page_query_result = await MaterialService.get_material_list_services(query_db, material_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=material_page_query_result)


@material_controller.post(
    '',
    summary='新增物料接口',
    description='用于新增物料',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:material:add')],
)
@ValidateFields(validate_model='add_material')
@Log(title='物料', business_type=BusinessType.INSERT)
async def add_module_admin_material(
    request: Request,
    add_material: MaterialModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_material.create_time = datetime.now()
    add_material.update_time = datetime.now()
    add_material_result = await MaterialService.add_material_services(query_db, add_material)
    logger.info(add_material_result.message)

    return ResponseUtil.success(msg=add_material_result.message)


@material_controller.put(
    '',
    summary='编辑物料接口',
    description='用于编辑物料',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:material:edit')],
)
@ValidateFields(validate_model='edit_material')
@Log(title='物料', business_type=BusinessType.UPDATE)
async def edit_module_admin_material(
    request: Request,
    edit_material: MaterialModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_material.update_time = datetime.now()
    edit_material_result = await MaterialService.edit_material_services(query_db, edit_material)
    logger.info(edit_material_result.message)

    return ResponseUtil.success(msg=edit_material_result.message)


@material_controller.delete(
    '/{ids}',
    summary='删除物料接口',
    description='用于删除物料',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('module_admin:material:remove')],
)
@Log(title='物料', business_type=BusinessType.DELETE)
async def delete_module_admin_material(
    request: Request,
    ids: Annotated[str, Path(description='需要删除的主键 ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    delete_material = DeleteMaterialModel(ids=ids)
    delete_material_result = await MaterialService.delete_material_services(query_db, delete_material)
    logger.info(delete_material_result.message)

    return ResponseUtil.success(msg=delete_material_result.message)


@material_controller.get(
    '/{id}',
    summary='获取物料详情接口',
    description='用于获取指定物料的详细信息',
    response_model=DataResponseModel[MaterialModel],
    dependencies=[UserInterfaceAuthDependency('module_admin:material:query')]
)
async def query_detail_module_admin_material(
    request: Request,
    id: Annotated[int, Path(description='主键 ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    material_detail_result = await MaterialService.material_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=material_detail_result)


@material_controller.post(
    '/export',
    summary='导出物料列表接口',
    description='用于导出当前符合查询条件的物料列表数据',
    response_class=StreamingResponse,
    responses={
        200: {
            'description': '流式返回物料列表excel文件',
            'content': {
                'application/octet-stream': {},
            },
        }
    },
    dependencies=[UserInterfaceAuthDependency('module_admin:material:export')],
)
@Log(title='物料', business_type=BusinessType.EXPORT)
async def export_module_admin_material_list(
    request: Request,
    material_page_query: Annotated[MaterialPageQueryModel, Form()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取全量数据
    material_query_result = await MaterialService.get_material_list_services(query_db, material_page_query, is_page=False)
    material_export_result = await MaterialService.export_material_list_services(material_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(material_export_result))
