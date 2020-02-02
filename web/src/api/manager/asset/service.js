import api from '@/api/index'
import { axios } from '@/utils/request'

export function getServiceList (parameter) {
  return axios({
    url: api.getServiceList,
    method: 'get',
    params: parameter
  })
}
