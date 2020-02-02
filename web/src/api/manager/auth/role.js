import api from '@/api/index'
import { axios } from '@/utils/request'

export function getRoleList (parameter) {
  return axios({
    url: api.getRoleList,
    method: 'get',
    params: parameter
  })
}

export function updateRoleInfo (parameter) {
  return axios({
    url: api.updateRoleInfo,
    method: 'post',
    data: parameter
  })
}

export function saveRoleInfo (parameter) {
  return axios({
    url: api.saveRoleInfo,
    method: 'post',
    data: parameter
  })
}

export function activateRole (parameter) {
  return axios({
    url: api.activateRole,
    method: 'post',
    data: parameter
  })
}

export function removeRole (parameter) {
  return axios({
    url: api.removeRole,
    method: 'post',
    data: parameter
  })
}
