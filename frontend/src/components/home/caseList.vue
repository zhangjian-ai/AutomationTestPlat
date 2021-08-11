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
                <el-input v-model="conditions.case_id" placeholder="用例编号" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="用例名称:">
                <el-input v-model="conditions.case_name" placeholder="用例名称" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="owner:">
                <el-input v-model="conditions.owner" placeholder="owner" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="优先级:">
                <el-select v-model="conditions.level" placeholder="优先级" clearable>
                  <el-option
                    v-for="item in levels"
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
              <el-form-item label="应用名称:">
                <el-select v-model="conditions.client_id" placeholder="应用名称" clearable>
                  <el-option
                    v-for="item in clients"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                  ></el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="功能模块:">
                <el-select v-model="conditions.module_id" placeholder="功能模块名称" clearable>
                  <el-option
                    v-for="item in modules"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                  ></el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="自动化:">
                <el-select v-model="conditions.is_auto" placeholder="实现自动化" clearable>
                  <el-option label="是" :value="true"></el-option>
                  <el-option label="否" :value="false"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <!-- 用例操作 -->
        <el-row>
          <el-col :span="2" style="text-align: left; padding-left:1.5em;">
            <el-button type="danger" icon="el-icon-plus" size="mini">先占个位</el-button>
          </el-col>
          <el-col :span="22">
            <el-button
              type="primary"
              icon="el-icon-search"
              size="mini"
              @click="getCasesByQuery()"
              native-type="submit"
            >查询</el-button>
            <el-button
              type="warning"
              icon="el-icon-refresh-left"
              size="mini"
              @click="conditions = {}"
            >重置</el-button>
          </el-col>
        </el-row>
      </div>
    </div>
    <!-- 信息展示区 -->
    <el-table
      :data="caseList"
      stripe
      v-loading="loading"
      border
      height="48em"
      size="mini"
      :header-cell-style="{background:'#eef1f6',color:'#606266', 'text-align': 'center'}"
    >
      <el-table-column type="selection" align="center"></el-table-column>
      <el-table-column label="序号" type="index" width="50" align="center"></el-table-column>
      <el-table-column prop="case_id" label="用例编号" width="200"></el-table-column>
      <el-table-column
        prop="case_name"
        label="用例名称"
        width="220"
        align="center"
        show-overflow-tooltip
      ></el-table-column>
      <el-table-column prop="client" label="应用" width="100" align="center"></el-table-column>
      <el-table-column prop="module" label="功能模块" width="120" align="center"></el-table-column>
      <el-table-column prop="level_value" label="优先级" width="60" align="center"></el-table-column>
      <el-table-column label="自动化" width="60" align="center">
        <template slot-scope="scope">
          <el-image v-if="scope.row.is_auto" :src="currect_url" style="width: 1.2em; height: 1.2em;"></el-image>
          <el-image v-else :src="error_url" style="width: 1.2em; height: 1.2em;"></el-image>
        </template>
      </el-table-column>
      <el-table-column prop="owner" label="OWNER" width="100" align="center"></el-table-column>
      <el-table-column prop="add_time" label="用例编写时间" width="150" align="center"></el-table-column>
      <el-table-column label="操作" align="center" width="125">
        <template slot-scope="scope">
          <el-button icon="el-icon-edit" circle size="mini" @click="openDrawer(scope.row)"></el-button>
          <el-button
            icon="el-icon-delete"
            style="color: red;"
            circle
            size="mini"
            @click="deleteCase(scope.row)"
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
            <el-input v-model="caseForm.case_id" disabled></el-input>
          </el-form-item>
          <el-form-item label="用例名称:" prop="case_name">
            <el-input v-model="caseForm.case_name"></el-input>
          </el-form-item>
          <el-form-item label="应用名称:" prop="client_id">
            <el-select v-model="caseForm.client_id">
              <el-option v-for="item in clients" :key="item.id" :label="item.name" :value="item.id"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="功能模块:" prop="module_id">
            <el-select v-model="caseForm.module_id">
              <el-option v-for="item in modules" :key="item.id" :label="item.name" :value="item.id"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="用例描述:">
            <el-input
              type="textarea"
              :autosize="{ minRows: 1, maxRows: 3 }"
              v-model="caseForm.description"
              style="width: 25em;"
            ></el-input>
          </el-form-item>
          <el-form-item label="测试步骤:">
            <el-input
              type="textarea"
              v-model="caseForm.step"
              :autosize="{ minRows: 2, maxRows: 5 }"
              style="width: 25em;"
            ></el-input>
          </el-form-item>
          <el-form-item label="优先级:" prop="level">
            <el-select v-model="caseForm.level">
              <el-option v-for="item in levels" :key="item[0]" :label="item[1]" :value="item[0]"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="owner:" prop="owner">
            <el-input v-model="caseForm.owner" style="width: 8em;" disabled></el-input>
          </el-form-item>
          <el-form-item label="更新人:">
            <el-input v-model="caseForm.updater" style="width: 8em;"></el-input>
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
          <el-form-item label="创建时间:">
            <el-input v-model="caseForm.add_time" disabled></el-input>
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
import {
  clients,
  modules,
  case_list,
  get_image,
  modify_case,
  delete_case,
  get_constants
} from "@/api";
export default {
  data() {
    return {
      // 用例列表
      caseList: [],

      //   查询条件
      conditions: {},

      //  应用和模块列表
      clients: [],
      modules: [],

      // 用例等级
      levels: [],

      //  加载中
      loading: false,

      //   分页
      count: 0,
      page: 1,
      page_size: 15,

      //  图标
      currect_url: "",
      error_url: "",

      // 用例抽屉的变量
      showDrawer: false,

      // 用例信息
      caseForm: {},

      // 表单校验规则
      rules: {
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
        owner: [
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

    // 通过查询按钮查询用例
    getCasesByQuery() {
      // 重置当前页
      this.page = 1;
      // 调用查询方法
      this.getCases();
    },

    // 打开用例抽屉。查看或者修改
    openDrawer(form) {
      this.showDrawer = true;
      // 深拷贝表单数据
      this.caseForm = JSON.parse(JSON.stringify(form));
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
            modify_case(this.caseForm).then(res => {
              this.$message({
                type: "success",
                message: res.data.msg
              });
            });
          });
        }
      });
    },

    // 删除用例
    deleteCase(form) {
      this.$confirm("您即将删除本用例, 确认是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        delete_case(form.id, form.case_id).then(res => {
          this.$message({
            type: "success",
            message: res.data.msg
          });
        });
        // 刷新列表
        this.getCases();
      });
    },

    // 加载Image
    loadImage() {
      get_image("正确图标").then(res => {
        this.currect_url = res.data.image;
      });
      get_image("错误图标").then(res => {
        this.error_url = res.data.image;
      });
    },

    // 加载搜索栏下拉框、用例等级信息
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
    }
  },
  created() {
    this.loadImage();
    this.loadOption();
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
  width: 96%;
  text-align: right;
}
.condition /deep/ .el-form-item__label {
  font-size: 0.9em !important;
}
.condition .el-input {
  width: 14em;
}
.condition .el-select {
  width: 12em;
}
.el-table {
  width: 100%;
  overflow: auto;
  margin: 1em 0;
}
.el-drawer .form {
  width: 96%;
  font-size: 1.2em;
  text-align: left;
  padding: 2%;
}
.el-drawer .el-input {
  width: 20em;
}
.el-drawer .el-select {
  width: 12em;
}
</style>