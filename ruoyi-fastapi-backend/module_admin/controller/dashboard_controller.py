from datetime import datetime
from typing import Annotated

from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.router import APIRouterPro
from common.vo import DataResponseModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.dashboard_service import DashboardService
from utils.log_util import logger
from utils.response_util import ResponseUtil

dashboard_controller = APIRouterPro(
    prefix='/dashboard',
    order_num=1,
    tags=['首页-数据统计'],
    dependencies=[PreAuthDependency()],
)


@dashboard_controller.get(
    '/stats',
    summary='获取首页统计数据',
    response_model=DataResponseModel[dict],
)
async def get_dashboard_stats(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    """
    获取首页统计数据
    """
    stats = await DashboardService.get_dashboard_stats(query_db)
    logger.info('获取首页统计数据成功')
    return ResponseUtil.success(data=stats)


@dashboard_controller.get(
    '/activities',
    summary='获取最近活动',
    response_model=DataResponseModel[list],
)
async def get_recent_activities(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    """
    获取最近活动记录
    """
    activities = await DashboardService.get_recent_activities(query_db, limit=10)
    logger.info('获取最近活动成功')
    return ResponseUtil.success(data=activities)
