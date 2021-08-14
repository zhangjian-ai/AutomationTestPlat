<template>
  <div class="mainbox">
    <el-tabs value="first">
      <!-- xmind导入用例 -->
      <el-tab-pane label="xmind导入" name="first">
        <upload></upload>
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
              label-width="10em"
              ref="caseForm"
              :rules="caseRules"
            >
              <el-form-item label="用例编号:" prop="case_id">
                <el-input v-model="caseForm.case_id"></el-input>
              </el-form-item>
              <el-form-item label="用例名称:" prop="case_name">
                <el-input v-model="caseForm.case_name"></el-input>
              </el-form-item>
              <el-form-item label="应用名称:" prop="client_id">
                <el-select v-model="caseForm.client_id">
                  <el-option
                    v-for="item in clients"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                  ></el-option>
                </el-select>
                <el-button
                  style="margin-left: 2em;"
                  icon="el-icon-plus"
                  type="primary"
                  plain
                  @click="openDialog('应用')"
                ></el-button>
              </el-form-item>
              <el-form-item label="功能模块:" prop="module_id">
                <el-select v-model="caseForm.module_id">
                  <el-option
                    v-for="item in modules"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                  ></el-option>
                </el-select>
                <el-button
                  style="margin-left: 2em;"
                  icon="el-icon-plus"
                  type="primary"
                  plain
                  @click="openDialog('模块')"
                ></el-button>
              </el-form-item>
              <el-form-item label="用例描述:">
                <el-input
                  type="textarea"
                  :autosize="{ minRows: 2, maxRows: 4 }"
                  v-model="caseForm.description"
                  style="width: 30em;"
                ></el-input>
              </el-form-item>
              <el-form-item label="测试步骤:">
                <el-input
                  type="textarea"
                  v-model="caseForm.step"
                  :autosize="{ minRows: 3, maxRows: 5 }"
                  style="width: 30em;"
                ></el-input>
              </el-form-item>
              <el-form-item label="优先级:" prop="level">
                <el-select v-model="caseForm.level">
                  <el-option
                    v-for="item in levels"
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
              <el-form-item v-if="caseForm.is_auto" label="自动化脚本路径:" prop="exec_path">
                <el-input v-model="caseForm.exec_path" style="width: 30em;"></el-input>
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
    <!-- 新增应用/模块弹窗 -->
    <el-dialog
      :title="'添加' + title"
      :visible.sync="dialogVisible"
      :close-on-click-modal="false"
      width="30%"
    >
      <el-form :rules="subRules" ref="subForm" :model="subForm" label-width="6em" size="mini">
        <el-form-item :label="title + '名称:'" prop="name">
          <el-input v-model="subForm.name"></el-input>
        </el-form-item>
        <el-form-item v-if="title == '模块'" label="所属应用:" prop="client">
          <el-select v-model="subForm.client">
            <el-option v-for="item in clients" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div style="text-align: right; margin-top: 2em; margin-right:1em;">
        <el-button size="mini" @click="dialogVisible = false">取 消</el-button>
        <el-button size="mini" type="primary" @click="create_client_module()">保 存</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import upload from "../common/upload.vue";
import {
  clients,
  modules,
  check_case,
  create_case,
  create_client,
  create_module,
  get_constants
} from "@/api";
export default {
  data() {
    const check_case_id = (rule, value, callback) => {
      check_case(value).then(res => {
        if (res.data.msg == "用例不存在") {
          callback();
        }
        callback(new Error("用例编号已存在"));
      });
    };
    return {
      // 用例信息
      caseForm: {},

      //  应用和模块列表
      clients: [],
      modules: [],

      // 用例优先级
      levels: [],

      // 用例表单校验规则
      caseRules: {
        case_id: [
          {
            required: true,
            message: "该项为必填",
            trigger: "blur"
          },
          { validator: check_case_id, trigger: "submit" }
        ],
        case_name: [
          {
            required: true,
            message: "该项为必填",
            trigger: "blur"
          }
        ],
        client_id: [
          {
            required: true,
            message: "该项为必填",
            trigger: "blur"
          }
        ],
        module_id: [
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
        is_auto: [
          {
            required: true,
            message: "该项为必填",
            trigger: "blur"
          }
        ],
        exec_path: [
          {
            required: true,
            message: "该项为必填",
            trigger: "blur"
          }
        ]
      },

      // 弹框变量
      title: "",
      dialogVisible: false,

      // 应用或模块表单
      subForm: {},

      // 应用表单校验
      subRules: {
        name: [
          {
            required: true,
            message: "该项为必填",
            trigger: "blur"
          }
        ],
        client: [
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
    // 加载搜索栏下拉框
    loadOption() {
      clients().then(res => {
        this.clients = res.data;
      });
      modules().then(res => {
        this.modules = res.data;
      });
      get_constants("CASE").then(res => {
        this.levels = res.data.LEVEL;
      });
    },

    // 创建用例
    create_submit() {
      this.$refs.caseForm.validate(valid => {
        if (valid) {
          create_case(this.caseForm).then(res => {
            this.$message({
              type: "success",
              message: res.data.msg
            });
          });
        }
      });
    },

    // 打开对话框
    openDialog(title) {
      this.title = title;
      this.dialogVisible = true;
    },

    // 创建应用或者模块
    create_client_module() {
      this.$refs.subForm.validate(valid => {
        if (valid) {
          if (this.subForm.client_id) {
            create_module(this.subForm).then(res => {
              this.$message({
                type: "success",
                message: `模块[${res.data.name}]创建成功`
              });
              this.subForm = {};
              this.dialogVisible = false;
              // 刷新modules
              modules().then(res => {
                this.modules = res.data;
              });
            });
          } else {
            create_client(this.subForm).then(res => {
              this.$message({
                type: "success",
                message: `应用[${res.data.name}]创建成功`
              });
              this.subForm = {};
              this.dialogVisible = false;
              // 刷新clients
              clients().then(res => {
                this.clients = res.data;
              });
            });
          }
        }
      });
    }
  },
  components: {
    upload
  },
  mounted() {
    this.loadOption();
  }
};
</script>
<style scoped>
.mainbox {
  width: 96%;
  margin: 2%;
}
.main {
  width: 45%;
  margin-left: 2%;
}
.main .footer {
  text-align: right;
  margin-top: 2em;
  margin-right: 2em;
}
.footer .el-button {
  margin-left: 3em;
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
  width: 20em;
}
.el-select {
  width: 10em;
}
.el-divider {
  margin: 0 0 1em 0;
  padding: 2px 0;
  background-color: tomato;
}
</style>