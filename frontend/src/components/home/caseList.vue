<template>
  <div>
    <div class="header">
      <!-- 搜索栏 -->
      <div class="condition">
        <el-form
          :inline="true"
          :model="conditions"
          size="mini"
          @keyup.enter.native="getCasesByQuery()"
        >
          <el-row>
            <el-col :span="6">
              <el-form-item label="用例编号:">
                <el-input v-model="conditions.no" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="用例名称:">
                <el-input v-model="conditions.name" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="AUTHOR:">
                <el-input v-model="conditions.author" clearable placeholder="用户昵称"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="优先级:">
                <el-select v-model="conditions.priority" clearable>
                  <el-option
                    v-for="item in $store.state.priorities"
                    :key="item[0]"
                    :label="item[1]"
                    :value="item[0]"
                  ></el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="6">
              <el-form-item label="功能模块:">
                <el-cascader
                  v-model="conditions.module"
                  :options="$store.state.modules"
                  expandTrigger="hover"
                  :props="{ checkStrictly: true, emitPath: false, value: 'id', label: 'name', children: 'subs'}"
                  @change="handleChange"
                  ref="cascader"
                  clearable
                ></el-cascader>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="自动化:">
                <el-select v-model="conditions.is_auto" clearable>
                  <el-option label="是" :value="true"></el-option>
                  <el-option label="否" :value="false"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="创建时间:">
                <el-date-picker
                  v-model="conditions.code_time"
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
          <el-col :span="23" style="text-align: right;">
            <el-button
              type="primary"
              icon="el-icon-search"
              size="mini"
              @click="getCasesByQuery()"
              native-type="submit"
            >查询</el-button>
            <el-button type icon="el-icon-refresh-left" size="mini" @click="conditions = {}">重置</el-button>
          </el-col>
        </el-row>
      </div>
    </div>
    <!-- 用例列表展示 -->
    <el-table
      :data="caseList"
      v-loading="loading"
      max-height="54.3em"
      size="mini"
      :header-cell-style="{background:'#eef1f6',color:'#606266', 'text-align': 'center'}"
    >
      <el-table-column type="selection" align="center"></el-table-column>
      <el-table-column label="序号" type="index" min-width="50%" align="center"></el-table-column>
      <el-table-column prop="no" label="用例编号" min-width="200%" align="center"></el-table-column>
      <el-table-column prop="name" label="用例名称" min-width="250%" align="center"></el-table-column>
      <el-table-column label="功能模块" min-width="200%">
        <template
          slot-scope="scope"
        >{{ (scope.row.module_str1 ? scope.row.module_str1 + " / " : "") + (scope.row.module_str2 ? scope.row.module_str2 + " / " : "") + (scope.row.module_str3 ? scope.row.module_str3 : "") }}</template>
      </el-table-column>
      <el-table-column prop="priority_str" label="优先级" min-width="60%" align="center"></el-table-column>
      <el-table-column label="自动化" min-width="60%" align="center">
        <template slot-scope="scope">
          <el-image v-if="scope.row.is_auto" :src="$store.state.correct"></el-image>
          <el-image v-else :src="$store.state.error"></el-image>
        </template>
      </el-table-column>
      <el-table-column prop="author" label="AUTHOR" min-width="100%" align="center"></el-table-column>
      <el-table-column prop="code_time" label="用例编写时间" min-width="150%" align="center"></el-table-column>
      <el-table-column label="操作" align="center" min-width="90%">
        <template slot-scope="scope">
          <el-button icon="el-icon-edit" circle size="mini" @click="openDrawer(scope.row.id)"></el-button>
          <el-button
            icon="el-icon-delete"
            style="color: red;"
            circle
            size="mini"
            @click="deleteCase(scope.row.id)"
          ></el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 分页 -->
    <el-row style="text-align: right;">
      <pagination :count="count" :page.sync="page" :page_size.sync="page_size" @function="getCases"></pagination>
    </el-row>
    <!-- 用例详情抽屉 -->
    <el-drawer :visible.sync="showDrawer" size="40%" :wrapperClosable="false" direction="rtl">
      <div slot="title" style="font-size: 1.2em; color: black;">用例详情</div>
      <div class="form">
        <el-form :model="caseForm" size="mini" label-width="10em" ref="caseForm" :rules="rules">
          <el-form-item label="ID:">
            <el-input v-model="caseForm.id" disabled style="width: 6em;"></el-input>
          </el-form-item>
          <el-form-item label="用例编号:">
            <el-input v-model="caseForm.no" disabled></el-input>
          </el-form-item>
          <el-form-item label="用例名称:" prop="name">
            <el-input v-model="caseForm.name"></el-input>
          </el-form-item>
          <el-form-item label="AUTHOR:" prop="author">
            <el-input v-model="caseForm.author" disabled></el-input>
          </el-form-item>
          <el-form-item label="功能模块:" prop="module">
            <el-cascader
              v-model="caseForm.module"
              :options="$store.state.modules"
              expandTrigger="hover"
              :props="{ checkStrictly: true, emitPath: false, value: 'id', label: 'name', children: 'subs'}"
              @change="handleChange"
              ref="cascader"
              clearable
              style="width: 20em;"
            ></el-cascader>
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
              :autosize="{ minRows: 1, maxRows: 2 }"
              v-model="caseForm.description"
            ></el-input>
          </el-form-item>
          <el-form-item label="测试步骤:">
            <el-input
              type="textarea"
              v-model="caseForm.step"
              :autosize="{ minRows: 2, maxRows: 5 }"
            ></el-input>
          </el-form-item>
          <el-form-item label="预期结果:">
            <el-input
              type="textarea"
              v-model="caseForm.expectation"
              :autosize="{ minRows: 1, maxRows: 2 }"
            ></el-input>
          </el-form-item>
          <el-form-item label="创建时间:">
            <el-input v-model="caseForm.code_time" disabled></el-input>
          </el-form-item>
          <el-form-item v-show="caseForm.reviser" label="最近修改时间:">
            <el-input v-model="caseForm.update_time" disabled></el-input>
          </el-form-item>
          <el-form-item v-show="caseForm.reviser" label="修改人:">
            <el-input v-model="caseForm.reviser_str" disabled></el-input>
          </el-form-item>
        </el-form>
        <div style="text-align: right; margin-right: 2em; margin-top: 2em;">
          <el-button size="mini" @click="showDrawer = false">取 消</el-button>
          <el-button size="mini" type="primary" @click="modify_submit()">保 存</el-button>
        </div>
      </div>
    </el-drawer>
  </div>
