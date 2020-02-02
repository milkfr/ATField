import api from '@/api/index'
import { axios } from '@/utils/request'

export function getHTTPList (parameter) {
  return axios({
    url: api.getHTTPList,
    method: 'get',
    params: parameter
  })
}

export function updateHTTPInfo (parameter) {
  return axios({
    url: api.updateHTTPInfo,
    method: 'post',
    data: parameter
  })
}

export function saveHTTPInfo (parameter) {
  return axios({
    url: api.saveHTTPInfo,
    method: 'post',
    data: parameter
  })
}

export function activateHTTP (parameter) {
  return axios({
    url: api.activateHTTP,
    method: 'post',
    data: parameter
  })
}

export function removeHTTP (parameter) {
  return axios({
    url: api.removeHTTP,
    method: 'post',
    data: parameter
  })
}
