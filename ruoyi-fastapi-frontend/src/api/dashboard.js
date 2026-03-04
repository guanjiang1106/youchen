import request from '@/utils/request'

// 获取首页统计数据
export function getDashboardStats() {
  return request({
    url: '/dashboard/stats',
    method: 'get'
  })
}

// 获取最近活动
export function getRecentActivities() {
  return request({
    url: '/dashboard/activities',
    method: 'get'
  })
}
