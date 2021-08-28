<template>
  <div class="sub-box">
    <el-form :model="logonForm" :rules="rules" ref="logonForm" size="mini" label-width="6em">
      <el-form-item prop="username" label="账号">
        <el-input v-model="logonForm.username" :disabled="ding"></el-input>
      </el-form-item>
      <el-form-item prop="nickname" label="昵称">
        <el-input v-model="logonForm.nickname"></el-input>
      </el-form-item>
      <el-form-item prop="email" label="邮箱">
        <el-input v-model="logonForm.email"></el-input>
      </el-form-item>
      <el-form-item prop="password" label="密码">
        <el-input type="password" v-model="logonForm.password"></el-input>
      </el-form-item>
      <el-form-item prop="password2" label="确认密码">
        <el-input type="password" v-model="logonForm.password2"></el-input>
      </el-form-item>
      <el-form-item prop="mobile" label="手机">
        <el-input v-model="logonForm.mobile"></el-input>
      </el-form-item>
      <el-form-item prop="smsCode" label="验证码">
        <el-input v-model="logonForm.smsCode" palceholder="验证码" style="width: 40%;"></el-input>
        <el-button
          type="primary"
          @click="sendSmsCode()"
          style="width: 35%; margin-left:5%;"
          :disabled="flag"
        >{{ tip }}</el-button>
      </el-form-item>
    </el-form>
    <el-button type="danger" @click="submit()">立&nbsp;即&nbsp;注&nbsp;册</el-button>
  </div>
</template>
<script>
/* eslint-disable */
import { send_sms_code, logon, check_user } from "@/api";
export default {
  props: ["ding", "form"],
  data() {
    // 表单校验方法
    const checkUsername = (rule, value, callback) => {
      check_user(value).then(res => {
        if (res.data.count > 0) {
          callback(new Error("用户名已存在"));
        }
        callback();
      });
    };
    const checkEmail = (rule, value, callback) => {
      if (value) {
        let pattern = /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/;
        if (!pattern.test(value)) {
          callback(new Error("邮箱格式错误"));
        }
      }
      callback();
    };
    const checkPassword2 = (rule, value, callback) => {
      if (value != this.logonForm.password) {
        callback(new Error("请确认两次密码一致"));
      }
      callback();
    };
    const checkMobile = (rule, value, callback) => {
      check_user(value).then(res => {
        if (res.data.count > 0) {
          callback(new Error("手机号已被注册"));
        }
        callback();
      });
    };
    return {
      // 注册表单
      logonForm: {},
      // 表单校验规则
      rules: {
        username: [
          {
            required: true,
            pattern: /^[\.\w]{6,18}$/,
            message: "账号由6-18位数字 字母 . 下划线 组成",
            trigger: "blur"
          },
          { validator: checkUsername, trigger: "submit" }
        ],
        nickname: [
          {
            required: true,
            pattern: /^[\u2E80-\u9FFF]{2,8}$/,
            message: "昵称由2-8位中文字符组成",
            trigger: "blur"
          }
        ],
        email: [{ validator: checkEmail, trigger: "blur" }],
        password: [
          {
            required: true,
            pattern: /^\S{8,20}$/,
            message: "密码不合法",
            trigger: "blur"
          }
        ],
        password2: [
          { required: true, message: "确认密码必填", trigger: "blur" },
          { validator: checkPassword2, trigger: "blur" }
        ],
        mobile: [
          {
            required: true,
            pattern: /^1[3-9]{1}\d{9}$/,
            message: "手机号码错误",
            trigger: "blur"
          },
          { validator: checkMobile, trigger: "submit" }
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
      flag: false,

      // 初始化props里面的参数。prop是单向绑定的，不应该在子组件内部改变prop。
      // 之所以有想修改prop中数据的冲动，主要是prop作为初始值传入后，子组件想把它当作局部数据来用。
      // 对于这种情况，官方的说法是定义一个局部变量，并用 prop 的值初始化它
      subForm: this.form
    };
  },
  methods: {
    submit() {
      this.$refs.logonForm.validate(valid => {
        if (valid) {
          logon(this.logonForm).then(res => {
            // 保存token信息
            this.$store.commit("setStatus", res.data);
            // 进入主页
            this.$router.replace("/");
          });
        }
      });
    },
    // 发送短信验证码
    sendSmsCode() {
      let pattern = /^1[3-9]{1}\d{9}$/;
      if (!pattern.test(this.logonForm.mobile)) {
        this.$message({
          type: "error",
          message: "手机号非法"
        });
      } else {
        send_sms_code(this.logonForm.mobile).then(() => {
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
    },
    // 判断props是否传值
    checkProps() {
      if (this.subForm) {
        // this.logonForm = JSON.parse(JSON.stringify(this.subForm));
        this.logonForm = this.subForm;
      }
    }
  },
  mounted() {
    this.checkProps();
  }
};
</script>
<style scoped>
.sub-box {
  text-align: left;
  width: 100%;
}
.el-input {
  width: 80%;
}
.el-button {
  width: 80%;
  margin-left: 10%;
}
</style>