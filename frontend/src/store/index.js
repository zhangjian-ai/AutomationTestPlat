import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // 用户状态信息
    nickname: sessionStorage.nickname || localStorage.nickname,
    token: sessionStorage.token || localStorage.token,

    // 模块下拉列表
    modules: [],

    // 用例等级
    priorities: [],

    // 用例自动化图标
    correct: "",
    error: "",

    // 用户列表
    users: [],

    // 测试任务信息
    levels: [],
    categories: [],
    status: [],
    case_status: [],

  },
  mutations: {
    // 修改用户状态
    setStatus(state, payload) {
      if (payload) {
        state.nickname = sessionStorage.nickname = payload.nickname
        state.token = sessionStorage.token = payload.token
      } else {
        state.nickname = ""
        state.token = ""
        sessionStorage.clear()
        localStorage.clear()
      }

    },

    setModules(state, payload) {
      if (payload) {
        state.modules = payload
      }
    },

    setPriorities(state, payload) {
      if (payload) {
        state.priorities = payload
      }
    },

    setCaseIcons(state, payload) {
      if (payload) {
        state.correct = payload.true;
        state.error = payload.false;
      }
    },

    setUsers(state, payload) {
      if (payload) {
        state.users = payload
      }
    },

    setJobInfo(state, payload) {
      if (payload) {
        state.levels = payload.LEVEL;
        state.categories = payload.TYPE;
        state.status = payload.STATUS;
        state.case_status = payload.CASE_STATUS
      }
    },

  },
  actions: {
  },
  modules: {
  }
})
