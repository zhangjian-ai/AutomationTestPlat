<template>
  <div class="input_place">
    <el-form :model="loginForm" :rules="rules" ref="loginForm">
      <el-form-item prop="mobile">
        <el-input v-model="loginForm.mobile" placeholder="请输入手机号" suffix-icon="el-icon-phone"></el-input>
      </el-form-item>
      <el-form-item prop="smsCode">
        <el-input v-model="loginForm.smsCode" placeholder="验证码" style="width: 10em"></el-input>
        <el-button
          type="primary"
          @click="sendSmsCode()"
          style="width: 8em; margin: 0; margin-left:3em; "
          size="mini"
          :disabled="flag"
        >{{ tip }}</el-button>
      </el-form-item>
    </el-form>
    <el-button type="danger" @click="submit()">立&nbsp;即&nbsp;登&nbsp;陆</el-button>
  </div>
</template>
<script>
// @ 符号等价于 ‘src’
import { send_sms_code, login } from "@/api";
export default {
  data() {
    return {
      // 登陆表单
      loginForm: {
        // 登陆类型
        type: "mobile"
      },
      rules: {
        mobile: [
          {
            required: true,
            pattern: /^1[3-9]{1}\d{9}$/,
            message: "手机号码错误",
            trigger: "blur"
          }
        ],
        smsCode: [
          {
            required: true,
            pattern: /^\d{6}$/,
            message: "验证码错误",
            trigger: "blur"
          }
        ]
      },
      // 短信按钮文本和按钮状态
      tip: "发送验证码",
      flag: false
    };
  },
  methods: {
    submit() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          login(this.loginForm).then(res => {
            // 保存token信息
            this.$store.commit("setStatus", res.data);
            // 进入主页
            this.$router.replace("/");
          });
        }
      });
    },
    sendSmsCode() {
      let pattern = /^1[3-9]{1}\d{9}$/;
      if (!pattern.test(this.loginForm.mobile)) {
        this.$message({
          type: "error",
          message: "手机号非法"
        });
      } else {
        send_sms_code(this.loginForm.mobile).then(() => {
          this.flag = true;
          // 定义一个计数器，倒计时短信发送周期，周期为60s
          let num = 60;
          let timer = setInterval(
            () => {
              if (num == 1) {
                // 销毁计数器
                clearInterval(timer);
                //修改按钮文本和状态
                this.tip = "发送验证码";
                this.flag = false;
              } else {
                num -= 1;
                this.tip = num + " s";
              }
            },
            1000,
            60
          );
        });
      }
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