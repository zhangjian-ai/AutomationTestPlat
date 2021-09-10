<template>
  <div>
    <el-row>
      <el-col :span="10">
        <div class="pieScope" v-if="$store.state.pie_title">
          <span>{{ $store.state.pie_title }} ({{ $store.state.pie_scope }})</span>
          <el-divider></el-divider>
          <div class="pieChart">
            <chart
              :data="$store.state.pie_data"
              :colors="$store.state.pie_colors"
              :category="$store.state.pie_category"
              :title="$store.state.pie_title"
            ></chart>
          </div>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <!-- <p>我是一块荒地 ...</p> -->
    </el-row>
  </div>
</template>
<script>
import chart from "@/components/common/pieChart.vue";
import {} from "@/api";
export default {
  props: [],
  data() {
    return {};
  },
  methods: {},
  mounted() {},
  components: {
    chart
  }
};
</script>
<style scoped>
.pieScope {
  width: 32em;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}
.pieScope span {
  margin: 0.5em;
  height: 2em;
  line-height: 2em;
  font-size: 1.2em;
  font-weight: bolder;
}
.pieScope .el-divider {
  padding: 0.4px 0;
  margin: 0 0 0.5em 0;
  background: #3cb371;
}
.pieScope .pieChart {
  width: 32em;
  height: 18em;
}
</style>
