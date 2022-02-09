import Vue from 'vue'
import VueRouter from 'vue-router'

// 解决当前子路由跳转报错,本质上就是捕获这个异常不上报
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'login',
    // component: (resolve) => require(['@/views/login.vue'], resolve)  懒加载，构建时生成多个js文件；webpack > 2.4 时，用下面的更简单
    component: () => import('@/views/login.vue'),
    children: [
      {
        path: 'account',
        name: 'login_by_account',
        component: () => import('@/components/login/loginByAccount.vue'),
        meta: {
          title: "登录"
        },
      },
      {
        path: 'mobile',
        name: 'login_by_mobile',
        component: () => import('@/components/login/loginByMobile.vue'),
        meta: {
          title: "手机号登录"
        },
      },
      {
        path: 'dingtalk',
        name: 'login_by_dingtalk',
        component: () => import('@/components/login/loginByDingtalk.vue'),
        meta: {
          title: "钉钉扫码登录"
        },
      },
      {
        path: 'logon',
        name: 'logon',
        component: () => import('@/components/login/logon.vue'),
        meta: {
          title: "注册"
        }
      },
    ]
  },
  {
    path: '/callBack',
    name: 'call_back',
    component: () => import('@/components/login/callBackByDingtalk.vue'),
  },
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/home.vue'),
    meta: {
    },
    children: [
      {
        path: '',
        name: 'induction',
        component: () => import('@/components/home/induction.vue'),
        meta: {
          title: "统计看板",
          requireAuth: true
        },
      },
      {
        path: 'caseList',
        name: 'case_list',
        component: () => import('@/components/home/caseList.vue'),
        meta: {
          title: "用例列表",
          requireAuth: true
        },
      },
      {
        path: 'caseCreate',
        name: 'case_create',
        component: () => import('@/components/home/caseCreate.vue'),
        meta: {
          title: "新建用例",
          requireAuth: true
        },
      },
      {
        path: 'jobCreate',
        name: 'job_create',
        component: () => import('@/components/home/jobCreate.vue'),
        meta: {
          title: "新建任务",
          requireAuth: true
        },
      },
      {
        path: 'jobList',
        name: 'job_list',
        component: () => import('@/components/home/jobList.vue'),
        meta: {
          title: "任务列表",
          requireAuth: true
        },
      },
      {
        path: 'apiTest',
        name: 'api_test',
        component: () => import('@/components/home/apiTest.vue'),
        meta: {
          title: "接口测试",
          requireAuth: true
        },
      },
      {
        path: 'sourceList',
        name: 'source_list',
        component: () => import('@/components/home/sourceList.vue'),
        meta: {
          title: "资源列表",
          requireAuth: true,
          keepAlive: true
        },
      },
      {
        path: 'workPlat',
        name: 'work_plat',
        component: () => import('@/components/home/workPlat.vue'),
        meta: {
          title: "我的工作台",
          requireAuth: true
        },
      },
    ]
  },

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
