import api from '@/api/index'
import { axios } from '@/utils/request'

export function getPluginList (parameter) {
  return axios({
    url: api.getPluginList,
    method: 'get',
    params: parameter
  })
}

export function updatePluginInfo (parameter) {
  return axios({
    url: api.updatePluginInfo,
    method: 'post',
    data: parameter
  })
}

export function savePluginInfo (parameter) {
  console.log(parameter)
  return axios({
    url: api.savePluginInfo,
    method: 'post',
    data: parameter
  })
}

export function activatePlugin (parameter) {
  return axios({
    url: api.activatePlugin,
    method: 'post',
    data: parameter
  })
}

export function removePlugin (parameter) {
  return axios({
    url: api.removePlugin,
    method: 'post',
    data: parameter
  })
}
