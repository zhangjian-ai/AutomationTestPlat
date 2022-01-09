<template>
  <div class="upload">
    <!-- 文件导入区域 -->
    <el-upload
      style="min-height: 8em; margin-bottom: 1em;"
      ref="upload"
      :limit="1"
      action
      accept=".zip, .rar, .tar, .gz, .exe, .dmg, .apk, .ipa"
      :on-change="handleChange"
      :http-request="handleHttpRequest"
      :auto-upload="false"
    >
      <el-button slot="trigger" size="mini" type="primary" :disabled="state">选取文件</el-button>
      <el-button
        style="margin: 0 2em;"
        size="mini"
        type="success"
        :disabled="state"
        @click="$refs.upload.submit()"
      >点击上传</el-button>
      <span slot="tip" class="tips">{{ message }}</span>
    </el-upload>
    <el-form
      :model="sourceForm"
      size="mini"
      :rules="rules"
      v-show="showSourceInfo"
      ref="sourceForm"
    >
      <el-form-item label="资源名称:" prop="name" label-width="25%">
        <el-input v-model="sourceForm.name" disabled></el-input>
      </el-form-item>
      <el-form-item label="资源大小:" prop="size" label-width="25%">
        <el-input v-model="sourceForm.size" disabled></el-input>
      </el-form-item>
      <el-form-item label="操作系统:" prop="os" label-width="25%">
        <el-select v-model="sourceForm.os" placeholder="请选操作系统">
          <el-option label="Windows" value="Windows"></el-option>
          <el-option label="MacOS" value="MacOS"></el-option>
          <el-option label="Linux/Unix" value="Linux/Unix"></el-option>
          <el-option label="Android" value="Android"></el-option>
          <el-option label="IOS" value="IOS"></el-option>
          <el-option label="未知" value="未知"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="版本号:" prop="version" label-width="25%">
        <el-input v-model="sourceForm.version" placeholder="例如: jdk1.8"></el-input>
      </el-form-item>
      <el-form-item label="描述信息:" prop="desc" label-width="25%">
        <el-input
          v-model="sourceForm.desc"
          type="textarea"
          placeholder="最多输入48个字符"
          show-word-limit
          :autosize="{ minRows: 1, maxRows: 2}"
          maxlength="48"
        ></el-input>
      </el-form-item>
    </el-form>
    <el-progress :percentage="percentage" v-show="showProgress"></el-progress>
  </div>
</template>
<script>
/* eslint-disable */
import axios from "axios";

import { uploadXmindCase, download } from "@/api";

export default {
  props: [],
  data() {
    return {
      // 提示信息
      message: "",

      // 资源信息表单
      showSourceInfo: false,
      sourceForm: {},
      rules: {
        os: [
          {
            required: true
          }
        ],
        version: [
          {
            required: true
          }
        ]
      },

      // 进度条
      showProgress: false,
      finish: 0,
      total: 1,

      // 按钮状态
      state: false
    };
  },
  methods: {
    // 自定义上传方法
    handleHttpRequest(file) {
      // 校验表单
      this.$refs.sourceForm.validate(valid => {
        console.log(file.file.size);

        if (valid) {
          // 建立WebSocket连接
          this.socket = new WebSocket(
            `ws://${axios.defaults.baseURL.split("/")[2]}/ws/upload/`
          );

          // 隐藏表单
          this.showSourceInfo = false;

          // 建立连接成功时回调
          this.socket.onopen = event => {
            // 展示上传进度条
            this.showProgress = true;

            // 变更提示信息
            this.message = "文件上传中...";

            // 置灰按钮
            this.state = true;
            this.$emit("changeState", true);

            // 清空已上传文件大小，保存文件大小
            this.finish = 0;
            this.total = file.file.size;

            // 发送资源信息到后端
            this.socket.send(JSON.stringify(this.sourceForm));
          };

          // 接收到服务器消息的回调
          this.socket.onmessage = event => {
            // 提取服务器消息
            let recvs = event.data.split(".");

            if (recvs[0] == "continue" && this.finish < this.total) {
              // 切割file，每次发送 102400 个字节到后端
              let content = file.file.slice(this.finish, this.finish + 102400);

              // 发送数据
              this.socket.send(content);

              // 更新finish
              this.finish += content.size;
            }
            if (recvs[0] == "saving") {
              // 更新提示信息（写入进度/异常信息）
              this.message = recvs[1];
            }

            if (recvs[0] == "close") {
              // 接收到 close 标识，表示上传完成，主动触发上传成功原生效果
              file.onSuccess();

              // 更新提示信息
              this.message = recvs[1];
            }
          };

          // 接收到服务器发起的关闭消息时的回调
          this.socket.onclose = event => {
            if (event.type == "close") {
              // 客户端同步断开连接
              this.socket.close();

              // 使能按钮
              this.state = false;
              this.$emit("changeState", false);
            }
          };
        }
      });
    },

    // 文件添加时回调
    handleChange(file, fileList) {
      // 仅在文件添加阶段校验。file常用属性：name，status
      // 添加文件时状态：ready；上传成功：success；上传失败：error
      if (file.status == "ready") {
        // 重置提示信息
        this.message = "提示: 选取文件后请继续完善资源相关信息";

        // 清空表单信息
        this.sourceForm = {};

        // 展示信息表单并回填资源信息
        this.showProgress = false;
        this.showSourceInfo = true;

        this.sourceForm.uid = file.uid;
        this.sourceForm.name = file.name;
        this.sourceForm.size = Math.round(file.size / 10000) / 100 + "M";
        this.sourceForm.size_bytes = file.size;

        // 添加提供者信息
        this.sourceForm.provider = this.$store.state.nickname;
      }
    },

    // 下载模板
    download_xmind_template() {
      download(this.$store.state.xmind_template_id).then(res => {
        let content = res.data;
        // FileReader主要用于将文件内容读入内存
        let reader = new FileReader();
        reader.readAsDataURL(content);
        // onload当读取操作成功完成时调用
        reader.onload = function(e) {
          // 创建一个超链接标签a
          let a = document.createElement("a");
          // 获取文件名fileName
          let fileName = res.headers["content-dispositon"].split("=");
          // 直接调用属性名设置download属性
          a.download = fileName[fileName.length - 1];
          // 这是href属性，另一种设置属性的方法
          a.setAttribute("href", e.target.result);
          // 将其添加到body中，点击时调用href，然后再删除 a 标签
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
        };
      });
    }
  },
  computed: {
    percentage() {
      return Math.floor((this.finish / this.total) * 100);
    }
  }
};
</script>
<style scoped>
.tips {
  display: block;
  margin: 2em 0 0;
  font-size: 0.5em;
  color: grey;
}
.el-form-item {
  width: 90%;
}
.el-input,
.el-select {
  width: 100%;
}
</style>
