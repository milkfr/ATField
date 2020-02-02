import api from '@/api/index'
import { axios } from '@/utils/request'

export function getCGIList (parameter) {
  return axios({
    url: api.getCGIList,
    method: 'get',
    params: parameter
  })
}

export function updateCGIInfo (parameter) {
  return axios({
    url: api.updateCGIInfo,
    method: 'post',
    data: parameter
  })
}

export function saveCGIInfo (parameter) {
  return axios({
    url: api.saveCGIInfo,
    method: 'post',
    data: parameter
  })
}

export function activateCGI (parameter) {
  return axios({
    url: api.activateCGI,
    method: 'post',
    data: parameter
  })
}

export function removeCGI (parameter) {
  return axios({
    url: api.removeCGI,
    method: 'post',
    data: parameter
  })
}
