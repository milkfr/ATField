import Vue from 'vue'
import { getToken, getUserInfo } from '@/api/manager/auth/login'
import { ACCESS_TOKEN } from '@/store/mutation-types'

const user = {
  state: {
    token: '',
    name: '',
    welcome: '',
    avatar: '',
    roles: [],
    info: {},
    permissions: []
  },

  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token
    },
    SET_NAME: (state, { name, welcome }) => {
      state.name = name
      state.welcome = welcome
    },
    SET_AVATAR: (state, avatar) => {
      state.avatar = avatar
    },
    SET_ROLES: (state, roles) => {
      state.roles = roles
    },
    SET_INFO: (state, info) => {
      state.info = info
    },
    SET_PERMISSIONS: (state, permissions) => {
      state.permissions = permissions
    }
  },

  actions: {
    // 登录
    Login ({ commit }, userInfo) {
      return new Promise((resolve, reject) => {
        getToken(userInfo).then(response => {
          const msg = response.msg
          Vue.ls.set(ACCESS_TOKEN, msg.token, 7 * 24 * 60 * 60 * 1000)
          commit('SET_TOKEN', msg.token)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 获取用户信息
    GetInfo ({ commit }) {
      return new Promise((resolve, reject) => {
        getUserInfo().then(response => {
          const msg = response.msg
          commit('SET_ROLES', msg.roles)
          commit('SET_NAME', msg.name)
          commit('SET_PERMISSIONS', msg.permissions)
          commit('SET_AVATAR', '/favicon.ico')
          // })
          // getInfo().then(response => {
          //   const result = response.result
          //   console.log(response.result)
          //   if (result.role && result.role.permissions.length > 0) {
          //     const role = result.role
          //     role.permissions = result.role.permissions
          //     role.permissions.map(per => {
          //       if (per.actionEntitySet != null && per.actionEntitySet.length > 0) {
          //         const action = per.actionEntitySet.map(action => { return action.action })
          //         per.actionList = action
          //       }
          //     })
          //     role.permissionList = role.permissions.map(permission => { return permission.permissionId })
          //     commit('SET_ROLES', result.role)
          //     commit('SET_INFO', result)
          //   } else {
          //     reject(new Error('getInfo: roles must be a non-null array !'))
          //   }
          //
          //   commit('SET_NAME', { name: result.name, welcome: welcome() })
          //   commit('SET_AVATAR', result.avatar)

          resolve(response)
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 登出
    Logout ({ commit, state }) {
      return new Promise((resolve) => {
        commit('SET_TOKEN', '')
        commit('SET_ROLES', [])
        Vue.ls.remove(ACCESS_TOKEN)
        resolve()

        // logout(state.token).then(() => {
        //   resolve()
        // }).catch(() => {
        //   resolve()
        // })
      })
    }

  }
}

export default user
