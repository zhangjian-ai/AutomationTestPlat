<template>
  <div>
    <div class="header">
      <!-- 搜索栏 -->
      <div class="condition">
        <el-form
          :inline="true"
          :model="conditions"
          size="mini"
          @keyup.enter.native="getJobsByQuery()"
        >
          <el-row>
            <el-col :span="6">
              <el-form-item label="任务编号:">
                <el-input v-model="conditions.task_no" placeholder="任务编号" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="任务名称:">
                <el-input v-model="conditions.task_name" placeholder="任务名称" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="任务状态:">
                <el-select v-model="conditions.status" placeholder="任务状态" clearable>
                  <el-option
                    v-for="item in $store.state.status"
                    :key="item[0]"
                    :label="item[1]"
                    :value="item[0]"
                  ></el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="优先级:">
                <el-select v-model="conditions.level" placeholder="优先级" clearable>
                  <el-option
                    v-for="item in $store.state.levels"
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
              <el-form-item label="任务类型:">
                <el-select v-model="conditions.type" placeholder="任务类型" clearable>
                  <el-option
                    v-for="item in $store.state.categories"
                    :key="item.id"
                    :label="item[1]"
                    :value="item[0]"
                  ></el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="创建人:">
                <el-select v-model="conditions.create_user" placeholder="创建人" clearable filterable>
                  <el-option
                    v-for="item in $store.state.users"
                    :key="item.id"
                    :label="item.nickname"
                    :value="item.id"
                  ></el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="责任人:">
                <el-select v-model="conditions.executor" placeholder="责任人" clearable filterable>
                  <el-option
                    v-for="item in $store.state.users"
                    :key="item.id"
                    :label="item.nickname"
                    :value="item.id"
                  ></el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="延期:">
                <el-select v-model="conditions.is_delay" placeholder="是否延期" clearable>
                  <el-option label="是" :value="true"></el-option>
                  <el-option label="否" :value="false"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <!-- 全局操作 -->
        <el-row>
          <el-col :span="2" style="text-align: left; padding-left: 1.5em;">
            <el-button
              type="primary"
              icon="el-icon-document"
              size="mini"
              @click="openDialog(selectedRows)"
            >批量指派</el-button>
          </el-col>
          <el-col :span="22">
            <el-button type="primary" icon="el-icon-search" size="mini" @click="getJobsByQuery()">查询</el-button>
            <el-button icon="el-icon-refresh-left" size="mini" @click="conditions = {}">重置</el-button>
          </el-col>
        </el-row>
      </div>
    </div>
    <!-- 信息展示区 -->
    <el-table
      :data="jobList"
      v-loading="loading"
      size="mini"
      border
      @selection-change="handleSelectionChange"
      :header-cell-style="{background:'#eef1f6',color:'#606266', 'text-align': 'center'}"
    >
      <el-table-column type="selection" align="center"></el-table-column>
      <el-table-column label="序号" type="index" min-width="50%" align="center"></el-table-column>
      <el-table-column prop="task_no" label="任务编号" min-width="150%"></el-table-column>
      <el-table-column prop="task_name" label="任务名称" min-width="200%" align="center"></el-table-column>
      <el-table-column prop="status_str" label="状态" min-width="100%" align="center"></el-table-column>
      <el-table-column prop="level_str" label="优先级" min-width="120%" align="center"></el-table-column>
      <el-table-column prop="type_str" label="任务类型" min-width="100%" align="center"></el-table-column>
      <el-table-column prop="executor_name" label="责任人" min-width="80%" align="center"></el-table-column>
      <el-table-column prop="expect_end_time" label="计划完成时间" min-width="150%" align="center"></el-table-column>
      <el-table-column prop="actual_end_time" label="实际完成时间" min-width="150%" align="center"></el-table-column>
      <el-table-column prop="create_time" label="创建时间" min-width="150%" align="center"></el-table-column>
      <el-table-column label="延期" min-width="60%" align="center">
        <template slot-scope="scope">{{ scope.row.is_delay ? '是' : '否' }}</template>
      </el-table-column>
      <el-table-column prop="create_user_name" label="创建人" min-width="80%" align="center"></el-table-column>
      <el-table-column prop="prd_no" label="关联需求号" min-width="120%" align="center"></el-table-column>
      <el-table-column label="操作" align="center" min-width="100%">
        <template slot-scope="scope">
          <el-link v-show="scope.row.status < 3" :underline="false">用例</el-link>
          <el-link
            v-show="scope.row.executor_name == null"
            :underline="false"
            @click="openDialog([scope.row])"
          >指派</el-link>
        </template>
      </el-table-column>
    </el-table>
    <!-- 分页 -->
    <el-row style="text-align: right;">
      <pagination :count="count" :page.sync="page" :page_size.sync="page_size" @function="getJobs"></pagination>
    </el-row>
    <!-- 指派任务弹窗 -->
    <el-dialog
      title="指派测试任务"
      :visible.sync="dialogVisible"
      :close-on-click-modal="false"
      width="25%"
    >
      <el-form
        :rules="dispatchRules"
        ref="dispatchForm"
        :model="dispatchForm"
        label-width="6em"
        size="mini"
      >
        <el-form-item label="指派给:" prop="user_id">
          <el-select v-model="dispatchForm.user_id" filterable>
            <el-option
              v-for="item in $store.state.users"
              :key="item.id"
              :label="item.nickname"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div style="text-align: right; margin-top: 2em; margin-right:1em;">
        <el-button size="mini" @click="dialogVisible = false">取 消</el-button>
        <el-button size="mini" type="primary" @click="dispatchJob()">确 认</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import pagination from "../common/pagination.vue";
