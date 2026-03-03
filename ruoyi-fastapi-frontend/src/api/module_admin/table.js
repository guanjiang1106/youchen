import request from '@/utils/request'

// 查询质量检验记录列表
export function listTable(query) {
  return request({
    url: '/module_admin/table/list',
    method: 'get',
    params: query
  })
}

// 查询质量检验记录详细
export function getTable(id) {
  return request({
    url: '/module_admin/table/' + id,
    method: 'get'
  })
}

// 新增质量检验记录
export function addTable(data) {
  return request({
    url: '/module_admin/table',
    method: 'post',
    data: data
  })
}

// 修改质量检验记录
export function updateTable(data) {
  return request({
    url: '/module_admin/table',
    method: 'put',
    data: data
  })
}

// 删除质量检验记录
export function delTable(id) {
  return request({
    url: '/module_admin/table/' + id,
    method: 'delete'
  })
}

// 导出质量检验记录列表
export function exportTable(query) {
  return request({
    url: '/module_admin/table/export',
    method: 'post',
    data: query
  })
}

// 生成随机质量检验记录数据
export function generateRandomData() {
  return request({
    url: '/module_admin/table/random',
    method: 'post'
  })
}
