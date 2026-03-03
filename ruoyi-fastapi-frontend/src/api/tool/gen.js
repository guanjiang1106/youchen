import request from '@/utils/request'

// 查询生成表数据
export function listTable(query) {
  return request({
    url: '/tool/gen/list',
    method: 'get',
    params: query
  })
}
// 查询db数据库列表
export function listDbTable(query) {
  return request({
    url: '/tool/gen/db/list',
    method: 'get',
    params: query
  })
}

// 查询表详细信息
export function getGenTable(tableId) {
  return request({
    url: '/tool/gen/' + tableId,
    method: 'get'
  })
}

// 修改代码生成信息
export function updateGenTable(data) {
  return request({
    url: '/tool/gen',
    method: 'put',
    data: data
  })
}

// 导入表
export function importTable(data) {
  return request({
    url: '/tool/gen/importTable',
    method: 'post',
    params: data
  })
}

// 创建表
export function createTable(data) {
  return request({
    url: '/tool/gen/createTable',
    method: 'post',
    params: data
  })
}

// AI生成建表SQL
export function generateTableSQL(data) {
  return request({
    url: '/tool/gen/generateTableSQL',
    method: 'post',
    params: data,
    timeout: 120000 // 设置2分钟超时，因为AI生成需要较长时间
  })
}

// 预览生成代码
export function previewTable(tableId) {
  return request({
    url: '/tool/gen/preview/' + tableId,
    method: 'get'
  })
}

// 删除表数据
export function delTable(tableId) {
  return request({
    url: '/tool/gen/' + tableId,
    method: 'delete'
  })
}

// 生成代码（自定义路径）
export function genCode(tableName) {
  return request({
    url: '/tool/gen/genCode/' + tableName,
    method: 'get'
  })
}

// 同步数据库
export function synchDb(tableName) {
  return request({
    url: '/tool/gen/synchDb/' + tableName,
    method: 'get'
  })
}

// 生成菜单
export function createMenu(tableId) {
  return request({
    url: '/tool/gen/createMenu/' + tableId,
    method: 'post',
    timeout: 30000 // 设置30秒超时
  })
}

// AI重构前端界面
export function refactorFrontend(data) {
  return request({
    url: '/tool/gen/refactorFrontend',
    method: 'post',
    data: data,
    timeout: 180000 // 设置3分钟超时，AI生成需要较长时间
  })
}

// 应用重构结果
export function applyRefactor(data) {
  return request({
    url: '/tool/gen/applyRefactor',
    method: 'post',
    data: data
  })
}
