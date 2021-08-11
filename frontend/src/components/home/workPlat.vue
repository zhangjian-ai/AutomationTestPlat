<template>
  <div>
    <!-- 任务列表 -->
    <el-col :span="7" v-show="showJobs">
      <div class="job_list">
        <div class="title">
          <span>{{ type == 0 ? '我的任务(未完成)' : '我的任务(已完成)' }}</span>
          <el-button
            size="mini"
            icon="el-icon-refresh"
            type="primary"
            style="margin-left: 8em; padding: 0.5em;"
            @click="getJobList()"
          >{{ type == 0 ? '已完成' : '未完成' }}</el-button>
          <el-divider></el-divider>
        </div>
        <el-table
          :data="jobList"
          :show-header="false"
          highlight-current-row
          v-loading="loading"
          @row-click="handleJobRowClick"
        >
          <el-table-column align="left" prop="task_name" width="230" show-overflow-tooltip></el-table-column>
          <el-table-column align="center">
            <template slot-scope="scope">
              <el-tag
                size="mini"
                :type="levelTag[scope.row.level]"
                effect="dark"
              >{{ scope.row.level_str }}</el-tag>
              <el-tag
                size="mini"
                :type="statusTag[scope.row.status]"
                effect="dark"
              >{{ scope.row.status_str }}</el-tag>
            </template>
          </el-table-column>
        </el-table>
        <!-- 分页 -->
        <div style="text-align: right;">
          <pagination
            :count="count"
            :page.sync="page"
            :page_size.sync="page_size"
            @function="getJobList"
          ></pagination>
        </div>
      </div>
    </el-col>
    <el-col :span="showJobs ? 1 : 0">
      <pre style="margin:0; padding: 0;">&nbsp;</pre>
    </el-col>
    <!-- 工作区 -->
    <el-col :span="showJobs ? 16 : 24" v-show="currentJob.task_no">
      <!-- 任务详情区 -->
      <div class="job_detail">
        <el-row>
          <span style="color: tomato; font-size: 1.4em;">{{ currentJob.type_str }}</span>
          <span style="margin-left: 3em; font-size: 0.8em;">
            责任人:
            <span style="color: #3a6b9c; font-size: 1.2em;">{{currentJob.executor_name }}</span>
          </span>
          <span style="margin-left: 3em; font-size: 0.8em;">任务编号: {{currentJob.task_no }}</span>
          <span style="margin-left: 3em; font-size: 0.8em;">计划完成时间: {{currentJob.expect_end_time }}</span>
        </el-row>
        <el-row>
          <el-col :span="19">
            <span
              style="font-size: 1.6em; font-weight: bolder;"
            >{{ currentJob.task_name | ellipsis(showJobs) }}</span>
          </el-col>
          <el-col :span="4" class="detail_tag">
            <el-tag
              size="small"
              :type="levelTag[currentJob.level]"
              effect="dark"
            >{{ currentJob.level_str }}</el-tag>
            <el-tag
              size="small"
              :type="statusTag[currentJob.status]"
              effect="dark"
            >{{ currentJob.status_str }}</el-tag>
          </el-col>
        </el-row>
        <el-row>
          <span style="font-size: 0.8em;">
            详细描述:
            <span style="color: gray;">{{ currentJob.task_detail}}</span>
          </span>
        </el-row>
        <el-row>
          <el-col :span="11">
            <span style="font-size: 0.8em;">关联需求: {{ currentJob.prd_no }}</span>
          </el-col>
          <el-col :span="4">
            <span v-if="jobWarningTag(currentJob)" style="color: red; font-size: 1.1em;">
              <i class="el-icon-warning"></i>
              &nbsp;{{ jobWarningTag(currentJob) }}
            </span>
            <pre v-else style="margin:0; padding: 0;">&nbsp;</pre>
          </el-col>
          <el-col :span="7" style="text-align: right;">
            <el-button
              v-show="currentJob.status == 3"
              size="mini"
              type="danger"
              @click="modifyJob(4)"
            >关闭</el-button>
            <el-button
              v-show="currentJob.status != 4"
              size="mini"
              type="info"
              @click="modifyJob()"
            >{{ currentJob.status == 5 ? '解挂' : '挂起' }}</el-button>
            <el-button
              v-show="[4, 5].indexOf(currentJob.status) == -1"
              size="mini"
              type="primary"
              @click="startTest()"
            >{{ showJobs ? '开始测试' : '任务列表' }}</el-button>
            <el-button
              v-show="currentJob.status == 4"
              size="mini"
              type="primary"
              @click="startTest()"
            >{{ showJobs ? '查看详情' : '任务列表' }}</el-button>
          </el-col>
        </el-row>
      </div>
      <!-- 用例详情 -->
      <div>
        <!-- 用例列表 -->
        <el-col :span="7" v-if="!showJobs">
          <div class="case_list">
            <span class="title">用例列表</span>
            <span>
              共
              <span style="color: dodgerblue;">{{ caseList ? caseList.length : 0 }}</span> 条用例
            </span>
            <el-divider></el-divider>
            <el-table
              :data="caseList"
              :show-header="false"
              v-loading="loading"
              row-key="id"
              highlight-current-row
              @current-change="handleRowChange"
            >
              <el-table-column label="序号" type="index" width="50" align="center"></el-table-column>
              <el-table-column
                align="left"
                prop="case.case_name"
                :width="showJobs ? 200 : 210"
                show-overflow-tooltip
              ></el-table-column>
              <el-table-column align="center">
                <template slot-scope="scope">
                  <el-tag
                    size="mini"
                    hit
                    :type="caseStatusTag[scope.row.case_status]"
                    :effect="scope.row.case_status == 0 ? 'plain' : 'dark'"
                  >{{ scope.row.case_status_str }}</el-tag>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-col>
        <el-col :span="1">
          <pre style="margin:0; padding: 0;">&nbsp;</pre>
        </el-col>
        <!-- 用例详情 -->
        <el-col :span="16">
          <div class="case_detail" v-if="currentCase.id">
            <el-row>
              <span style="color: orangered;">{{ currentCase.case.case_id }}</span>
              <span style="margin-left: 2em; font-size: 0.8em;">
                测试系统:
                <span style="color: tomato;">{{ currentCase.case.client }}</span>
              </span>
              <span style="margin-left: 2em; font-size: 0.8em;">
                功能模块:
                <span style="color: tomato;">{{ currentCase.case.module }}</span>
              </span>
            </el-row>
            <el-row>
              <el-col :span="20">
                <span
                  style="font-size: 1.1em;"
                >{{ currentCase.case.case_name | ellipsis(showJobs) }}</span>
              </el-col>
              <el-col :span="3" class="detail_tag">
                <el-tag size="mini" type="primary">{{ currentCase.case.level_value }}</el-tag>
                <el-tag v-show="currentCase.case.is_auto" size="mini" type="primary">A</el-tag>
              </el-col>
            </el-row>
            <el-row>
              <span style="font-size: 0.8em;">
                用例描述:
                <span style="color: gray;">{{ currentCase.case.description }}</span>
              </span>
            </el-row>
            <!-- 测试步骤、结果 -->
            <el-row>
              <el-col :span="18" style="font-size: 0.8em;">
                测试步骤:
                <br />
                <el-col :span="1">
                  <pre style="margin:0; padding: 0;">&nbsp;</pre>
                </el-col>
                <el-col :span="22">
                  <div class="case_step">{{ currentCase.case.step }}</div>
                </el-col>
              </el-col>
              <el-col :span="6" style="font-size: 0.8em;">
                <el-row>
                  测试结果:
                  <el-select
                    :disabled="[4, 5].indexOf(currentJob.status) != -1"
                    v-model="currentCase.case_status"
                    filterable
                    size="mini"
                    style="width: 8em;"
                  >
                    <el-option
                      v-for="item in case_statusList"
                      :key="item[0]"
                      :label="item[1]"
                      :value="item[0]"
                      :disabled="item[0] == 0"
                    ></el-option>
                  </el-select>
                </el-row>
                <el-row style="margin-top:2em;">
                  <el-button
                    :disabled="[4, 5].indexOf(currentJob.status) != -1"
                    size="mini"
                    type="primary"
                    @click="submitTestResult()"
                  >确 定</el-button>
                </el-row>
              </el-col>
            </el-row>
          </div>
          <!-- 富文本编辑器 -->
          <editor
            v-show="currentJob.status != 4 && currentCase.id"
            :value.sync="currentCase.test_detail"
            ref="richText"
          ></editor>
          <div class="results" v-show="currentJob.status == 4 && currentCase.test_detail">
            <p class="banner">测 试 记 录</p>
            <div v-html="currentCase.test_detail"></div>
          </div>
        </el-col>
      </div>
    </el-col>
  </div>
