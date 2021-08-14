<template>
  <!-- 二次封装 vue-quill-editor 富文本编辑器 -->
  <!-- npm i vue-quill-editor -->
  <div>
    <!-- 图片上传组件 -->
    <el-upload
      class="avatar-uploader"
      action
      accept=".jpeg, .png, .jpg"
      :show-file-list="false"
      :on-success="uploadSuccess"
      :on-error="uploadError"
      :http-request="handleHttpRequest"
    ></el-upload>

    <quill-editor
      class="editor"
      v-model="content"
      ref="myQuillEditor"
      :options="editorOption"
      @blur="onEditorBlur($event)"
      @focus="onEditorFocus($event)"
      @change="onEditorChange($event)"
    ></quill-editor>
  </div>
</template>
<script>
/* eslint-disable */

// 工具栏配置
const toolbarOptions = [
  ["bold", "italic", "underline", "strike"], // 加粗 斜体 下划线 删除线
  ["blockquote", "code-block"], // 引用  代码块
  [{ header: 1 }, { header: 2 }], // 1、2 级标题
  [{ list: "ordered" }, { list: "bullet" }], // 有序、无序列表
  [{ script: "sub" }, { script: "super" }], // 上标/下标
  [{ indent: "-1" }, { indent: "+1" }], // 缩进
  // [{'direction': 'rtl'}],                         // 文本方向
  [{ size: ["small", false, "large", "huge"] }], // 字体大小
  [{ header: [1, 2, 3, 4, 5, 6, false] }], // 标题
  [{ color: [] }, { background: [] }], // 字体颜色、字体背景颜色
  [{ font: [] }], // 字体种类
  [{ align: [] }], // 对齐方式
  ["clean"], // 清除文本格式
  ["link", "image", "video"] // 链接、图片、视频
];

import { quillEditor } from "vue-quill-editor";
import "quill/dist/quill.core.css";
import "quill/dist/quill.snow.css";
import "quill/dist/quill.bubble.css";

import { uploadImage, deleteRemoteImage } from "@/api";

export default {
  props: {
    /*编辑器的内容*/
    value: {
      type: String
    }
  },

  components: {
    quillEditor
  },

  data() {
    return {
      content: "",
      editorOption: {
        theme: "snow",
        placeholder: "记录您的测试结果",
        modules: {
          toolbar: {
            container: toolbarOptions,
            // container: "#toolbar",
            handlers: {
              image: function(value) {
                if (value) {
                  // 触发input框选择图片文件
                  document.querySelector(".avatar-uploader input").click();
                } else {
                  this.quill.format("image", false);
                }
              }
            }
          }
        }
      },

      // 上传的图片链接
      imageUrls: []
    };
  },

  methods: {
    onEditorBlur() {
      //失去焦点事件
    },

    onEditorFocus() {
      //获得焦点事件
    },

    onEditorChange() {
      // 内容改变事件
      this.$emit("update:value", this.content);
    },

    // 自定义上传方法
    handleHttpRequest(file) {
      // 创建上传表单并添加文件
      let form = new FormData();
      form.append("file", file.file);

      // 使用 http-request 参数来自定义上传行为
      // 使用这个参数之后，on-success，和on-progress就不起作用了，可以这样做
      // 接口返回成功时处理，调用onSuccess，手动触发on-success钩子函数，需要手动传入response
      // onProgress 同理
      // 能够复用el-upload原生的一些动作
      uploadImage(form).then(res => {
        if (res.status == 201) {
          file.onSuccess(res);
        }
        if (res.status == 200) {
          file.onError(res);
        }
      });
    },

    // 富文本图片上传成功
    uploadSuccess(res) {
      // res为图片服务器返回的数据
      // 获取富文本组件实例
      let quill = this.$refs.myQuillEditor.quill;

      // 获取光标所在位置
      let length = quill.getSelection().index;

      // 插入图片  res.url为服务器返回的图片地址 插入<img src='url'/>
      quill.insertEmbed(length, "image", res.data.url);

      // 调整光标到最后
      quill.setSelection(length + 1);

      // 收集图片链接
      this.imageUrls.push(res.data.url);
    },

    // 富文本图片上传失败
    uploadError(res) {
      this.$message.error(res.data.msg);
    },

    // 检查图片是否都被使用,没有使用的图片从服务器删掉
    clearInvalidImage() {
      let index_list = [];
      // 服务器端删除
      this.imageUrls.forEach((value, index) => {
        if (this.content.search(value) < 0) {
          // 调用接口删除该图片
          deleteRemoteImage(value).then(() => {
            index_list.push(index);
          });
        }
      });
      // 本地列表删除
      index_list.forEach(value => {
        this.imageUrls.splice(value, 1);
      });
    },

    // 清空图片列表
    clearImageList() {
      this.imageUrls = [];
    },

    // 删除所有当前图片
    clearAllImage() {
      // 在更新值之前,先清理掉没有使用的图片链接
      if (this.imageUrls.length != 0) {
        // 服务器端删除
        this.imageUrls.forEach(value => {
          // 调用接口删除该图片
          deleteRemoteImage(value);
        });
        // 清空列表
        this.imageUrls = [];
      }
    }
  },
  watch: {
    // 监听value的变化,实现双向实时动态绑定
    // 这里是子组件更新为父组件的值
    // $emit 是把子组件的值传给父组件
    value: function() {
      this.content = this.value;
    }
  }
};
</script> 

<style>
.editor {
  line-height: normal !important;
  margin-top: -2em;
  /* 解决空格被删除的问题 */
  white-space: pre-wrap;
}
.editor img {
  max-height: 15em !important;
}
.ql-snow .ql-tooltip[data-mode="link"]::before {
  content: "请输入链接地址:";
}
.ql-snow .ql-tooltip.ql-editing a.ql-action::after {
  border-right: 0px;
  content: "保存";
  padding-right: 0px;
}

.ql-snow .ql-tooltip[data-mode="video"]::before {
  content: "请输入视频地址:";
}

.ql-snow .ql-picker.ql-size .ql-picker-label::before,
.ql-snow .ql-picker.ql-size .ql-picker-item::before {
  content: "14px";
}
.ql-snow .ql-picker.ql-size .ql-picker-label[data-value="small"]::before,
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="small"]::before {
  content: "10px";
}
.ql-snow .ql-picker.ql-size .ql-picker-label[data-value="large"]::before,
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="large"]::before {
  content: "18px";
}
.ql-snow .ql-picker.ql-size .ql-picker-label[data-value="huge"]::before,
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="huge"]::before {
  content: "32px";
}

.ql-snow .ql-picker.ql-header .ql-picker-label::before,
.ql-snow .ql-picker.ql-header .ql-picker-item::before {
  content: "文本";
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="1"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="1"]::before {
  content: "标题1";
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="2"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="2"]::before {
  content: "标题2";
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="3"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="3"]::before {
  content: "标题3";
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="4"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="4"]::before {
  content: "标题4";
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="5"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="5"]::before {
  content: "标题5";
}
.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="6"]::before,
.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="6"]::before {
  content: "标题6";
}

.ql-snow .ql-picker.ql-font .ql-picker-label::before,
.ql-snow .ql-picker.ql-font .ql-picker-item::before {
  content: "标准字体";
}
.ql-snow .ql-picker.ql-font .ql-picker-label[data-value="serif"]::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="serif"]::before {
  content: "衬线字体";
}
.ql-snow .ql-picker.ql-font .ql-picker-label[data-value="monospace"]::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="monospace"]::before {
  content: "等宽字体";
}
</style>
