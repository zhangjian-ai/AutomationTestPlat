<template>
  <div>
    <!-- 任务列表 -->
    <el-col :span="7" v-show="showJobs">
      <div class="job_list">
        <el-row class="title">
          <el-col :span="20">
            <span>{{ type == 0 ? '我的任务(未完成)' : '我的任务(已完成)' }}</span>
          </el-col>
          <el-col :span="4">
            <el-button
              size="mini"
              icon="el-icon-refresh"
              type="primary"
              style="padding: 0.5em;"
              @click="getJobList()"
            >{{ type == 0 ? '已完成' : '未完成' }}</el-button>
          </el-col>
        </el-row>
        <el-divider></el-divider>
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
            :count="job_count"
            :page.sync="job_page"
            :page_size.sync="job_page_size"
            @function="getJobList()"
          ></pagination>
        </div>
      </div>
    </el-col>
    <el-col :span="showJobs ? 1 : 0">
      <pre style="margin:0; padding: 0;">&nbsp;</pre>
    </el-col>
    <!-- 工作区 -->
    <el-col :span="showJobs ? 16 : 24" v-show="currentJob.task_no">
      <!-- 任务详情 -->
      <div class="job_detail">
        <el-row>
          <el-col
            :span="16"
            style="font-size: 1.5em; font-weight: bolder;"
          >{{ currentJob.task_name | ellipsis(showJobs) }}</el-col>
          <el-col :span="8" style="text-align: right;">
            <el-button
              v-show="currentJob.status == 3"
              size="mini"
              type="danger"
              @click="modifyJob(4)"
            >完成</el-button>
            <el-button
              v-show="currentJob.status != 4 && showJobs"
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
        <el-descriptions :column="4" direction="vertical" border v-show="showJobs">
          <!-- <template slot="extra"></template> -->
          <el-descriptions-item label="责任人">{{currentJob.executor_name }}</el-descriptions-item>
          <el-descriptions-item label="任务类型">{{ currentJob.type_str }}</el-descriptions-item>
          <el-descriptions-item label="计划完成时间">{{ currentJob.expect_end_time }}</el-descriptions-item>
          <el-descriptions-item label="属性标签">
            <el-tag size="small" type="danger" effect="dark" v-show="jobWarningTag(currentJob)">
              <i class="el-icon-warning"></i>
              &nbsp;{{ jobWarningTag(currentJob) }}
            </el-tag>
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
          </el-descriptions-item>
          <el-descriptions-item label="关联需求">{{currentJob.prd_no }}</el-descriptions-item>
          <el-descriptions-item label="任务编号">{{currentJob.task_no }}</el-descriptions-item>
          <el-descriptions-item label="任务描述">{{currentJob.task_detail }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <!-- 用例详情 -->
      <div>
        <!-- 用例列表 -->
        <el-col :span="7" v-if="!showJobs">
          <div class="case_list">
            <span class="title">用例列表</span>
            <el-divider></el-divider>
            <el-table
              :data="caseList"
              :show-header="false"
              v-loading="loading"
              row-key="id"
              highlight-current-row
              @current-change="handleRowChange"
            >
              <el-table-column label="序号" type="index" min-width="50%" align="center"></el-table-column>
              <el-table-column
                align="left"
                prop="case.name"
                :min-width="showJobs ? '200%' : '210%'"
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
            <!-- 分页 -->
            <div style="text-align: right;">
              <pagination
                :count="case_count"
                :page.sync="case_page"
                :page_size.sync="case_page_size"
                @function="getCaseList"
              ></pagination>
            </div>
          </div>
        </el-col>
        <el-col :span="1">
          <pre style="margin:0; padding: 0;">&nbsp;</pre>
        </el-col>
        <!-- 用例详情 -->
        <el-col :span="16">
          <div class="case_detail" v-if="!showJobs && showCaseDetail">
            <el-descriptions
              :title="currentCase.case.name | ellipsis(showJobs)"
              size="small"
              border
            >
              <template slot="extra">
                测试结果:
                <el-select
                  :disabled="[4, 5].indexOf(currentJob.status) != -1"
                  v-model="currentCase.case_status"
                  filterable
                  size="mini"
                  style="width: 7em; margin-right: 2em;"
                >
                  <el-option
                    v-for="item in $store.state.case_status"
                    :key="item[0]"
                    :label="item[1]"
                    :value="item[0]"
                    :disabled="item[0] == 0"
                  ></el-option>
                </el-select>
                <el-button
                  :disabled="[4, 5].indexOf(currentJob.status) != -1"
                  size="mini"
                  type="primary"
                  @click="submitTestResult()"
                >确 定</el-button>
              </template>
              <el-descriptions-item label="用例编号">{{ currentCase.case.no }}</el-descriptions-item>
              <el-descriptions-item
                label="所属模块"
              >{{ (currentCase.case.module_str1 ? currentCase.case.module_str1 + " / " : "") + (currentCase.case.module_str2 ? currentCase.case.module_str2 + " / " : "") + (currentCase.case.module_str3 ? currentCase.case.module_str3 : "") }}</el-descriptions-item>
              <el-descriptions-item label="属性标签">
                <el-tag
                  size="mini"
                  :type="caseTag[currentCase.case.priority_str]"
                  effect="dark"
                >{{ currentCase.case.priority_str }}</el-tag>
                <el-tag v-show="currentCase.case.is_auto" size="mini" type="primary" effect="dark">A</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="AUTHOR" :span="1">{{ currentCase.case.author }}</el-descriptions-item>
              <el-descriptions-item label="用例描述" :span="2">{{ currentCase.case.description }}</el-descriptions-item>
              <el-descriptions-item label="测试步骤" :span="3">{{ currentCase.case.step }}</el-descriptions-item>
              <el-descriptions-item label="预期结果" :span="3">{{ currentCase.case.expectation }}</el-descriptions-item>
            </el-descriptions>
          </div>
          <!-- 富文本编辑器 -->
          <editor
            v-show="!showJobs && currentJob.status != 4 && showCaseDetail"
            :value.sync="currentCase.test_detail"
            ref="richText"
          ></editor>
          <div class="results" v-show="currentJob.status == 4 && showCaseDetail">
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
  saveTestResult,
  modify_job,
  query_case
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

      // 用例等级标签类型映射
      caseTag: {
        高: "danger",
        中: "success",
        低: "info"
      },

      // 测试任务切换变量 0:未完成  1:已完成
      type: 0,

      // 分页
      job_count: 0,
      job_page: 1,
      job_page_size: 15,
      case_count: 0,
      case_page: 1,
      case_page_size: 15,

      // 当前选中的任务对象、用例列表
      currentJob: {},
      currentCase: {},
      caseList: [],

      // 是否展示列表
      showJobs: true,

      // 是否展示用例详情
      showCaseDetail: false
    };
  },

  methods: {
    // 获取当前登陆人员的测试任务
    getJobList() {
      let status = this.type == 0 ? "finish" : "unfinish";
      this.type = this.type == 0 ? 1 : 0;
      // 加载任务列表
      this.loadJobList(status);
    },

    // 加载测试任务
    loadJobList(status) {
      this.loading = true;

      job_list(this.job_page, this.job_page_size, status).then(res => {
        this.jobList = res.data.results;
        this.job_count = res.data.count;
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
      // 赋值之前清空一下可能未使用的图片
      this.$refs.richText.clearAllImage();

      if (!now.case.no) {
        this.showCaseDetail = false;

        // 获取用例详情
        query_case(now.case.id).then(res => {
          now.case = JSON.parse(JSON.stringify(res.data));
          this.currentCase = JSON.parse(JSON.stringify(now));

          this.showCaseDetail = true;
        });
      } else {
        this.currentCase = JSON.parse(JSON.stringify(now));
      }
    },

    // 开始测试
    startTest() {
      this.showJobs = !this.showJobs;
      this.showCaseDetail = false;

      // 还原页码
      this.case_page = 1;
      this.getCaseList();
    },

    // 获取用例列表
    getCaseList() {
      // 清空用例列表及详情
      this.caseList = [];
      this.currentCase = {};

      if (!this.showJobs) {
        this.loading = true;
        // 关闭任务列表则加载用例列表
        job_case_detail(
          this.case_page,
          this.case_page_size,
          this.currentJob.id
        ).then(res => {
          this.caseList = res.data.results;
          this.case_count = res.data.count;

          // 获取用例详情
          query_case(this.caseList[0].case.id).then(res => {
            this.caseList[0].case = JSON.parse(JSON.stringify(res.data));
            this.currentCase = JSON.parse(JSON.stringify(this.caseList[0]));

            this.loading = false;
            this.showCaseDetail = true;
          });
        });
      } else {
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

    // 保存测试结果
    submitTestResult() {
      let that = this;
      // 提交之前先清空无效的图片链接
      this.$refs.richText.clearInvalidImage();

      if (this.currentCase.test_detail) {
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
      } else {
        this.$message.warning({
          message: "请记录您的测试结果"
        });
      }
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

        this.showCaseDetail = false;
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
      let num = showJobs ? 25 : 30;
      if (value.length > num) {
        return value.slice(0, num) + " ...";
      }
      return value;
    }
  }
};
</script>
<style scoped>
.el-tag {
  margin: 0 0.5em;
}
.el-divider {
  margin: 0.5em 0;
  background-color: tomato;
  padding: 1px 0;
}
div /deep/ .el-table__body tr.current-row > td {
  background-color: #3b7ec5 !important;
  color: whitesmoke;
}
div /deep/ .el-table--enable-row-hover .el-table__body tr:hover > td {
  background: #609fe2 !important;
  color: whitesmoke;
}

.job_list {
  background-color: gainsboro;
  padding: 0.5em 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}
.job_list .title {
  font-size: 1.2em;
  color: rgb(49, 119, 189);
  font-weight: bolder;
  margin: 0.2em 1em;
}
.job_list .el-table {
  border: 1px solid gainsboro;
}
.job_detail {
  padding: 0.5em;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}
.job_detail .el-row {
  margin: 0.5em 0;
}
.job_detail /deep/ .el-descriptions__title {
  font-size: 1.5em;
}

.case_list {
  margin: 0.5em 0;
  background-color: gainsboro;
  padding: 0.5em 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}
.case_list .title {
  font-size: 1.2em;
  color: rgb(49, 119, 189);
  font-weight: bolder;
  margin: 0.2em 1em;
}

.case_list .el-table {
  font-size: 0.8em;
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
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}

.results {
  padding: 1em;
  margin-top: 1.5em;
  max-height: 40em;
  overflow: auto;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}
.results .banner {
  font-size: 1.5em;
  font-weight: bolder;
  text-align: center;
  padding: 0;
  margin: 0.2em 0;
}
.results >>> img {
  max-height: 12em;
}
</style>