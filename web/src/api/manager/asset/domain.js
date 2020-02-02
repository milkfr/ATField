import api from '@/api/index'
import { axios } from '@/utils/request'

export function getDomainList (parameter) {
  return axios({
    url: api.getDomainList,
    method: 'get',
    params: parameter
  })
}

export function updateDomainInfo (parameter) {
  return axios({
    url: api.updateDomainInfo,
    method: 'post',
    data: parameter
  })
}

export function saveDomainInfo (parameter) {
  return axios({
    url: api.saveDomainInfo,
    method: 'post',
    data: parameter
  })
}

export function activateDomain (parameter) {
  return axios({
    url: api.activateDomain,
    method: 'post',
    data: parameter
  })
}

export function removeDomain (parameter) {
  return axios({
    url: api.removeDomain,
    method: 'post',
    data: parameter
  })
}
