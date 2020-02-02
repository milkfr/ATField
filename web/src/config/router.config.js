// eslint-disable-next-line
import { UserLayout, BasicLayout, RouteView, BlankLayout, PageView } from '@/layouts'

export const asyncRouterMap = [

  {
    path: '/',
    name: 'index',
    component: BasicLayout,
    meta: { title: '首页' },
    redirect: '/auth/user',
    children: [
      // auth
      {
        path: '/auth',
        name: 'auth',
        redirect: '/auth/permission',
        component: RouteView,
        meta: { title: '访问控制', keepAlive: true, icon: 'user', permission: [ 'manager_auth.permission', 'manager_auth.role', 'manager_auth.user' ] },
        children: [
          {
            path: '/auth/permission',
            name: 'Permission',
            component: () => import('@/views/auth/Permission'),
            meta: { title: '权限列表', keepAlive: true, permission: [ 'manager_auth.permission' ] }
          },
          {
            path: '/auth/role',
            name: 'Role',
            component: () => import('@/views/auth/Role'),
            meta: { title: '角色列表', keepAlive: true, permission: [ 'manager_auth.role' ] }
          },
          {
            path: '/auth/user',
            name: 'User',
            component: () => import('@/views/auth/User'),
            meta: { title: '用户列表', keepAlive: true, permission: [ 'manager_auth.user' ] }
          }
        ]
      },

      // forms
      {
        path: '/asset',
        name: 'asset',
        redirect: '/asset/host',
        component: RouteView,
        meta: { title: '资产列表', icon: 'form', permission: [ 'manager_asset.host', 'manager_asset.domain', 'manager_asset.service' ] },
        children: [
          {
            path: '/asset/host',
            name: 'Host',
            component: () => import('@/views/asset/Host'),
            meta: { title: '主机列表', keepAlive: true, permission: [ 'manager_asset.host' ] }
          },
          {
            path: '/asset/domain',
            name: 'Domain',
            component: () => import('@/views/asset/Domain'),
            meta: { title: '域名列表', keepAlive: true, permission: [ 'manager_asset.domain' ] }
          },
          {
            path: '/asset/service',
            name: 'Service',
            component: () => import('@/views/asset/Service'),
            meta: { title: '服务列表', keepAlive: true, permission: [ 'manager_asset.service' ] }
          },
          {
            path: '/asset/http',
            name: 'HTTP',
            component: () => import('@/views/asset/HTTP'),
            meta: { title: 'HTTP应用列表', keepAlive: true, permission: [ 'manager_asset.http' ] }
          },
          {
            path: '/asset/cgi',
            name: 'CGI',
            component: () => import('@/views/asset/CGI'),
            meta: { title: 'CGI列表', keepAlive: true, permission: [ 'manager_asset.cgi' ] }
          },
          {
            path: '/asset/zone',
            name: 'Zone',
            component: () => import('@/views/asset/Zone'),
            meta: { title: '区域列表', keepAlive: true, permission: [ 'manager_asset.zone' ] }
          }
        ]
      },

      // forms
      {
        path: '/scanner',
        name: 'scanner',
        redirect: '/scanner/plugin',
        component: RouteView,
        meta: { title: '扫描任务', icon: 'profile', permission: [ 'manager_scanner.plugin', 'manager_scanner.task' ] },
        children: [
          {
            path: '/scanner/plugin',
            name: 'Plugin',
            component: () => import('@/views/scanner/Plugin'),
            meta: { title: '插件列表', keepAlive: true, permission: [ 'manager_scanner.plugin' ] }
          },
          {
            path: '/scanner/Task',
            name: 'Task',
            component: () => import('@/views/scanner/Task'),
            meta: { title: '任务列表', keepAlive: true, permission: [ 'manager_scanner.task' ] }
          }
        ]
      },

      // Exception
      {
        path: '/exception',
        name: 'exception',
        component: RouteView,
        redirect: '/exception/403',
        meta: { title: '异常页', icon: 'warning', permission: [ 'exception' ] },
        children: [
          {
            path: '/exception/403',
            name: 'Exception403',
            component: () => import(/* webpackChunkName: "fail" */ '@/views/exception/403'),
            meta: { title: '403', permission: [ 'exception' ] }
          },
          {
            path: '/exception/404',
            name: 'Exception404',
            component: () => import(/* webpackChunkName: "fail" */ '@/views/exception/404'),
            meta: { title: '404', permission: [ 'exception' ] }
          },
          {
            path: '/exception/500',
            name: 'Exception500',
            component: () => import(/* webpackChunkName: "fail" */ '@/views/exception/500'),
            meta: { title: '500', permission: [ 'exception' ] }
          }
        ]
      }

    ]
  },
  {
    path: '*', redirect: '/404', hidden: true
  }
]

/**
 * 基础路由
 * @type { *[] }
 */
export const constantRouterMap = [
  {
    path: '/user',
    component: UserLayout,
    redirect: '/user/login',
    hidden: true,
    children: [
      {
        path: 'login',
        name: 'login',
        component: () => import(/* webpackChunkName: "user" */ '@/views/user/Login')
      }
    ]
  },

  {
    path: '/test',
    component: BlankLayout,
    redirect: '/test/home',
    children: [
      {
        path: 'home',
        name: 'TestHome',
        component: () => import('@/views/Home')
      }
    ]
  },

  {
    path: '/404',
    component: () => import(/* webpackChunkName: "fail" */ '@/views/exception/404')
  }

]
