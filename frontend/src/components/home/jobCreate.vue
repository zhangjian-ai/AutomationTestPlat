<template>
  <div class="main">
    <!-- 创建任务表单 -->
    <el-col :span="10">
      <div class="text_zone">
        <div class="title">
          <p>创建测试任务</p>
          <el-divider></el-divider>
        </div>
        <div class="form">
          <span class="tips">&nbsp;创建任务提交之前请先勾选任务所需之用例</span>
          <el-form :model="jobForm" label-width="25%" ref="jobForm" :rules="rules" size="mini">
            <el-form-item label="任务名称:" prop="task_name">
              <el-input v-model="jobForm.task_name"></el-input>
            </el-form-item>
            <el-form-item label="任务详情:">
              <el-input
                type="textarea"
                :autosize="{ minRows: 3, maxRows: 5 }"
                v-model="jobForm.task_detail"
              ></el-input>
            </el-form-item>
            <el-form-item label="优先级:" prop="level">
              <el-select v-model="jobForm.level">
                <el-option
                  v-for="item in $store.state.levels"
                  :key="item[0]"
                  :label="item[1]"
                  :value="item[0]"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="任务类型:" prop="type">
              <el-select v-model="jobForm.type">
                <el-option
                  v-for="item in $store.state.categories"
                  :key="item[0]"
                  :label="item[1]"
                  :value="item[0]"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="责任人:">
              <el-select v-model="jobForm.executor" filterable clearable>
                <el-option
                  v-for="item in $store.state.users"
                  :key="item.id"
                  :label="item.nickname"
                  :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="关联需求:">
              <el-input v-model="jobForm.prd_no"></el-input>
            </el-form-item>
            <el-form-item label="计划完成时间:" prop="expect_end_time">
              <el-date-picker
                v-model="jobForm.expect_end_time"
                type="datetime"
                placeholder="选择日期时间"
                value-format="yyyy-MM-dd HH:mm:ss"
                width="50%"
              ></el-date-picker>
            </el-form-item>
          </el-form>
          <div class="footer">
            <el-button size="mini" @click="jobForm = {}">重 置</el-button>
            <el-button size="mini" type="primary" @click="create_submit()">保 存</el-button>
          </div>
        </div>
      </div>
    </el-col>
    <el-col :span="2">
      <pre style="margin:0; padding: 0;">&nbsp;</pre>
    </el-col>
    <!-- 用例列表 -->
    <el-col :span="7">
      <div class="caselist">
        <el-input placeholder="关键字过滤" v-model="filterText" size="mini"></el-input>
        <el-tree
          :data="$store.state.case_tree"
          show-checkbox
          node-key="id"
          :render-after-expand="false"
          @check-change="handleChange"
          :props="defaultProps"
          :filter-node-method="filterNode"
          ref="tree"
        ></el-tree>
        <div>
          <p>
            <span>
              ☑️ 您已勾选&nbsp;
              <span style="color: red;">{{ num }}</span>&nbsp;条用例
            </span>
            <el-button
              style="margin-left: 5em;"
              size="mini"
              type="primary"
              plain
              @click="clearCaseList()"
            >清除选中</el-button>
          </p>
        </div>
      </div>
    </el-col>
  </div>
</template>
<script>
import { create_job } from "@/api";
export default {
  data() {
    return {
      // 列表树过滤
      filterText: "",

      // 列表树
      defaultProps: {
        children: "subs",
        label: "name",
        disabled: "disabled"
      },

      // 创建任务表单、用例数组
      jobForm: {},
      case: [],

      // 表单校验规则
      rules: {
        task_name: [
          {
            required: true,
            message: "该项为必填",
            trigger: "blur"
          }
        ],
        level: [
          {
            required: true,
            message: "该项为必填",
            trigger: "blur"
          }
        ],
        type: [
          {
            required: true,
            message: "该项为必填",
            trigger: "blur"
          }
        ],
        expect_end_time: [
          {
            required: true,
            message: "该项为必填",
            trigger: "blur"
          }
        ]
      }
    };
  },
  methods: {
    // 过滤节点。绑定的属性方法
    // value是调用组件filter方法是传入的值，data是节点数据对象。下面的name即是defaultProps中定义的值
    filterNode(value, data) {
      if (!value) return true;
      return data.name.indexOf(value) !== -1;
    },

    // 节点选中状态变化的绑定事件。这里用不上第三个参数，所以没有入参
    handleChange(data, self) {
      if (data.cate == "case") {
        if (self) {
          this.case.push(data.id);
        } else {
          for (let i = 0; i < this.case.length; i++) {
            if (this.case[i] == data.id) {
              this.case.splice(i, 1);
            }
          }
        }
      }
    },

    // 清空已勾选的用例
    clearCaseList() {
      this.$refs.tree.setCheckedNodes(this.case);
    },

    // 创建提交
    create_submit() {
      this.$refs.jobForm.validate(valid => {
        if (valid) {
          if (this.case.length == 0) {
            this.$message({
              type: "error",
              message: "请勾选测试用例"
            });
            return;
          }
          this.jobForm.case = this.case;
          create_job(this.jobForm).then(res => {
            this.$message({
              type: "success",
              message: res.data.msg
            });
            // 刷新任务统计
            this.$store.dispatch("jobInductions");
          });
        }
      });
    }
  },
  watch: {
    // 过滤节点
    filterText(val) {
      // 防抖
      let timer = null;
      let func = this.$refs.tree.filter;
      (() => {
        if (timer !== null) {
          clearTimeout(timer);
        }
        timer = setTimeout(() => {
          // filter 接收一个任意类型的参数，该参数会在 filter-node-method 中作为第一个参数
          func(val);
        }, 500);
      })();
    }
  },
  computed: {
    // 选择用例数
    num() {
      if (this.case) {
        return this.case.length;
      }
      return 0;
    }
  }
};
</script>
<style scoped>
.main {
  margin: 2em 3em;
}
.caselist p {
  text-align: left;
  padding-left: 1em;
  color: grey;
}
/* 列表部分样式 */
.caselist {
  background-color: rgb(214, 212, 212);
  height: 39em;
  width: 22em;
  margin-top: 3.5em;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}
.el-tree {
  margin: 0.2em 0 0 0;
  height: 33em;
  color: black;
  border: 1px solid skyblue;
  overflow: auto;
}
.el-tree /deep/ .el-tree-node__content:hover {
  background-color: #488fa3;
}
.el-tree /deep/ .el-tree-node:focus > .el-tree-node__content {
  background-color: #488fa3;
}
.caselist /deep/ input.el-input__inner {
  border-radius: 0;
  border: 2px solid black;
}
.caselist /deep/ .el-checkbox__input.is-disabled .el-checkbox__inner {
  background-color: #aaaaaa;
}

/* 表单部分样式 */
.text_zone {
  width: 30em;
}
.title {
  width: 100%;
  text-align: left;
}
.title p {
  font-size: 1.5em;
  margin: 0.2em 0;
}
.title .el-divider {
  margin: 1em 0 2em 0;
  background-color: tomato;
  padding: 2px 0;
}
.form {
  background-color: whitesmoke;
  padding: 1em 0 2em 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}
.form .tips {
  font-size: 0.8em;
  color: tomato;
  margin-left: 2em;
}
.form .footer {
  text-align: right;
  margin-top: 2em;
  margin-right: 2em;
}
.form .footer .el-button {
  margin-left: 3em;
}
.el-form-item {
  margin: 2em 0;
}
.el-form-item >>> .el-textarea__inner {
  width: 80%;
}
.form .el-input {
  width: 80%;
}
.form .el-select {
  width: 30%;
}
</style>