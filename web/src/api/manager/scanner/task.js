import api from '@/api/index'
import { axios } from '@/utils/request'

export function getTaskList (parameter) {
  return axios({
    url: api.getTaskList,
    method: 'get',
    params: parameter
  })
}

export function updateTaskInfo (parameter) {
  return axios({
    url: api.updateTaskInfo,
    method: 'post',
    data: parameter
  })
}

export function saveTaskInfo (parameter) {
  return axios({
    url: api.saveTaskInfo,
    method: 'post',
    data: parameter
  })
}

export function activateTask (parameter) {
  return axios({
    url: api.activateTask,
    method: 'post',
    data: parameter
  })
}

export function removeTask (parameter) {
  return axios({
    url: api.removeTask,
    method: 'post',
    data: parameter
  })
}

export function enableTask (parameter) {
  return axios({
    url: api.enableTask,
    method: 'post',
    data: parameter
  })
}

export function disableTask (parameter) {
  return axios({
    url: api.disableTask,
    method: 'post',
    data: parameter
  })
}
