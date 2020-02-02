import api from '@/api/index'
import { axios } from '@/utils/request'

export function getPermissionList (parameter) {
  return axios({
    url: api.getPermissionList,
    method: 'get',
    params: parameter
  })
}

export function activatePermission (parameter) {
  return axios({
    url: api.activatePermission,
    method: 'post',
    data: parameter
  })
}

export function removePermission (parameter) {
  return axios({
    url: api.removePermission,
    method: 'post',
    data: parameter
  })
}
