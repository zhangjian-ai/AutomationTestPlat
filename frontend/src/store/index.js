import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // 用户状态信息
    nickname: sessionStorage.nickname || localStorage.nickname,
    token: sessionStorage.token || localStorage.token
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

    }
  },
  actions: {
  },
  modules: {
  }
})
