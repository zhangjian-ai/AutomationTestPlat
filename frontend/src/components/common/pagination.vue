<template>
  <el-pagination
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"
    small
    :current-page="page"
    :page-sizes="[15, 30, 60, 100]"
    :page-size="page_size"
    layout="total, sizes, prev, pager, next, jumper"
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
    handleSizeChange(size) {
      // 变更页面条数时，把当前页设置为1
      this.$emit("update:page", 1);

      // 修改后刷新当前页数据
      this.$emit("update:page_size", size);
      this.$emit("function");
    },

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
