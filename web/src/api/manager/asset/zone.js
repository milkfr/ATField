import api from '@/api/index'
import { axios } from '@/utils/request'

export function getZoneList (parameter) {
  return axios({
    url: api.getZoneList,
    method: 'get',
    params: parameter
  })
}

export function updateZoneInfo (parameter) {
  return axios({
    url: api.updateZoneInfo,
    method: 'post',
    data: parameter
  })
}

export function saveZoneInfo (parameter) {
  return axios({
    url: api.saveZoneInfo,
    method: 'post',
    data: parameter
  })
}

export function removeZone (parameter) {
  return axios({
    url: api.removeZone,
    method: 'post',
    data: parameter
  })
}
