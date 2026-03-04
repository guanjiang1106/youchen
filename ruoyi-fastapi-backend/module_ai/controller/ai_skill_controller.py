"""
AI 技能管理控制器
"""
from datetime import datetime
from typing import Annotated

from fastapi import Query, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.annotation.log_annotation import Log
from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.enums import BusinessType
from common.router import APIRouterPro
from common.vo import DataResponseModel, ResponseBaseModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_ai.service.ai_skill_service import AiSkillService
from utils.log_util import logger
from utils.response_util import ResponseUtil

ai_skill_controller = APIRouterPro(
    prefix='/ai/skill',
    order_num=103,
    tags=['AI管理-技能管理'],
    dependencies=[PreAuthDependency()],
)


@ai_skill_controller.get(
    '/list',
    summary='获取可用技能列表',
    response_model=DataResponseModel,
    dependencies=[UserInterfaceAuthDependency('ai:skill:list')],
)
async def get_skill_list(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    """
    获取当前用户可用的技能列表
    """
    try:
        # 加载用户可用的技能
        skills = await AiSkillService.load_available_skills(
            user_id=current_user.user.user_id,
            query_db=query_db
        )
        
        # 转换为前端需要的格式
        skill_list = []
        for skill in skills:
            skill_info = {
                'name': skill.name,
                'description': skill.description,
                'emoji': skill.metadata.emoji if skill.metadata else None,
                'file_path': skill.file_path,
                'use_count': skill.use_count,
                'last_used': skill.last_used.isoformat() if skill.last_used else None,
                'requires': {
                    'bins': skill.metadata.requires.bins if skill.metadata and skill.metadata.requires else [],
                    'env': skill.metadata.requires.env if skill.metadata and skill.metadata.requires else [],
                    'os': skill.metadata.requires.os if skill.metadata and skill.metadata.requires else [],
                } if skill.metadata and skill.metadata.requires else None,
                'primary_env': skill.metadata.primary_env if skill.metadata else None,
            }
            skill_list.append(skill_info)
        
        logger.info(f'获取技能列表成功，共 {len(skill_list)} 个技能')
        return ResponseUtil.success(data={'skills': skill_list, 'total': len(skill_list)})
    except Exception as e:
        logger.error(f'获取技能列表失败: {e}', exc_info=True)
        return ResponseUtil.error(msg=f'获取技能列表失败: {str(e)}')


@ai_skill_controller.get(
    '/detail/{skill_name}',
    summary='获取技能详情',
    response_model=DataResponseModel,
    dependencies=[UserInterfaceAuthDependency('ai:skill:query')],
)
async def get_skill_detail(
    request: Request,
    skill_name: str,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    """
    获取指定技能的详细信息
    """
    try:
        # 加载所有技能
        skills = await AiSkillService.load_available_skills(
            user_id=current_user.user.user_id,
            query_db=query_db
        )
        
        # 查找指定技能
        target_skill = None
        for skill in skills:
            if skill.name == skill_name:
                target_skill = skill
                break
        
        if not target_skill:
            return ResponseUtil.error(msg=f'技能 {skill_name} 不存在')
        
        # 返回详细信息
        skill_detail = {
            'name': target_skill.name,
            'description': target_skill.description,
            'content': target_skill.content,
            'emoji': target_skill.metadata.emoji if target_skill.metadata else None,
            'file_path': target_skill.file_path,
            'use_count': target_skill.use_count,
            'last_used': target_skill.last_used.isoformat() if target_skill.last_used else None,
            'metadata': {
                'requires': {
                    'bins': target_skill.metadata.requires.bins if target_skill.metadata.requires else [],
                    'any_bins': target_skill.metadata.requires.any_bins if target_skill.metadata.requires else [],
                    'env': target_skill.metadata.requires.env if target_skill.metadata.requires else [],
                    'os': target_skill.metadata.requires.os if target_skill.metadata.requires else [],
                } if target_skill.metadata and target_skill.metadata.requires else None,
                'primary_env': target_skill.metadata.primary_env if target_skill.metadata else None,
            } if target_skill.metadata else None,
        }
        
        logger.info(f'获取技能详情成功: {skill_name}')
        return ResponseUtil.success(data=skill_detail)
    except Exception as e:
        logger.error(f'获取技能详情失败: {e}', exc_info=True)
        return ResponseUtil.error(msg=f'获取技能详情失败: {str(e)}')


@ai_skill_controller.get(
    '/stats',
    summary='获取技能统计信息',
    response_model=DataResponseModel,
    dependencies=[UserInterfaceAuthDependency('ai:skill:list')],
)
async def get_skill_stats(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    """
    获取技能使用统计信息
    """
    try:
        # 加载所有技能
        skills = await AiSkillService.load_available_skills(
            user_id=current_user.user.user_id,
            query_db=query_db
        )
        
        # 统计信息
        total_skills = len(skills)
        used_skills = sum(1 for s in skills if s.use_count > 0)
        total_uses = sum(s.use_count for s in skills)
        
        # 最常用的技能（前5个）
        top_skills = sorted(skills, key=lambda s: s.use_count, reverse=True)[:5]
        top_skills_data = [
            {
                'name': s.name,
                'description': s.description,
                'use_count': s.use_count,
                'emoji': s.metadata.emoji if s.metadata else None,
            }
            for s in top_skills
        ]
        
        # 最近使用的技能（前5个）
        recent_skills = sorted(
            [s for s in skills if s.last_used],
            key=lambda s: s.last_used,
            reverse=True
        )[:5]
        recent_skills_data = [
            {
                'name': s.name,
                'description': s.description,
                'last_used': s.last_used.isoformat() if s.last_used else None,
                'emoji': s.metadata.emoji if s.metadata else None,
            }
            for s in recent_skills
        ]
        
        stats = {
            'total_skills': total_skills,
            'used_skills': used_skills,
            'unused_skills': total_skills - used_skills,
            'total_uses': total_uses,
            'top_skills': top_skills_data,
            'recent_skills': recent_skills_data,
        }
        
        logger.info(f'获取技能统计成功')
        return ResponseUtil.success(data=stats)
    except Exception as e:
        logger.error(f'获取技能统计失败: {e}', exc_info=True)
        return ResponseUtil.error(msg=f'获取技能统计失败: {str(e)}')


@ai_skill_controller.get(
    '/prompt',
    summary='获取技能提示词',
    response_model=DataResponseModel,
    dependencies=[UserInterfaceAuthDependency('ai:skill:query')],
)
async def get_skills_prompt(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    """
    获取格式化后的技能提示词（用于调试）
    """
    try:
        # 加载所有技能
        skills = await AiSkillService.load_available_skills(
            user_id=current_user.user.user_id,
            query_db=query_db
        )
        
        # 格式化为提示词
        prompt = AiSkillService.format_skills_for_prompt(skills)
        
        logger.info(f'获取技能提示词成功，长度: {len(prompt)} 字符')
        return ResponseUtil.success(data={
            'prompt': prompt,
            'length': len(prompt),
            'skill_count': len(skills),
        })
    except Exception as e:
        logger.error(f'获取技能提示词失败: {e}', exc_info=True)
        return ResponseUtil.error(msg=f'获取技能提示词失败: {str(e)}')
