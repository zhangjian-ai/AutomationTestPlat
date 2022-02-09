<template>
  <div class="mainbox">
    <el-tabs value="first">
      <!-- xmind导入用例 -->
      <el-tab-pane label="xmind导入" name="first">
        <uploadXmind></uploadXmind>
      </el-tab-pane>
      <!-- 手工添加 -->
      <el-tab-pane label="手工创建" name="second">
        <div class="main">
          <div class="header">
            <p>创建测试用例</p>
            <el-divider></el-divider>
          </div>
          <div class="form">
            <el-form
              :model="caseForm"
              size="mini"
              label-width="30%"
              ref="caseForm"
              :rules="caseRules"
            >
              <el-form-item label="用例编号:" prop="no">
                <el-input v-model="caseForm.no"></el-input>
              </el-form-item>
              <el-form-item label="用例名称:" prop="name">
                <el-input v-model="caseForm.name"></el-input>
              </el-form-item>
              <el-form-item label="归属模块:" prop="module">
                <el-cascader
                  v-model="caseForm.module"
                  :options="$store.state.modules"
                  expandTrigger="hover"
                  :props="{ checkStrictly: true, emitPath: false, value: 'id', label: 'name', children: 'subs'}"
                  @change="handleChange"
                  ref="cascader"
                  clearable
                ></el-cascader>
                <el-button icon="el-icon-plus" type="primary" @click="dialogVisible = true"></el-button>
              </el-form-item>
              <el-form-item label="优先级:" prop="priority">
                <el-select v-model="caseForm.priority">
                  <el-option
                    v-for="item in $store.state.priorities"
                    :key="item[0]"
                    :label="item[1]"
                    :value="item[0]"
                  ></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="自动化:" prop="is_auto">
                <el-select v-model="caseForm.is_auto">
                  <el-option label="是" :value="true"></el-option>
                  <el-option label="否" :value="false"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item v-if="caseForm.is_auto" label="自动化脚本路径:" prop="path">
                <el-input v-model="caseForm.path"></el-input>
              </el-form-item>
              <el-form-item v-show="caseForm.is_auto" label="自动化版本:">
                <el-input v-model="caseForm.version"></el-input>
              </el-form-item>
              <el-form-item v-show="caseForm.is_auto" label="自动化类型:">
                <el-input v-model="caseForm.type"></el-input>
              </el-form-item>
              <el-form-item label="用例描述:">
                <el-input
                  type="textarea"
                  :autosize="{ minRows: 1, maxRows: 3 }"
                  v-model="caseForm.description"
                ></el-input>
              </el-form-item>
              <el-form-item label="测试步骤:">
                <el-input
                  type="textarea"
                  v-model="caseForm.step"
                  :autosize="{ minRows: 3, maxRows: 5 }"
                ></el-input>
              </el-form-item>
              <el-form-item label="预期结果:">
                <el-input
                  type="textarea"
                  v-model="caseForm.expectation"
                  :autosize="{ minRows: 1, maxRows: 2 }"
                ></el-input>
              </el-form-item>
            </el-form>
            <div class="footer">
              <el-button size="mini" @click="caseForm = {}">重 置</el-button>
              <el-button size="mini" type="primary" @click="create_submit()">保 存</el-button>
            </div>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
    <!-- 新增模块弹窗 -->
    <el-dialog title="新增模块" :visible.sync="dialogVisible" :close-on-click-modal="false" width="30%">
      <el-form ref="subForm" :model="subForm" label-width="25%" size="mini" :rules="subRules">
        <el-form-item label="父级模块:">
          <el-cascader
            v-model="subForm.parent"
            :options="improve_modules()"
            expandTrigger="hover"
            :props="{ checkStrictly: true, emitPath: false, value: 'id', label: 'name', children: 'subs'}"
            @change="handleChange"
            ref="cascader"
            clearable
          ></el-cascader>
        </el-form-item>
        <el-form-item label="模块名称:" prop="name">
          <el-input v-model="subForm.name"></el-input>
        </el-form-item>
      </el-form>
      <div style="text-align: right; margin-top: 2em; margin-right:1em;">
        <el-button size="mini" @click="dialogVisible = false">取 消</el-button>
        <el-button size="mini" type="primary" @click="create_module()">保 存</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import uploadXmind from "../common/uploadXmind.vue";
