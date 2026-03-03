import request from '@/utils/request'

// 查询工艺信息列表
export function listInfo(query) {
  return request({
    url: '/module_admin/info/list',
    method: 'get',
    params: query
  })
}

// 查询工艺信息详细
export function getInfo(id) {
  return request({
    url: '/module_admin/info/' + id,
    method: 'get'
  })
}

// 新增工艺信息
export function addInfo(data) {
  return request({
    url: '/module_admin/info',
    method: 'post',
    data: data
  })
}

// 修改工艺信息
export function updateInfo(data) {
  return request({
    url: '/module_admin/info',
    method: 'put',
    data: data
  })
}

// 删除工艺信息
export function delInfo(id) {
  return request({
    url: '/module_admin/info/' + id,
    method: 'delete'
  })
}

// 导出工艺信息
export function exportInfo(query) {
  return request({
    url: '/module_admin/info/export',
    method: 'post',
    params: query
  })
}

// 生成随机工艺信息数据
export function generateRandomData(count) {
  return request({
    url: '/module_admin/info/generate_random_data',
    method: 'post',
    data: { count }
  })
}