</template>
<script>
/* eslint-disable */

import pagination from "../common/simple_pagination.vue";
import editor from "../common/editor.vue";

import {
  job_list,
  job_case_detail,
  get_constants,
  saveTestResult,
  modify_job
} from "@/api";
export default {
  data() {
    return {
      // 测试任务列表
      jobList: [],

      //  加载中
      loading: false,

      // 任务标签对象
      statusTag: {
        2: "wanring",
        3: "primary",
        4: "success",
        5: "info"
      },
      levelTag: {
        0: "danger",
        1: "warning",
        2: "success",
        3: "info"
      },
      caseStatusTag: {
        0: "info",
        1: "success",
        2: "danger",
        3: "warning",
        4: "info"
      },

      // 用例状态列表
      case_statusList: [],

      // 测试任务切换变量 0:未完成  1:已完成
      type: 0,

      // 分页
      count: 0,
      page: 1,
      page_size: 15,

      // 当前选中的任务对象、用例列表
      currentJob: {},
      currentCase: {},
      caseList: [],

      // 是否展示列表
      showJobs: true
    };
  },

  methods: {
    // 获取当前登陆人员的测试任务
    getJobList() {
      let status = "";
      if ((this.page, this.page_size, this.type == 0)) {
        status = "finish";
        this.type = 1;
      } else {
        status = "unfinish";
        this.type = 0;
      }
      this.loadJobList(status);
    },

    // 加载测试任务
    loadJobList(status) {
      this.loading = true;

      job_list(this.page, this.page_size, status).then(res => {
        this.jobList = res.data.results;
        this.count = res.data.count;
        if (this.jobList[0]) {
          this.currentJob = this.jobList[0];
        } else {
          this.currentJob = {};
        }
        this.loading = false;
      });
    },

    // 测试任务行点击事件
    handleJobRowClick(row) {
      if (this.currentJob.task_no != row.task_no) {
        this.currentJob = row;
      }
    },

    // 用例当前行变化的事件
    handleRowChange(now, old) {
      if (this.currentCase.id != now.id) {
        // 赋值之前清空一下可能未使用的图片
        this.$refs.richText.clearAllImage();
        this.currentCase = JSON.parse(JSON.stringify(now));
      }
    },

    // 开始测试
    startTest() {
      this.showJobs = !this.showJobs;

      if (!this.showJobs) {
        this.loading = true;
        // 关闭任务列表则加载用例列表
        job_case_detail(this.currentJob.id).then(res => {
          this.caseList = res.data;
          this.loading = false;

          this.currentCase = JSON.parse(JSON.stringify(this.caseList[0]));
        });
      } else {
        // 清空用例列表及详情
        this.caseList = [];
        this.currentCase = {};

        // 清空可能未使用的图片
        this.$refs.richText.clearAllImage();
      }
    },

    // 任务预警标签
    jobWarningTag(job) {
      let days = Math.ceil(
        (new Date(job.expect_end_time) - new Date()) / (24 * 60 * 60 * 1000)
      );
      if (job.status != 4 && 0 < days && days <= 2) {
        return "即将到期";
      }
      if (job.status != 4 && days <= 0) {
        return "已延期";
      }
      if (job.status == 4 && job.is_delay == true) {
        return "延期关闭";
      }
      return false;
    },

    // 加载搜索栏下拉框、用例等级信息
    loadOption() {
      get_constants("JOB").then(res => {
        this.case_statusList = res.data.CASE_STATUS;
      });
    },

    // 保存测试结果
    submitTestResult() {
      let that = this;
      // 提交之前先清空无效的图片链接
      this.$refs.richText.clearInvalidImage();

      saveTestResult({
        // 组装请求数据
        id: this.currentCase.id,
        case_status: this.currentCase.case_status,
        test_detail: this.currentCase.test_detail
      }).then(res => {
        this.$message.success(res.data.msg);

        // 再不刷新的情况下临时修改用例状态
        let data = res.data.data;
        for (let i in this.caseList) {
          if (this.caseList[i].id == data.id) {
            this.caseList[i].case_status = data.case_status;
            this.caseList[i].case_status_str = data.case_status_str;
            this.caseList[i].test_detail = data.test_detail;

            // 修改任务状态
            if (this.currentJob.status == 2) {
              this.currentJob.status = 3;
              this.currentJob.status_str = "测试中";
            }

            // 清空富文本中图片列表
            that.$refs.richText.clearImageList();
            return;
          }
        }
      });
    },

    // 任务状态变更
    modifyJob(status = null) {
      let state = null;
      if (!status) {
        state = this.currentJob.status == 5 ? 2 : 5;
      } else {
        state = status;
      }
      modify_job({
        id: this.currentJob.id,
        status: state
      }).then(res => {
        this.$message.success(res.data.msg);
        this.currentJob.status = res.data.data.status;
        this.currentJob.status_str = res.data.data.status_str;

        // 关闭任务时,打开任务列表,同时清空用例列表
        if (state == 4) {
          this.showJobs = true;
          this.caseList = [];
          this.currentCase = {};
        }
      });
    }
  },
  created() {
    // 加载测试任务
    this.loadJobList("unfinish");
    this.loadOption();
  },
  beforeDestroy() {
    // 再清理一次未使用的图片
    this.$refs.richText.clearAllImage();
  },
  components: {
    pagination,
    editor
  },
  filters: {
    // 控制任务标题显示字数.
    // 过滤器中不能使用this,所以showJobs参数是在调用时一起传过来的
    ellipsis(value, showJobs) {
      if (!value) return "";
      let num = showJobs ? 20 : 30;
      if (value.length > num) {
        return value.slice(0, num) + " ...";
      }
      return value;
    }
  }
};
</script>
<style scoped>
.title span {
  font-size: 1.2em;
  color: rgb(49, 119, 189);
  font-weight: bolder;
  margin: 0.2em 1em;
}