</template>
<script>
import pagination from "../common/pagination.vue";
import { case_list, query_case, modify_case, delete_case } from "@/api";
export default {
  data() {
    return {
      // 用例列表
      caseList: [],

      //   查询条件
      conditions: {},

      //  加载中
      loading: false,

      //   分页
      count: 0,
      page: 1,
      page_size: 15,

      // 用例抽屉的变量
      showDrawer: false,

      // 用例信息
      resData: {},
      caseForm: {},

      // 表单校验规则
      rules: {
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
      }
    };
  },
  methods: {
    // 获取用例列表
    getCases() {
      this.loading = true;

      case_list(this.page, this.page_size, this.conditions).then(res => {
        this.caseList = res.data.results;
        this.count = res.data.count;

        this.loading = false;
      });
    },

    // 通过查询按钮查询用例列表
    getCasesByQuery() {
      // 重置当前页
      this.page = 1;
      // 调用查询方法
      this.getCases();
    },

    // 打开用例抽屉。查看或者修改
    openDrawer(id) {
      this.showDrawer = true;
      // 重置表单
      this.caseForm = {};
      // 获取用例详情
      query_case(id).then(res => {
        // Object.assign(res.data.base, res.data.detail);
        // 深拷贝表单数据
        this.caseForm = JSON.parse(JSON.stringify(res.data));
        this.resData = JSON.parse(JSON.stringify(res.data));
      });
    },

    // 用例修改保存
    modify_submit() {
      this.$refs.caseForm.validate(valid => {
        if (valid) {
          this.$confirm("您正在修改当前用例, 确认是否继续?", "提示", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning"
          }).then(() => {
            // 筛选出修改的项
            let form = {};
            for (let key in this.caseForm) {
              if (this.caseForm[key] != this.resData[key]) {
                form[key] = this.caseForm[key];
              }
            }
            if (JSON.stringify(form) == "{}") {
              this.$message({
                type: "info",
                message: "未作修改 何必保存"
              });
            } else {
              // 发起修改
              form.id = this.caseForm.id;
              modify_case(form).then(res => {
                this.$message({
                  type: "success",
                  message: res.data.msg
                });
                // 刷新用例列表并关闭抽屉
                this.getCases();
                this.showDrawer = false;
              });
            }
          });
        }
      });
    },

    // 删除用例
    deleteCase(id) {
      this.$confirm("您即将删除本用例, 确认是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        delete_case(id).then(res => {
          this.$message({
            type: "success",
            message: res.data.msg
          });
          // 刷新列表
          this.getCases();
        });
      });
    },

    // 级联选择器事件,选中节点变化时触发
    handleChange() {
      // 选择选项后,自动关闭下拉框
      this.$refs.cascader.dropDownVisible = false;
    }
  },
  created() {
    this.getCases();
  },
  components: {
    pagination
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
.condition .el-select,
.condition .el-cascader {
  width: 120%;
}

.el-date-editor--datetimerange.el-input__inner {
  width: 14.8em;
}

.el-table {
  width: 100%;
  overflow: auto;
  margin: 1em 0;
}
.el-table .el-image {
  height: 1.2em;
}
.el-drawer .form {
  width: 96%;
  padding: 2%;
}
.el-drawer .el-input {
  width: 65%;
}
.el-drawer .el-form-item >>> .el-textarea__inner {
  width: 80%;
}
.el-drawer .el-select {
  width: 25%;
}
</style>