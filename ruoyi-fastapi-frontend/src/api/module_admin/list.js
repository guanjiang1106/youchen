import request from '@/utils/request'

// 查询设备清单列表
export function listList(query) {
  return request({
    url: '/module_admin/list/list',
    method: 'get',
    params: query
  })
}

// 查询设备清单详细
export function getList(id) {
  return request({
    url: '/module_admin/list/' + id,
    method: 'get'
  })
}

// 新增设备清单
export function addList(data) {
  return request({
    url: '/module_admin/list',
    method: 'post',
    data: data
  })
}

// 修改设备清单
export function updateList(data) {
  return request({
    url: '/module_admin/list',
    method: 'put',
    data: data
  })
}

// 删除设备清单
export function delList(id) {
  return request({
    url: '/module_admin/list/' + id,
    method: 'delete'
  })
}

// 导出设备清单
export function exportList(query) {
  return request({
    url: '/module_admin/list/export',
    method: 'post',
    params: query
  })
}

// 生成随机设备清单数据
export function generateRandom(count) {
  const data = new FormData()
  data.append('count', count)
  return request({
    url: '/module_admin/list/generate',
    method: 'post',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    data: data
  })
}