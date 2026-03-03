import request from '@/utils/request'

// 查询老师维护列表
export function listTeacher(query) {
  return request({
    url: '/module_admin/teacher/list',
    method: 'get',
    params: query
  })
}

// 查询老师维护详细
export function getTeacher(id) {
  return request({
    url: '/module_admin/teacher/' + id,
    method: 'get'
  })
}

// 新增老师维护
export function addTeacher(data) {
  return request({
    url: '/module_admin/teacher',
    method: 'post',
    data: data
  })
}

// 修改老师维护
export function updateTeacher(data) {
  return request({
    url: '/module_admin/teacher',
    method: 'put',
    data: data
  })
}

// 删除老师维护
export function delTeacher(id) {
  return request({
    url: '/module_admin/teacher/' + id,
    method: 'delete'
  })
}

// 导出老师维护
export function exportTeacher(query) {
  return request({
    url: '/module_admin/teacher/export',
    method: 'post',
    params: query
  })
}

// 随机生成老师维护数据
export function generateRandomTeacher(count) {
  const data = new FormData()
  data.append('count', count)
  return request({
    url: '/module_admin/teacher/generate',
    method: 'post',
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    data: data
  })
}