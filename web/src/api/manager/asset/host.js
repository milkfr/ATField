import api from '@/api/index'
import { axios } from '@/utils/request'

export function getHostList (parameter) {
  return axios({
    url: api.getHostList,
    method: 'get',
    params: parameter
  })
}

export function getHostService (parameter) {
  return axios({
    url: api.getHostService,
    method: 'get',
    params: parameter
  })
}

export function updateHostInfo (parameter) {
  return axios({
    url: api.updateHostInfo,
    method: 'post',
    data: parameter
  })
}

export function saveHostInfo (parameter) {
  return axios({
    url: api.saveHostInfo,
    method: 'post',
    data: parameter
  })
}

export function activateHost (parameter) {
  return axios({
    url: api.activateHost,
    method: 'post',
    data: parameter
  })
}

export function removeHost (parameter) {
  return axios({
    url: api.removeHost,
    method: 'post',
    data: parameter
  })
}
