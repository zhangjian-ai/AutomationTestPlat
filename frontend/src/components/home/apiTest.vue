<template>
  <div>
    <!-- 请求参数表单 -->
    <el-form :model="baseForm" class="base-form">
      <!-- 基本信息 -->
      <el-form-item>
        <el-input placeholder="url" v-model="baseForm.url" class="input-url" @blur="parseUrl()">
          <el-select
            v-model="baseForm.method"
            slot="prepend"
            placeholder="请求方式"
            class="select-method"
          >
            <el-option label="GET" value="get"></el-option>
            <el-option label="POST" value="post"></el-option>
            <el-option label="PUT" value="put"></el-option>
            <el-option label="DELETE" value="delete"></el-option>
          </el-select>
        </el-input>
        <el-button type="primary" @click="executeTest()">执行</el-button>
      </el-form-item>
      <!-- 详细参数 -->
      <el-form-item>
        <span style="font-size: 1.2em;">请求参数</span>
        <el-tabs type="border-card">
          <!-- query 参数 -->
          <el-tab-pane label="Params">
            <span style="margin-right: 1.5em">Query 参数</span>
            <el-button size="mini" icon="el-icon-plus" @click="addKeyValue(0)" circle></el-button>
            <el-table
              :data="params"
              size="mini"
              :header-cell-style="{background:'#eef1f6', color:'#606266', 'text-align': 'center', 'height': '1.2em', 'line-height': '1.2em'}"
            >
              <el-table-column label="KEY" prop="key" width="100px" align="center"></el-table-column>
              <el-table-column label="VALUE" prop="value" align="center"></el-table-column>
              <el-table-column label="操作" width="150px" align="center">
                <template slot-scope="scope">
                  <el-button
                    size="mini"
                    type="success"
                    icon="el-icon-edit"
                    circle
                    @click="editKeyValue(scope.$index, 0)"
                  ></el-button>
                  <el-button
                    size="mini"
                    type="danger"
                    icon="el-icon-delete"
                    circle
                    @click="deleteKeyValue(scope.$index)"
                  ></el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <!-- body 参数 -->
          <el-tab-pane label="Body">
            <span style="font-size: 1.2em;">Body 参数</span>
            <vueJsonEditor v-model="body" :mode="'code'" lang="zh"></vueJsonEditor>
          </el-tab-pane>
          <!-- header 参数 -->
          <el-tab-pane label="Header">
            <span style="margin-right: 1.5em">Header 参数</span>
            <el-button size="mini" icon="el-icon-plus" @click="addKeyValue(2)" circle></el-button>
            <el-table
              :data="headers"
              size="mini"
              :header-cell-style="{background:'#eef1f6', color:'#606266', 'text-align': 'center', 'height': '1.2em', 'line-height': '1.2em'}"
            >
              <el-table-column label="KEY" prop="key" width="100px" align="center"></el-table-column>
              <el-table-column label="VALUE" prop="value" align="center"></el-table-column>
              <el-table-column label="操作" width="150px" align="center">
                <template slot-scope="scope">
                  <el-button
                    size="mini"
                    type="success"
                    icon="el-icon-edit"
                    circle
                    @click="editKeyValue(scope.$index, 2)"
                  ></el-button>
                  <el-button
                    size="mini"
                    type="danger"
                    icon="el-icon-delete"
                    circle
                    @click="deleteKeyValue(scope.$index, 2)"
                  ></el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <!-- cookie 参数 -->
          <el-tab-pane label="Cookie">
            <span style="margin-right: 1.5em">Cookie 配置</span>
            <el-button size="mini" icon="el-icon-plus" @click="addKeyValue(3)" circle></el-button>
            <el-table
              :data="cookies"
              size="mini"
              :header-cell-style="{background:'#eef1f6', color:'#606266', 'text-align': 'center', 'height': '1.2em', 'line-height': '1.2em'}"
            >
              <el-table-column label="KEY" prop="key" width="100px" align="center"></el-table-column>
              <el-table-column label="VALUE" prop="value" align="center"></el-table-column>
              <el-table-column label="操作" width="150px" align="center">
                <template slot-scope="scope">
                  <el-button
                    size="mini"
                    type="success"
                    icon="el-icon-edit"
                    circle
                    @click="editKeyValue(scope.$index, 3)"
                  ></el-button>
                  <el-button
                    size="mini"
                    type="danger"
                    icon="el-icon-delete"
                    circle
                    @click="deleteKeyValue(scope.$index, 3)"
                  ></el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </el-form-item>
      <!-- 执行结果 -->
      <el-from-item v-if="responseCode">
        <br />
        <span style="font-size: 1.2em;">执行结果</span>
        <span style="font-size: 0.8em; margin-left: 2em;">状态码: {{ responseCode }}</span>
        <el-tabs type="border-card">
          <!-- 响应 header -->
          <el-tab-pane label="Response Header">
            <vueJsonEditor v-model="responseHeader" :mode="'view'" lang="zh"></vueJsonEditor>
          </el-tab-pane>
          <!-- 响应 body -->
          <el-tab-pane label="Response Body">
            <vueJsonEditor v-model="responseBody" :mode="'view'" lang="zh"></vueJsonEditor>
          </el-tab-pane>
        </el-tabs>
      </el-from-item>
    </el-form>
    <!-- 参数新增、编辑弹窗 -->
    <el-dialog
      title="键值对 参数"
      :visible.sync="dialogVisible"
      width="30em"
      :show-close="false"
      close-on-click-modal
    >
      <el-form :model="tempForm" status-icon size="mini" label-width="20%" class="dialog-form">
        <el-form-item label="KEY: ">
          <el-input v-model="tempForm.key"></el-input>
        </el-form-item>
        <el-form-item label="VALUE: ">
          <el-input type="textarea" rows="3" v-model="tempForm.value"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="closeDialog()" size="mini">取 消</el-button>
        <el-button type="primary" @click="saveDialog()" size="mini">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import { execute_test } from "@/api";
