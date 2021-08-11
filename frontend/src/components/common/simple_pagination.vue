<template>
  <el-pagination
    @current-change="handleCurrentChange"
    small
    :current-page="page"
    :page-size="page_size"
    layout="total, prev, pager, next, jumper"
    :total="count"
  ></el-pagination>
</template>
<script>
export default {
  props: ["count", "page", "page_size"],
  data() {
    return {};
  },
  methods: {
    // 这是钩子函数
    handleCurrentChange(currentPage) {
      // 修改后刷新当前页数据
      this.$emit("update:page", currentPage);
      this.$emit("function");
    }
  }
};
</script>
<style scoped>
</style>
