<template>
  <div>
    <div class="header">
      <!-- 搜索栏 -->
      <div class="condition">
        <el-form
          :inline="true"
          :model="conditions"
          size="mini"
          @keyup.enter.native="getSourceList()"
        >
          <el-row>
            <el-col :span="6">
              <el-form-item label="资源名称:">
                <el-input v-model="conditions.name" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="版本信息:">
                <el-input v-model="conditions.version" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="提供者:">
                <el-input v-model="conditions.provider" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="操作系统:">
                <el-select v-model="conditions.os" clearable>
                  <el-option label="Windows" value="Windows"></el-option>
                  <el-option label="MacOS" value="MacOS"></el-option>
                  <el-option label="Linux/Unix" value="Linux/Unix"></el-option>
                  <el-option label="Android" value="Android"></el-option>
                  <el-option label="IOS" value="IOS"></el-option>
                  <el-option label="未知" value="未知"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="上传时间:">
                <el-date-picker
                  v-model="conditions.create_time"
                  type="datetimerange"
                  range-separator="-"
                  start-placeholder="开始时间"
                  end-placeholder="结束时间"
                  value-format="yyyy-MM-dd HH:mm:ss"
                ></el-date-picker>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>

        <!-- 查询操作 -->
        <el-row>
          <el-col :span="2" style="text-align: left;">
            <el-button
              type="success"
              icon="el-icon-upload"
              size="mini"
              @click="dialogVisible = true"
            >资源上传</el-button>
          </el-col>
          <el-col :span="21" style="text-align: right;">
            <el-button
              type="primary"
              icon="el-icon-search"
              size="mini"
              @click="getSourceList()"
              native-type="submit"
            >查询</el-button>
            <el-button type icon="el-icon-refresh-left" size="mini" @click="conditions = {}">重置</el-button>
          </el-col>
        </el-row>
      </div>
    </div>
    <!-- 资源列表展示 -->
    <el-table
      :data="sourceList"
      v-loading="loading"
      max-height="54.3em"
      size="mini"
      :header-cell-style="{background:'#eef1f6',color:'#606266', 'text-align': 'center'}"
    >
      <el-table-column label="序号" type="index" min-width="30%" align="center"></el-table-column>
      <el-table-column prop="uid" label="UID" min-width="120%" align="center"></el-table-column>
      <el-table-column prop="name" label="名称" min-width="200%" align="center"></el-table-column>
      <el-table-column prop="desc" label="简介" min-width="160%" align="center"></el-table-column>
      <el-table-column prop="os" label="操作系统" min-width="80%" align="center"></el-table-column>
      <el-table-column prop="version" label="版本" min-width="60%" align="center"></el-table-column>
      <el-table-column prop="size" label="大小" min-width="100%" align="center"></el-table-column>
      <el-table-column prop="create_time" label="上传时间" min-width="150%" align="center"></el-table-column>
      <el-table-column prop="provider" label="提供者" min-width="100%" align="center"></el-table-column>
      <el-table-column prop="count" label="下载次数" min-width="80%" align="center"></el-table-column>
      <el-table-column label="操作" align="center" min-width="60%">
        <template slot-scope="scope">
          <el-button
            :disabled="showProgress"
            icon="el-icon-download"
            type="primary"
            circle
            size="mini"
            @click="downloadSource(scope.row)"
          ></el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 分页 -->
    <el-row style="text-align: right;">
      <pagination
        :count="count"
        :page.sync="page"
        :page_size.sync="page_size"
        @function="getSource"
      ></pagination>
    </el-row>
    <!-- 资源上传弹窗 -->
    <el-dialog
      title="资源上传"
      :visible.sync="dialogVisible"
      width="30%"
      destroy-on-close
      :show-close="false"
      :close-on-click-modal="false"
    >
      <uploadSource @changeState="value => state = value"></uploadSource>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false" size="mini" :disabled="state">关 闭</el-button>
      </span>
    </el-dialog>
    <!-- 资源下载浮窗 -->
    <transition name="el-zoom-in-bottom">
      <el-card class="box-card" v-show="showProgress">
        <div slot="header" class="clearfix">
          <span>资源下载</span>
        </div>
        <div>
          <span id="source_name">{{ name }}</span>
          <el-progress :percentage="percentage"></el-progress>
        </div>
      </el-card>
    </transition>
  </div>
</template>
<script>
/* eslint-disable */
import axios from "axios";

import pagination from "../common/pagination.vue";
import uploadSource from "../common/uploadSource.vue";

import { source_list } from "@/api";

