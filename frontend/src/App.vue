<template>
  <div id="app" @click="clickHandler">
    <router-view v-wechat-title="$route.meta.title" />
  </div>
</template>
<script>
/* eslint-disable */

export default {
  // 全局解决element UI button 点击后不失焦的问题
  // 但是部分组件里面的按钮由于没有冒泡，所以仍无法解决
  methods: {
    clickHandler(ev) {
      if ((ev.target.nodeName == "SPAN") | (ev.target.nodeName == "I")) {
        ev.target.parentNode.blur();
      }
      if (ev.target.nodeName == "BUTTON") {
        ev.target.blur();
      }
    }
  }
};
</script>
<style>
body,
html,
#app {
  margin: 0px;
  padding: 0px;
  height: 100%;
  width: 100%;
}

/* 全局修改消息弹框样式 */
.el-message {
  top: 30px !important;
  min-width: 5em !important;
  padding: 0.5em !important;
  border-radius: 0 !important;
}
.el-message .el-message__content {
  font-size: 1em;
}

/* 全局修改级联选择器样式 */
.el-cascader-panel .el-radio {
  width: 100%;
  height: 100%;
  z-index: 10;
  position: absolute;
  top: 10px;
  right: 10px;
}
.el-cascader-panel .el-radio__input {
  visibility: hidden;
}
.el-cascader-panel .el-cascader-node__postfix {
  top: 10px;
}

/* 全局设置下拉框最大高度 */
.el-select-dropdown__list {
  max-height: 15em;
  overflow: auto;
}
</style>