import { job_list, dispatch_job } from "@/api";
export default {
  data() {
    return {
      // 测试任务列表
      jobList: [],

      // 查询条件
      conditions: {},

      //  加载中
      loading: false,

      // 分页
      count: 0,
      page: 1,
      page_size: 15,

      // dialog指派任务
      dialogVisible: false,
      dispatchForm: {},
      dispatchRules: {
        user_id: [
          {
            required: true,
            message: "请选择指派人",
            trigger: "blur"
          }
        ]
      },

      // 批量勾选行
      selectedRows: [],

      // 勾选任务的id列表
      job_ids: []
    };
  },
  methods: {
    // 获取用例列表
    getJobs() {
      this.loading = true;

      job_list(this.page, this.page_size, this.conditions).then(res => {
        this.jobList = res.data.results;
        this.count = res.data.count;

        this.loading = false;
      });
    },

    // 通过查询按钮查询用例
    getJobsByQuery() {
      // 重置当前页
      this.page = 1;
      // 调用查询方法
      this.getJobs();
    },

    // 批量勾选行
    handleSelectionChange(rows) {
      this.selectedRows = rows;
    },

    // 打开指派任务弹框
    openDialog(rows) {
      // 清空ids
      this.job_ids = [];
      // 校验长度
      if (rows.length == 0) {
        this.$message({
          type: "warning",
          message: "未勾选测试任务"
        });
        return;
      }
      // 校验是否被指派
      for (let i in rows) {
        // 校验是否已指派
        if (rows[i].executor_name | rows[i].executor) {
          this.$message({
            type: "warning",
            message: "已指派任务不能再次指派"
          });
          return;
        } else {
          this.job_ids.push(rows[i].id);
        }
      }
      // 打开弹窗
      this.dialogVisible = true;
    },

    // 指派任务
    dispatchJob() {
      this.$refs.dispatchForm.validate(valid => {
        if (valid) {
          // 拼装请求data
          this.dispatchForm.job_ids = this.job_ids;
          // 发起请求
          dispatch_job(this.dispatchForm).then(res => {
            this.$message({
              type: "success",
              message: res.data.msg
            });
            // 清空表单
            this.dialogVisible = false;
            this.dispatchForm = {};
            // 刷新列表
            this.getJobs();
          });
        }
      });
    }
  },
  created() {
    this.getJobs();
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
  margin: 0.5em 0;
}
.condition {
  width: 96%;
  text-align: right;
}
.condition /deep/ .el-form-item__label {
  font-size: 0.8em !important;
  font-weight: 350;
}
.condition .el-input {
  width: 15em;
}
.condition .el-select {
  width: 12.8em;
}
.el-table .el-link {
  font-size: 0.6em;
  font-weight: 400;
  margin: 0 1em;
}
</style>