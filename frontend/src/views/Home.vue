<template>
  <el-container>
    <el-aside>
      <!-- 菜单 -->
      <el-menu
        router
        :default-active="$route.path"
        unique-opened
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
      >
        <!-- LOGO -->
        <el-image :src="url"></el-image>
        <el-submenu index="1">
          <template slot="title">用例管理</template>
          <el-menu-item index="/caseList">
            <span slot="title">用例列表</span>
          </el-menu-item>
          <el-menu-item index="/caseCreate">
            <span slot="title">新建用例</span>
          </el-menu-item>
        </el-submenu>
        <el-submenu index="2">
          <template slot="title">任务管理</template>
          <el-menu-item index="/jobList">
            <span slot="title">任务列表</span>
          </el-menu-item>
          <el-menu-item index="/jobCreate">
            <span slot="title">新建任务</span>
          </el-menu-item>
        </el-submenu>
      </el-menu>
    </el-aside>
    <el-main>
      <!-- 头部 面包屑 -->
      <div class="header">
        <el-col :span="5">
          <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{$route.meta.title}}</el-breadcrumb-item>
          </el-breadcrumb>
        </el-col>
        <el-col :span="18">
          <el-link :underline="false">
            您好:
            <span>{{ $store.state.nickname }}</span>
          </el-link>
          <el-divider direction="vertical"></el-divider>
          <el-link :underline="false" @click="$router.push('/workPlat')">工作台</el-link>
          <el-divider direction="vertical"></el-divider>
          <el-link :underline="false" @click="logout()">注销</el-link>
        </el-col>
      </div>
      <el-divider></el-divider>
      <!-- 主体部分 -->
      <div>
        <router-view />
      </div>
    </el-main>
  </el-container>
</template>
<script>
import { get_image, modules, user_list, get_constants } from "@/api";
export default {
  data() {
    return {
      // LOGO
      url: ""
    };
  },
  methods: {
    // 注销登陆
    logout() {
      this.$store.commit("setStatus");
      this.$router.replace("/login/account");
    },

    // 加载Image
    loadImage() {
      get_image("home").then(res => {
        this.url = res.data.logo;
      });
      get_image("case").then(res => {
        this.$store.commit("setCaseIcons", res.data);
      });
    },

    // 加载搜索栏下拉框
    loadOption() {
      modules().then(res => {
        this.$store.commit("setModules", res.data);
      });
      get_constants("CASE").then(res => {
        this.$store.commit("setPriorities", res.data.LEVEL);
      });
      get_constants("JOB").then(res => {
        this.$store.commit("setJobInfo", res.data);
      });
      user_list().then(res => {
        this.$store.commit("setUsers", res.data);
      });
    }
  },
  mounted() {
    this.loadImage();
    this.loadOption();
  }
};
</script>
<style scoped>
.el-container {
  width: 100%;
  height: 100%;
}
.el-aside {
  text-align: center;
  width: 12% !important;
}
.el-aside .el-menu {
  width: 100%;
  height: 100%;
}
.el-menu-item {
  min-width: 100%;
  background: #39424b !important;
}
.el-menu-item.is-active {
  background: #3a6b9c !important;
}
.el-menu-item:hover {
  background: #294c6e !important;
}
.el-menu /deep/ .el-submenu__title:hover {
  background: #294c6e !important;
}

.header {
  height: 1.5em;
  line-height: 1.5em;
  text-align: right;
}
.header span {
  color: #ee7700;
  font-weight: bolder;
}
.header .el-breadcrumb {
  padding: 0.5em 0;
}
.header .el-link {
  margin: 0 0.6em;
  padding: 0 0.4em;
}
.header .el-link:hover {
  background: #dcdcdc;
  border-radius: 3px;
}

.el-divider {
  margin: 0.5em 0;
  background-color: gray;
}
.el-main {
  padding: 0.5em 1em;
}
</style>