import { modules, query_case, create_case, create_module } from "@/api";
export default {
  data() {
    const check_case_no = (rule, value, callback) => {
      if (value) {
        query_case(null, value).then(res => {
          if (res.data.msg == "用例不存在") {
            callback();
          }
          callback(new Error("用例编号已存在"));
        });
      }
      callback();
    };
    return {
      // 用例信息
      caseForm: {},

      // 用例表单校验
      caseRules: {
        no: [
          {
            validator: check_case_no,
            trigger: "blur"
          }
        ],
        name: [
          {
            required: true,
            message: "该项为必填",
            trigger: "blur"
          }
        ],
        module: [
          {
            required: true,
            message: "该项为必填",
            trigger: "blur"
          }
        ],
        priority: [
          {
            required: true,
            message: "该项为必填",
            trigger: "blur"
          }
        ],
        is_auto: [
          {
            required: true,
            message: "该项为必填",
            trigger: "blur"
          }
        ],
        path: [
          {
            required: true,
            message: "该项为必填",
            trigger: "blur"
          }
        ]
      },

      // 弹框变量
      dialogVisible: false,

      // 模块表单
      subForm: {},

      // 模块表单校验
      subRules: {
        name: [
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
    // 创建用例
    create_submit() {
      this.$refs.caseForm.validate(valid => {
        if (valid) {
          create_case(this.caseForm).then(res => {
            this.$message({
              type: "success",
              message: res.data.msg
            });
            // 刷新用例树列表
            this.$store.dispatch("caseTree");
          });
        }
      });
    },

    // 创建模块时保留一级、二级下拉框
    improve_modules() {
      let sub_modules = JSON.parse(JSON.stringify(this.$store.state.modules));
      sub_modules.forEach(val_1 => {
        if (val_1.subs) {
          val_1.subs.forEach(val_2 => {
            val_2.subs = null;
          });
        }
      });
      return sub_modules;
    },

    // 创建模块
    create_module() {
      this.$refs.subForm.validate(valid => {
        if (valid) {
          create_module(this.subForm).then(res => {
            this.$message({
              type: "success",
              message: `模块[${res.data.name}]创建成功`
            });
            this.subForm = {};
            this.dialogVisible = false;
            // 刷新modules
            modules().then(res => {
              this.$store.commit("setModules", res.data);
            });
          });
        }
      });
    },

    // 级联选择器事件,选中节点变化时触发
    handleChange() {
      // 选择选项后,自动关闭下拉框
      this.$refs.cascader.dropDownVisible = false;
    }
  },
  components: {
    uploadXmind
  }
};
</script>
<style scoped>
.mainbox {
  width: 96%;
  margin: 2%;
}
.main {
  width: 30em;
  margin-left: 2%;
}
.main .footer {
  text-align: right;
  margin-top: 2em;
  margin-right: 2em;
}
.footer .el-button {
  margin-left: 2em;
}
.main .header p {
  text-align: left;
  font-size: 1.5em;
  margin: 0.5em 0;
}
.main .form {
  background-color: whitesmoke;
  padding: 1.5em 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}
.el-input {
  width: 65%;
}
.el-select {
  width: 30%;
}
.el-cascader {
  width: 50%;
}
.el-form-item >>> .el-textarea__inner {
  width: 80%;
}
.el-form-item .el-button {
  margin-left: 1em;
  padding: 0.3em;
}
.el-divider {
  margin: 0 0 1em 0;
  padding: 2px 0;
  background-color: tomato;
}
</style>