.title .el-divider {
  margin: 0.5em 0;
  background-color: tomato;
  padding: 1px 0;
}

.job_list {
  background-color: silver;
  padding: 0.5em 0;
  border: 1px solid silver;
}

.job_list .el-tag {
  margin: 0 0.5em;
}
.job_list .el-table {
  font-size: 1em;
  height: 40em !important;
  overflow: auto;
}
/deep/ .el-table__body tr.current-row > td {
  background-color: #355e8a !important;
  color: whitesmoke;
}
/deep/ .el-table--enable-row-hover .el-table__body tr:hover > td {
  background: #608fc2 !important;
  color: whitesmoke;
}

.job_detail {
  padding: 0.5em;
  background-color: #dce2f1;
}
.job_detail .el-row {
  margin: 0.5em 0;
  line-height: 2em;
  height: 2em;
}
.job_detail .detail_tag {
  text-align: center;
}
.job_detail .detail_tag .el-tag {
  margin: 0 0.5em;
}

.case_list {
  margin: 0.5em 0;
  background-color: silver;
  padding: 0.5em 0;
  border: 1px solid silver;
}
.case_list .title {
  font-size: 1.2em;
  color: rgb(49, 119, 189);
  font-weight: bolder;
  margin: 0.2em 1em;
}
.case_list .el-divider {
  margin: 0.5em 0;
  background-color: tomato;
  padding: 1px 0;
}
.case_list .el-table {
  font-size: 0.8em;
  height: 55em !important;
  overflow: auto;
}
.case_list /deep/ .el-table td {
  line-height: 2em;
  height: 2em;
  padding: 0.5em 0;
}
.case_detail {
  margin: 0.5em 0;
  white-space: pre-line;
  /* 外层高度自适应内层变化.不指定height为自适应,加了之后会滚动显示超出部分 */
  overflow: auto;
  padding: 0.5em;
  background-color: #ebebe4;
}
.case_detail .el-row {
  margin: 0.3em 0;
  line-height: 1.5em;
  height: 1.5em;
}
.case_detail .el-row .el-tag {
  margin: 0 0.5em;
}
.case_detail .case_step {
  height: 8em;
  margin: 0 1em;
  padding: 0 1em;
  overflow: auto;
  background-color: whitesmoke;
}
.results {
  border-radius: 0.5em;
  padding: 1em;
  margin-top: 1.5em;
  background-color: whitesmoke;
  height: 30em;
  overflow: auto;
}
.results .banner {
  font-size: 1.5em;
  font-weight: bolder;
  text-align: center;
  padding: 0;
  margin: 0.5em 0;
}
.results >>> img {
  max-height: 15em;
}
</style>