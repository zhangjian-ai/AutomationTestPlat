<template>
  <div class="input_place">
    <div id="login"></div>
  </div>
</template>
<script>
/* eslint-disable */
import { login_by_ding } from "@/api";
export default {
  methods: {
    // 钉钉登陆
    login() {
      login_by_ding().then(res => {
        // 展示二维码
        var obj = DDLogin({
          id: "login", //这里需要你在自己的页面定义一个HTML标签并设置id，例如<div id="login_container"></div>或<span id="login_container"></span>
          goto: encodeURIComponent(res.data.url), //请参考注释里的方式
          style: "border:none;background-color:#FFFFFF;",
          width: "250",
          height: "300"
        });

        // 定义监听扫码事件
        var handleMessage = function(event) {
          var origin = event.origin;
          if (origin == "https://login.dingtalk.com") {
            //判断是否来自ddLogin扫码事件。
            var loginTmpCode = event.data;
            //获取到loginTmpCode后就可以在这里构造跳转链接
            login_by_ding(loginTmpCode).then(res => {
              location.href = res.data.url;
            });
          }
        };

        // 在当前窗口增加监听事件
        if (typeof window.addEventListener != "undefined") {
          window.addEventListener("message", handleMessage, false);
        } else if (typeof window.attachEvent != "undefined") {
          window.attachEvent("onmessage", handleMessage);
        }
      });
    }
  },
  mounted() {
    this.login();
  }
};
</script>
<style scoped>
</style>