export default {
  data() {
    return {
      // 资源列表
      sourceList: [],

      //   查询条件
      conditions: {},

      //  加载中
      loading: false,

      //   分页
      count: 0,
      page: 1,
      page_size: 15,

      // 上传弹窗
      state: false,
      dialogVisible: false,

      // 下载资源变量
      content: [],
      name: "",
      cur: 0,
      total: 1,

      // 接收资源标识
      flag: 0,

      // 下载资源进度条
      percentage: 0,
      showProgress: false
    };
  },
  methods: {
    // 获取资源列表
    getSource() {
      this.loading = true;

      source_list(this.page, this.page_size, this.conditions).then(res => {
        this.sourceList = res.data.results;
        this.count = res.data.count;

        this.loading = false;
      });
    },

    // 通过搜索栏查询资源列表
    getSourceList() {
      // 重置当前页
      this.page = 1;
      // 调用查询方法
      this.getSource();
    },

    // 下载资源
    downloadSource(row) {
      // 修改接收标识，重置已接收资源大小
      this.name = "";
      this.content = [];
      this.percentage = this.cur = this.flag = 0;

      // 建立WebSocket连接
      this.socket = new WebSocket(
        `ws://${axios.defaults.baseURL.split("/")[2]}/ws/download/`
      );

      // 建立连接成功时回调
      this.socket.onopen = event => {
        // 发送资源信息到后端
        this.socket.send(row.uid);

        // 展示进度条
        this.showProgress = true;
      };

      // 接收到服务器消息时回调
      this.socket.onmessage = event => {
        // 接收标识为 0 时，解析服务器消息
        if (this.flag == 0) {
          let recvs = event.data.split(".");

          // 按场景处理消息
          if (recvs[0] == "error") {
            // 给出 toast，关闭连接
            this.$message({
              type: "error",
              message: recvs[1]
            });

            this.socket.close();
            this.showProgress = false;
          }

          if (recvs[0] == "prepare") {
            // 此时把 name 当作提示信息用
            this.name = `资源准备中... ${recvs[1]}`;
          }

          if (recvs[0] == "ready") {
            // 判断真实资源大小和预期资源大小是否相同
            if (recvs[1] == row.size_bytes + "") {
              // 保存当前资源总大小
              this.total = row.size_bytes;
              this.flag = 1;

              // 设置资源名称
              this.name = row.name;

              // 告知服务器当前可接受资源
              this.socket.send("receiving");
            } else {
              // 如果资源大小不一致，就 toast 提示并关闭
              this.$message({
                type: "error",
                message: "抱歉，资源已损坏！"
              });

              this.socket.close();
              this.showProgress = false;
            }
          }

          if (recvs[0] == "close") {
            // 关闭socket
            this.socket.close();

            this.showProgress = false;
          }

          return;
        }

        // 接收标识为 1 时，直接保存 bytes 文件
        if (this.flag == 1) {
          this.content.push(event.data);

          // 修改已接收资源长度，计算百分比(这里降低一下计算的频率)
          this.cur += event.data.size;
          if (this.cur % 204800 == 0 || this.cur == this.total) {
            this.percentage = Math.floor((this.cur / this.total) * 100);
          }

          // 判断是否已经全部接收完成
          if (this.cur == this.total) {
            // 保存文件到本地
            // FileReader主要用于将文件内容读入内存
            let reader = new FileReader();
            reader.readAsDataURL(
              new Blob(this.content, { type: "application/octet-stream" })
            );

            // onload当读取操作成功完成时调用
            reader.onload = e => {
              // 创建一个超链接标签a
              let a = document.createElement("a");
              // 直接调用属性名设置download属性，该属性作为下载时的文件名
              a.download = this.name;
              // 这是href属性，另一种设置属性的方法
              a.setAttribute("href", e.target.result);
              // 将其添加到body中，点击时调用href，然后再删除 a 标签
              document.body.appendChild(a);
              a.click();
              document.body.removeChild(a);

              // 发送完成标识
              this.socket.send("complete");
            };

            return;
          }

          // 没接收完成则继续发送接收标识
          this.socket.send("receiving");
        }
      };

      // 接收到服务器发起的关闭消息时的回调
      this.socket.onclose = event => {
        if (event.type == "close") {
          // 客户端同步断开连接
          this.socket.close();

          // 隐藏进度条
          this.showProgress = false;
        }
      };
    }
  },

  created() {
    this.getSource();
  },

  components: {
    pagination,
    uploadSource
  }
};
</script>
<style scoped>
.header {
  background-color: rgb(236, 236, 236);
  padding: 0.5em 0;
  margin-top: 0.5em;
}
.condition {
  width: 98%;
  margin-left: 2%;
  text-align: left;
}
.condition /deep/ .el-form-item__label {
  font-size: 0.8em !important;
  font-weight: 350;
  width: 25%;
}
.condition .el-form-item {
  width: 100%;
}
.condition .el-input,
.condition .el-select {
  min-width: 80%;
}

.el-date-editor--datetimerange.el-input__inner {
  max-width: 12.4em;
}

.el-table {
  width: 100%;
  overflow: auto;
  margin: 1em 0;
}

.box-card {
  z-index: 100;
  width: 20%;
  position: fixed;
  left: 1%;
  top: 85%;
}
/deep/ .el-card__header,
/deep/ .el-card__body {
  padding: 0.5em;
  font-size: 0.8em;
}

#source_name {
  display: block;
  color: grey;
  margin: 0.5em 0;
}
</style>