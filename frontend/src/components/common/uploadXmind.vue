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
        @click="download_xmind_template"
      >xmind 模版</el-link>
      <div class="hiden">
        <el-button
          v-show="ids.length > 0"
          size="mini"
          type="danger"
          @click="$router.push({name: 'job_create', params: {ids: ids}})"
        >同步创建任务</el-button>
        <span v-if="loading" style="color: grey; margin-bottom: 0;">
          <i class="el-icon-loading" slot="suffix"></i>用例导入中···
        </span>
      </div>
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
import { uploadXmindCase, download } from "@/api";
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
          console.log(fileName);
          a.download = fileName[fileName.length - 1];
          // 这是href属性，另一种设置属性的方法
          a.setAttribute("href", e.target.result);
          // 将其添加到body中，点击时调用href，然后再
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
        };
      });
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
.hiden {
  margin-top: 1em;
}
</style>
