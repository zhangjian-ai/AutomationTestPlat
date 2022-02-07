import Vue from 'vue'
import Vuex from 'vuex'

import { get_image, get_file, modules, user_list, get_constants, case_tree, job_inductions, get_public_key } from "@/api";


Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // 服务器公钥
    public_key: "",

    // 用户状态信息
    nickname: sessionStorage.nickname || localStorage.nickname,
    token: sessionStorage.token || localStorage.token,

    // 模块下拉列表
    modules: [],

    // 用例等级
    priorities: [],

    // 用户列表
    users: [],

    // 测试任务信息
    levels: [],
    categories: [],
    status: [],
    case_status: [],

    // 静态图片链接
    logo_url: "",
    login_url: "",
    auto_true: "",
    auto_false: "",
    loading: "",

    // 静态文件链接
    xmind_template_id: 0,

    // 树结构用例列表
    case_tree: [],

    // 统计饼图变量
    pie_data: [],
    pie_colors: [],
    pie_category: [],
    pie_title: "",
    pie_scope: ""

  },
  mutations: {
    // 保存公钥
    setPublicKey(state, payload) {
      state.public_key = payload
    },

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
    // 模块级联选择器数据
    setModules(state, payload) {
      if (payload) {
        state.modules = payload
      }
    },
    // 用例优先级
    setPriorities(state, payload) {
      if (payload) {
        state.priorities = payload
      }
    },
    // 用户列表
    setUsers(state, payload) {
      if (payload) {
        state.users = payload
      }
    },
    // 测试任务下拉框
    setJobInfo(state, payload) {
      if (payload) {
        state.levels = payload.LEVEL;
        state.categories = payload.TYPE;
        state.status = payload.STATUS;
        state.case_status = payload.CASE_STATUS
      }
    },
    // 设置系统图片链接
    setImageUrl(state, payload) {
      if (payload) {
        state.logo = payload.logo;
        state.login = payload.login;
        state.loading = payload.loading;
      }
    },
    // 设置系统静态文件链接
    setStaticFile(state, payload) {
      if (payload) {
        state.xmind_template_id = payload.xmind_template
      }
    },
    // 创建任务页面的用例列表
    setCaseTree(state, payload) {
      if (payload) {
        state.case_tree = payload
      }
    },

    // 创建任务页面的用例列表
    setPie(state, payload) {
      if (payload) {
        state.pie_data = payload.data;
        state.pie_colors = payload.colors;
        state.pie_category = payload.category;
        state.pie_title = payload.title;
        state.pie_scope = payload.scope;
      }
    },

  },
  actions: {
    // 加载公钥
    loadPublicKey(context) {
      get_public_key().then(res => {
        context.commit("setPublicKey", res.data.key)
      })
    },

    // 加载搜索栏下拉框
    loadOption(context) {
      modules().then(res => {
        context.commit("setModules", res.data);
      });
      get_constants("CASE").then(res => {
        context.commit("setPriorities", res.data.LEVEL);
      });
      get_constants("JOB").then(res => {
        context.commit("setJobInfo", res.data);
      });
      user_list().then(res => {
        context.commit("setUsers", res.data);
      });
    },

    // 加载Image
    loadImage(context) {
      get_image().then(res => {
        context.commit("setImageUrl", res.data);
      });
    },

    // 加载静态文件
    loadStaticFile(context) {
      get_file().then(res => {
        context.commit("setStaticFile", res.data)
      })
    },

    // 获取用例列表树数据
    caseTree(context) {
      case_tree().then(res => {
        context.commit("setCaseTree", res.data);
      });
    },

    // 任务统计
    jobInductions(context) {
      job_inductions().then(res => {
        context.commit("setPie", res.data);
      });
    }
  },
  modules: {
  }
})
