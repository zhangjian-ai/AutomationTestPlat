<template>
  <div class="input_place">
    <el-form :model="loginForm" :rules="rules" ref="ruleForm">
      <el-form-item prop="username">
        <el-input v-model="loginForm.username" placeholder="请输入用户名" suffix-icon="el-icon-user"></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input
          type="password"
          v-model="loginForm.password"
          autocomplete="off"
          placeholder="请输入密码"
          suffix-icon="el-icon-lock"
        ></el-input>
      </el-form-item>
    </el-form>
    <el-button type="danger" @click="submit()">立&nbsp;即&nbsp;登&nbsp;陆</el-button>
  </div>
</template>
<script>
import { login } from "@/api";
export default {
  data() {
    return {
      // 登陆表单
      loginForm: {
        // 登陆类型
        type: "account"
      },
      rules: {
        username: [
          {
            required: true,
            message: "请填写用户名",
            trigger: "blur"
          }
        ],
        password: [
          {
            required: true,
            message: "请填写密码",
            trigger: "blur"
          }
        ]
      }
    };
  },
  methods: {
    submit() {
      login(this.loginForm).then(res => {
        // 保存token信息
        this.$store.commit("setStatus", res.data);
        // 进入主页
        this.$router.replace("/");
      });
    }
  }
};
</script>
<style scoped>
.input_place {
  text-align: left;
  width: 20em;
  margin-left: 2em;
}
.el-input {
  width: 20em;
  margin-top: 1em;
}
.el-button {
  width: 20em;
  margin: 1em 0;
}
</style>