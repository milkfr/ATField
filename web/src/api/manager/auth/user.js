import api from '@/api/index'
import { axios } from '@/utils/request'

export function getUserList (parameter) {
  return axios({
    url: api.getUserList,
    method: 'get',
    params: parameter
  })
}

export function updateUserInfo (parameter) {
  return axios({
    url: api.updateUserInfo,
    method: 'post',
    data: parameter
  })
}

export function saveUserInfo (parameter) {
  return axios({
    url: api.saveUserInfo,
    method: 'post',
    data: parameter
  })
}

export function activateUser (parameter) {
  return axios({
    url: api.activateUser,
    method: 'post',
    data: parameter
  })
}

export function removeUser (parameter) {
  return axios({
    url: api.removeUser,
    method: 'post',
    data: parameter
  })
}
