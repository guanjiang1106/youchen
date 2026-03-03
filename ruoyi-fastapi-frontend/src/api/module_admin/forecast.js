import request from '@/utils/request'

// 查询销售预测，存储各产品在各区域的销售预测数据列表
export function listForecast(query) {
  return request({
    url: '/module_admin/forecast/list',
    method: 'get',
    params: query
  })
}

// 查询销售预测，存储各产品在各区域的销售预测数据详细
export function getForecast(id) {
  return request({
    url: '/module_admin/forecast/' + id,
    method: 'get'
  })
}

// 新增销售预测，存储各产品在各区域的销售预测数据
export function addForecast(data) {
  return request({
    url: '/module_admin/forecast',
    method: 'post',
    data: data
  })
}

// 修改销售预测，存储各产品在各区域的销售预测数据
export function updateForecast(data) {
  return request({
    url: '/module_admin/forecast',
    method: 'put',
    data: data
  })
}

// 删除销售预测，存储各产品在各区域的销售预测数据
export function delForecast(id) {
  return request({
    url: '/module_admin/forecast/' + id,
    method: 'delete'
  })
}
