<template>
  <div class="main" :style="{backgroundImage: 'url('+$store.state.login_url+')',backgroundSize: '100% 100%'}">
    <!-- 内容盒子 -->
    <el-row class="box">
      <div class="sub_box">
        <p class="title">{{title[titleIndex]}}</p>
        <el-divider></el-divider>
        <div>
          <router-view />
        </div>
        <el-divider></el-divider>
        <div class="links">
          <el-col :span="4">
            <el-link
              :underline="false"
              :disabled="loginEnable"
              @click="changeLoginType(1)"
            >{{ otherType1[1] }}</el-link>
          </el-col>
          <el-col :span="5">
            <el-link
              :underline="false"
              :disabled="loginEnable"
              @click="changeLoginType(2)"
            >{{ otherType2[1] }}</el-link>
          </el-col>
          <el-col :span="14">
            <el-link
              icon="el-icon-edit"
              :underline="false"
              @click="goLogon()"
            >{{titleLink[titleIndex]}}</el-link>
          </el-col>
        </div>
      </div>
    </el-row>
  </div>
</template>
<script>
export default {
  data() {
    return {
      // 注册登陆切换
      title: ["用 户 登 陆", "用 户 注 册"],
      titleLink: ["立即注册", "已有账号"],
      titleIndex: 0,

      loginEnable: false,

      // 登陆方式切换，path
      currentType: ["/login/account", "账号密码"],
      otherType1: ["/login/mobile", "手机登陆"],
      otherType2: ["/login/dingtalk", "钉钉扫码"]
    };
  },
  methods: {
    // 去注册
    goLogon() {
      // 登陆使能
      this.loginEnable = this.loginEnable == true ? false : true;

      // 文本变更
      this.titleIndex = this.titleIndex == 1 ? 0 : 1;

      // 路由变更
      this.$router.replace(
        this.titleIndex == 1 ? "/login/logon" : "/login/account"
      );
    },
    // 切换登陆方式
    changeLoginType(type) {
      if (type == 1) {
        // 交换两个变量的值，ES6解构赋值
        [this.currentType, this.otherType1] = [
          this.otherType1,
          this.currentType
        ];
        this.$router.replace(this.currentType[0]);
      }
      if (type == 2) {
        [this.currentType, this.otherType2] = [
          this.otherType2,
          this.currentType
        ];
        this.$router.replace(this.currentType[0]);
      }
    }
  },
  mounted() {
    // 加载服务器公钥
    this.$store.dispatch("loadPublicKey");

    // 避免一些奇怪的问题出现
    this.$router.replace("/login/account");

    // 加载背景图片
    this.$store.dispatch("loadImage");
  }
};
</script>
<style scoped>
.main {
  margin: 0px;
  padding: 0px;
  width: 100%;
  height: 100%;
  text-align: center;
}
.title {
  font-size: 1.5em;
  color: red;
}
.el-divider {
  padding: 0.5px;
  background-color: tomato;
}

.box {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  border-radius: 5px;
  background-color: rgba(245, 245, 245, 0.5);
  width: 24em;
  text-align: center;
}
.sub_box {
  width: 22em;
  margin-left: 1em;
  text-align: center;
}
.links {
  text-align: right;
  margin-bottom: 4em;
}
</style>