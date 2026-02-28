import request from '@/utils/request'

// 查询工艺列表
export function listProcess(query) {
  return request({
    url: '/module_admin/process/list',
    method: 'get',
    params: query
  })
}

// 查询工艺详细
export function getProcess(id) {
  return request({
    url: '/module_admin/process/' + id,
    method: 'get'
  })
}

// 新增工艺
export function addProcess(data) {
  return request({
    url: '/module_admin/process',
    method: 'post',
    data: data
  })
}

// 修改工艺
export function updateProcess(data) {
  return request({
    url: '/module_admin/process',
    method: 'put',
    data: data
  })
}

// 删除工艺
export function delProcess(id) {
  return request({
    url: '/module_admin/process/' + id,
    method: 'delete'
  })
}
