import request from '@/utils/request'

// 查询学生信息列表
export function listStudents(query) {
  return request({
    url: '/stu/students/list',
    method: 'get',
    params: query
  })
}

// 查询学生信息详细
export function getStudents(id) {
  return request({
    url: '/stu/students/' + id,
    method: 'get'
  })
}

// 新增学生信息
export function addStudents(data) {
  return request({
    url: '/stu/students',
    method: 'post',
    data: data
  })
}

// 修改学生信息
export function updateStudents(data) {
  return request({
    url: '/stu/students',
    method: 'put',
    data: data
  })
}

// 删除学生信息
export function delStudents(id) {
  return request({
    url: '/stu/students/' + id,
    method: 'delete'
  })
}
