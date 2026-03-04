from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from module_admin.entity.do.log_do import SysLogininfor, SysOperLog
from module_admin.entity.do.user_do import SysUser
from utils.common_util import CamelCaseUtil


class DashboardService:
    """
    首页数据统计服务
    """

    @classmethod
    async def get_dashboard_stats(cls, db: AsyncSession) -> dict:
        """
        获取首页统计数据

        :param db: 数据库会话
        :return: 统计数据字典
        """
        # 获取总用户数
        total_users_result = await db.execute(select(func.count(SysUser.user_id)))
        total_users = total_users_result.scalar() or 0

        # 获取今日新增用户数
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_users_result = await db.execute(
            select(func.count(SysUser.user_id)).where(SysUser.create_time >= today_start)
        )
        today_users = today_users_result.scalar() or 0

        # 获取昨日新增用户数（用于计算增长率）
        yesterday_start = today_start - timedelta(days=1)
        yesterday_users_result = await db.execute(
            select(func.count(SysUser.user_id)).where(
                SysUser.create_time >= yesterday_start, SysUser.create_time < today_start
            )
        )
        yesterday_users = yesterday_users_result.scalar() or 0

        # 计算用户增长率
        user_growth = 0.0
        if yesterday_users > 0:
            user_growth = round(((today_users - yesterday_users) / yesterday_users) * 100, 1)
        elif today_users > 0:
            user_growth = 100.0

        # 获取总操作日志数
        total_logs_result = await db.execute(select(func.count(SysOperLog.oper_id)))
        total_logs = total_logs_result.scalar() or 0

        # 获取今日操作数
        today_logs_result = await db.execute(
            select(func.count(SysOperLog.oper_id)).where(SysOperLog.oper_time >= today_start)
        )
        today_logs = today_logs_result.scalar() or 0

        # 获取昨日操作数
        yesterday_logs_result = await db.execute(
            select(func.count(SysOperLog.oper_id)).where(
                SysOperLog.oper_time >= yesterday_start, SysOperLog.oper_time < today_start
            )
        )
        yesterday_logs = yesterday_logs_result.scalar() or 0

        # 计算操作增长率
        log_growth = 0.0
        if yesterday_logs > 0:
            log_growth = round(((today_logs - yesterday_logs) / yesterday_logs) * 100, 1)
        elif today_logs > 0:
            log_growth = 100.0

        # 获取今日登录次数
        today_logins_result = await db.execute(
            select(func.count(SysLogininfor.info_id)).where(SysLogininfor.login_time >= today_start)
        )
        today_logins = today_logins_result.scalar() or 0

        # 获取昨日登录次数
        yesterday_logins_result = await db.execute(
            select(func.count(SysLogininfor.info_id)).where(
                SysLogininfor.login_time >= yesterday_start, SysLogininfor.login_time < today_start
            )
        )
        yesterday_logins = yesterday_logins_result.scalar() or 0

        # 计算登录增长率
        login_growth = 0.0
        if yesterday_logins > 0:
            login_growth = round(((today_logins - yesterday_logins) / yesterday_logins) * 100, 1)
        elif today_logins > 0:
            login_growth = 100.0

        # 获取今日成功登录率
        today_success_logins_result = await db.execute(
            select(func.count(SysLogininfor.info_id)).where(
                SysLogininfor.login_time >= today_start, SysLogininfor.status == '0'
            )
        )
        today_success_logins = today_success_logins_result.scalar() or 0

        success_rate = 0.0
        if today_logins > 0:
            success_rate = round((today_success_logins / today_logins) * 100, 1)

        # 获取昨日成功登录率
        yesterday_success_logins_result = await db.execute(
            select(func.count(SysLogininfor.info_id)).where(
                SysLogininfor.login_time >= yesterday_start,
                SysLogininfor.login_time < today_start,
                SysLogininfor.status == '0',
            )
        )
        yesterday_success_logins = yesterday_success_logins_result.scalar() or 0

        yesterday_success_rate = 0.0
        if yesterday_logins > 0:
            yesterday_success_rate = round((yesterday_success_logins / yesterday_logins) * 100, 1)

        # 计算成功率变化
        success_rate_change = round(success_rate - yesterday_success_rate, 1)

        return {
            'totalUsers': total_users,
            'todayUsers': today_users,
            'userGrowth': user_growth,
            'totalLogs': total_logs,
            'todayLogs': today_logs,
            'logGrowth': log_growth,
            'todayLogins': today_logins,
            'loginGrowth': login_growth,
            'successRate': success_rate,
            'successRateChange': success_rate_change,
        }

    @classmethod
    async def get_recent_activities(cls, db: AsyncSession, limit: int = 10) -> list:
        """
        获取最近活动记录

        :param db: 数据库会话
        :param limit: 返回记录数
        :return: 活动记录列表
        """
        # 获取最近的操作日志
        query = (
            select(SysOperLog)
            .order_by(SysOperLog.oper_time.desc())
            .limit(limit)
        )

        result = await db.execute(query)
        logs = result.scalars().all()

        activities = []
        for log in logs:
            # 根据业务类型确定图标和颜色
            icon_map = {
                '0': {'icon': 'el-icon-info', 'color': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'},
                '1': {'icon': 'el-icon-plus', 'color': 'linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%)'},
                '2': {'icon': 'el-icon-edit', 'color': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'},
                '3': {'icon': 'el-icon-delete', 'color': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'},
            }

            business_type = str(log.business_type) if log.business_type is not None else '0'
            icon_info = icon_map.get(business_type, icon_map['0'])

            # 根据状态确定状态文本和样式
            status_map = {
                '0': {'status': 'success', 'statusText': '成功'},
                '1': {'status': 'error', 'statusText': '失败'},
            }

            status = str(log.status) if log.status else '0'
            status_info = status_map.get(status, status_map['0'])

            # 计算时间差
            time_diff = cls._format_time_diff(log.oper_time)

            activity = {
                'icon': icon_info['icon'],
                'color': icon_info['color'],
                'title': log.title or '系统操作',
                'operName': log.oper_name or '未知',
                'time': time_diff,
                'status': status_info['status'],
                'statusText': status_info['statusText'],
            }

            activities.append(activity)

        return activities

    @classmethod
    def _format_time_diff(cls, oper_time: datetime) -> str:
        """
        格式化时间差

        :param oper_time: 操作时间
        :return: 格式化的时间差字符串
        """
        if not oper_time:
            return '未知时间'

        now = datetime.now()
        diff = now - oper_time

        if diff.days > 0:
            if diff.days == 1:
                return '昨天'
            elif diff.days < 7:
                return f'{diff.days}天前'
            else:
                return oper_time.strftime('%Y-%m-%d')

        hours = diff.seconds // 3600
        if hours > 0:
            return f'{hours}小时前'

        minutes = diff.seconds // 60
        if minutes > 0:
            return f'{minutes}分钟前'

        return '刚刚'