import vueJsonEditor from "vue-json-editor";

export default {
  data() {
    return {
      baseForm: {},
      params: [],
      headers: [],
      cookies: [],

      // body 当前只支持json串
      body: "",
      tempForm: {},
      dialogVisible: false,
      // 记录谁打开的键值对弹窗
      // 0-query, 1-body, 2-header, 3-cookie
      origin: 0,

      // 响应
      responseCode: 0,
      responseHeader: "",
      responseBody: ""
    };
  },
  methods: {
    // 新增Query键值对
    addKeyValue(origin) {
      this.dialogVisible = true;
      this.origin = origin;
    },

    // 删除Query键值对
    deleteKeyValue(index, origin) {
      if (origin == 0) {
        this.params.splice(index, 1);
      }
      if (origin == 2) {
        this.headers.splice(index, 1);
      }
      if (origin == 3) {
        this.cookies.splice(index, 1);
      }
    },

    // 编辑Query键值对
    editKeyValue(index, origin) {
      this.addKeyValue(origin);
      if (origin == 0) {
        this.tempForm = JSON.parse(
          JSON.stringify(this.params.slice(index, index + 1)[0])
        );
      }
      if (origin == 2) {
        this.tempForm = JSON.parse(
          JSON.stringify(this.headers.slice(index, index + 1)[0])
        );
      }
      if (origin == 3) {
        this.tempForm = JSON.parse(
          JSON.stringify(this.cookies.slice(index, index + 1)[0])
        );
      }
    },

    // 关闭弹窗
    closeDialog() {
      this.dialogVisible = false;
      this.tempForm = {};
    },

    // 确认弹窗修改
    saveDialog() {
      if (this.tempForm.key) {
        // query 参数保存逻辑
        if (this.origin == 0) {
          this.params.forEach(item => {
            if (item.key == this.tempForm.key) {
              item.value = this.tempForm.value;
              this.tempForm = {};
            }
          });

          if (this.tempForm.key) {
            this.params.push(this.tempForm);
          }
        }

        // header 参数保存逻辑
        if (this.origin == 2) {
          this.headers.forEach(item => {
            if (item.key == this.tempForm.key) {
              item.value = this.tempForm.value;
              this.tempForm = {};
            }
          });

          if (this.tempForm.key) {
            this.headers.push(this.tempForm);
          }
        }

        // cookie 参数保存逻辑
        if (this.origin == 3) {
          this.cookies.forEach(item => {
            if (item.key == this.tempForm.key) {
              item.value = this.tempForm.value;
              this.tempForm = {};
            }
          });

          if (this.tempForm.key) {
            this.cookies.push(this.tempForm);
          }
        }
      }
      this.closeDialog();
    },

    // 解析URL
    parseUrl() {
      let tempArray = this.baseForm.url.split("?");
      let url = tempArray[0];

      if (tempArray[1]) {
        this.params = [];
        var queryArray;
        try {
          queryArray = decodeURI(tempArray[1]).split("&");

          queryArray.forEach(item => {
            this.params.push({
              key: item.split("=")[0],
              value: item.split("=")[1]
            });
          });

          this.baseForm.url = url;
        } catch (URIError) {
          this.$message({
            type: "error",
            message: "URL解析错误"
          });
        }
      }
    },

    // 执行接口测试
    executeTest() {
      if (this.baseForm.method && this.baseForm.url) {
        execute_test({
          url: this.baseForm.url,
          method: this.baseForm.method,
          params: this.params,
          body: this.body,
          headers: this.headers,
          cookies: this.cookies
        }).then(res => {
          this.responseCode = res.data.code;
          this.responseHeader = res.data.headers;
          this.responseBody = res.data.body;
        });
      } else {
        this.$message({
          type: "error",
          message: "缺少基本请求信息"
        });
      }
    }
  },

  watch: {},

  components: {
    vueJsonEditor
  }
};
</script>
<style scoped>
.base-form {
  width: 70%;
}
.dialog-form {
  width: 90%;
}
.input-url {
  margin-right: 1em;
  width: 80%;
}
.select-method {
  width: 8em;
}
.select-protocol {
  margin-right: 1em;
  width: 6em;
}
</style>    