<template>
  <div class="upload">
    <!-- 文件导入区域 -->
    <div class="clear">
      <el-button size="mini" @click="$refs.upload.clearFiles();">清空列表</el-button>
    </div>
    <el-upload
      style="width: 30%; min-height: 8em; margin-bottom: 1em;"
      ref="upload"
      action
      multiple
      accept=".xmind"
      :limit="5"
      :on-exceed="handleLimit"
      :on-change="handleChange"
      :on-success="handleSuccess"
      :on-error="handleError"
      :http-request="handleHttpRequest"
      :auto-upload="false"
    >
      <el-button slot="trigger" size="mini" type="primary">选取文件</el-button>
      <el-button style="margin: 0 2em;" size="mini" type="success" @click="submit()">点击上传</el-button>
      <el-link
        style="padding-top: 0.5em;"
        size="mini"
        icon="el-icon-download"
        type="primary"
        :href="$store.state.xmind_template_url"
      >xmind 模版</el-link>
      <el-button
        v-show="ids.length > 0"
        style="margin-left: 2em;"
        size="mini"
        type="danger"
        @click="$router.push({name: 'job_create', params: {ids: ids}})"
      >同步创建任务</el-button>
      <span v-if="loading" style="margin-left: 1em; color: grey; margin-bottom: 0;">
        <i class="el-icon-loading" slot="suffix"></i>用例导入中···
      </span>
      <div slot="tip" class="tips">提示: 只能上传xmind文件</div>
    </el-upload>
    <!-- 导入结果展示 -->
    <transition name="el-zoom-in-top">
      <div class="result" v-show="show">
        <div v-show="title.replace(/[\r\n]/g,'')">
          <span class="title">{{ title }}</span>
        </div>
        <div v-show="error.replace(/[\r\n]/g,'')">
          <span class="title">
            <br />导入异常:
            <br />
          </span>
          <span>{{ error }}</span>
        </div>
        <div v-show="success.replace(/[\r\n]/g,'')">
          <span class="title">
            <br />用例详情:
            <br />
          </span>
          <span>{{ success }}</span>
        </div>
      </div>
    </transition>
  </div>
</template>
<script>
/* eslint-disable */
import { uploadXmindCase } from "@/api";
export default {
  props: [],
  data() {
    return {
      // 上传结果
      title: "",
      error: "",
      success: "",

      // 用例统计
      count: 0,

      // 结果展示
      show: false,
      loading: false,

      // 上传用例id
      ids: []
    };
  },
  methods: {
    // 自定义上传方法
    async handleHttpRequest(file) {
      this.loading = true;

      // 创建上传表单并添加文件
      let form = new FormData();
      form.append("file", file.file);

      // 使用 http-request 参数来自定义上传行为
      // 使用这个参数之后，on-success，和on-progress就不起作用了，可以这样做
      // 接口返回成功时处理，调用onSuccess，手动触发on-success钩子函数，需要手动传入response
      // onProgress 同理
      // 能够复用el-upload原生的一些动作
      const res = await uploadXmindCase(form);
      // 同步操作
      this.show = true;
      this.loading = false;
      if (res.status == 201) {
        file.onSuccess(res);
      }
      if (res.status == 200) {
        file.onError(res);
      }
    },

    // 确认提交
    submit() {
      this.show = false;
      this.clearResult();
      this.$refs.upload.submit();
    },

    // 文件添加时校验
    handleChange(file, fileList) {
      // 仅在文件添加阶段校验。file常用属性：name，status
      // 添加文件时状态：ready；上传成功：success；上传失败：error
      if (file.status == "ready") {
        // 重复文件校验
        for (let j = 0; j < fileList.slice(0, -1).length; j++) {
          if (fileList[j].name == file.name) {
            this.$message({
              type: "error",
              message: "同名的文件已存在"
            });
            fileList.splice(-1, 1);
            break;
          }
        }
      }
    },

    // 最大文件数时提示
    handleLimit() {
      this.$message({
        type: "warning",
        message: "上传文件数已达上限"
      });
    },

    // 上传成功时的回调函数
    handleSuccess(response, file, fileList) {
      this.count += response.data.count;
      this.title = `导入用例: ${this.count}`;
      this.success += response.data.success.join("\n") + "\n";
      this.ids = this.ids.concat(response.data.ids);

      // 刷新用例树列表
      this.$store.dispatch("caseTree");
    },

    // 上传失败时的回调函数
    handleError(response, file, fileList) {
      this.error += response.data.error + "\n";
    },

    // 清空导入结果信息
    clearResult() {
      this.title = "";
      this.error = "";
      this.success = "";
      this.count = 0;
      this.show = false;
    }
  }
};
</script>
<style scoped>
.clear {
  margin-bottom: 1em;
}
.upload {
  /* white-space 让换行符\n生效 */
  white-space: pre-line;
  width: inherit;
  height: 40em;
}
.tips {
  margin: 2em 0 0;
  font-size: 0.5em;
  color: orangered;
}
.result {
  position: absolute;
  width: 50%;
  left: 45%;
  top: 0;
  background-color: whitesmoke;
  padding: 1em;
  overflow: auto;
  font-size: 0.9em;
  max-height: 45em;
  border-radius: 0.5em;
}
.result .title {
  font-size: 1.2em;
  font-weight: bolder;
}
</style>
