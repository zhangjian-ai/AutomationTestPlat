<template>
  <div v-if="loading" style="text-align: center;">
    <el-image :src="url"></el-image>
    <p style="font-size: 2em;">客官莫急 俺正努力</p>
  </div>
  <div v-else class="main">
    <div class="box">
      <div class="sub_box">
        <p class="title">
          欢迎您，
          <span style="color: red;">{{logonForm.nickname}} 吴迪</span> :
        </p>
        <p class="text">您是首次登陆本平台，请先完成注册以授权。</p>
        <el-divider></el-divider>
        <!-- 主要内容 -->
        <logon :ding="true" :form="logonForm"></logon>
        <el-divider></el-divider>
      </div>
    </div>
  </div>
</template>
<script>
import { ding_login, get_image } from "@/api";
import logon from "@/components/login/logon.vue";
export default {
  data() {
    return {
      // 回调地址中的code
      code: "",

      // 加载等待，gif地址
      loading: true,
      url: "",

      // 首次扫码时，注册表单
      logonForm: {}
    };
  },
  methods: {
    // 获取钉钉code
    getCode() {
      // 获取回调地址中code的值
      let url = window.location.href;
      let paramsSet = url.substr(url.lastIndexOf("?") + 1).split("&");
      paramsSet.forEach(value => {
        let key = value.split("=")[0];
        let val = value.split("=")[1];
        if (key == "code") {
          this.code = val;
        }
      });
    },
    // 登陆
    loginByDing(code) {
      ding_login(code).then(res => {
        // 判断后端返回值
        if (res.status == 202) {
          // 判断钉钉账号是否有效
          // !res.data.active
          if (!res.data.active) {
            this.$message.error("当前登陆账号已失效，请重新登录");
            setTimeout(() => {
              this.$router.replace("/login/dingtalk");
            }, 2000);
          }
          // 有效则调用注册组件
          this.logonForm = res.data;
          if (delete this.logonForm.active) {
            this.loading = false;
          }
          return;
        } else {
          // 保存用户信息
          this.$store.commit("setStatus", res.data);
          // 跳转到主页
          this.$router.push("/");
        }
      });
    },

    // 加载image
    loadImage() {
      get_image("login").then(res => {
        this.url = res.data.loading;
      });
    }
  },
  mounted() {
    this.loadImage();
    this.getCode();
    this.loginByDing(this.code);
  },
  components: {
    logon
  }
};
</script>
<style scoped>
.main {
  width: 100%;
  height: 100%;
}
.title {
  text-align: left;
  margin: 0.5em;
}
.text {
  text-align: left;
  font-size: 0.8em;
  color: red;
  margin: 0.5em;
}
.el-divider {
  padding: 0.3px;
  background-color: red;
}
.box {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  border-radius: 5px;
  background-color: whitesmoke;
  width: 24em;
}
.sub_box {
  width: 22em;
  text-align: center;
  margin-left: 1em;
}
</style>