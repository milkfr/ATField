import api from '@/api/index'
import { axios } from '@/utils/request'

export function getToken (parameter) {
  return axios({
    url: api.getToken,
    method: 'post',
    data: parameter
  })
}

export function getUserInfo (parameter) {
  return axios({
    url: api.getUserInfo,
    method: 'get',
    params: parameter
  })
}
