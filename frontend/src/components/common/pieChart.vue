<template>
  <div id="chart" class="chart"></div>
</template>
<script>
// 安装依赖: npm install echarts --save
// main.js 全局引入:
// import echarts from "echarts";
// Vue.prototype.$echarts = echarts;

import echarts from "echarts";
export default {
  props: {
    category: {
      type: Array,
      required: true
    },
    title: {
      type: String,
      default: ""
    },
    colors: {
      type: Array,
      required: true
    },
    data: {
      type: Array,
      required: true
    }
  },
  data() {
    return {};
  },

  methods: {
    drawPieChart() {
      let that = this;
      const chartPie = echarts.init(document.getElementById("chart"));
      // 饼图配置信息
      const options = {
        // 当hover时,饼图分类区域上面展示的文字
        tooltip: {
          trigger: "item",
          formatter: "{a}<br/>{b}: {c}<br/>占比: {d}%"
          //   formatter: "{b}: {c} [{d}%]"
        },
        legend: {
          // 分类标签内容及其展示的位置
          data: that.category,
          left: 10,
          // 纵向排列
          orient: "vertical"
          //   下面注释的代码是控制分类放在哪个地方,需要体验的话，直接把上面的代码注释，把下面的代码解开注释即可
          //   data: ["直接访问", "邮件营销", "联盟广告", "视频广告", "搜索引擎"],
          //   left: "center",
          //   top: "bottom",
          //   orient: "horizontal"
        },
        series: [
          {
            name: that.title,
            // 图表类型:pie、line、bar等
            type: "pie",
            // 圆圈的粗细
            radius: ["45%", "80%"],
            // 圆圈的位置
            center: ["55%", "55%"],
            // 是否规避标签重叠
            avoidLabelOverlap: true,
            // 动画持续时间：2秒  进入页面时饼图的加载时长
            animationDuration: 1000,
            // label标签样式
            label: {
              // 不在饼图中心展示分类标题. show为true时,所有的label都将展示在饼图中间,会重叠
              //   show: false,
              //   position: "center",

              // formatter 存在时,表示展示饼图分类的引用说明标签
              show: true,
              formatter: "{b}:{c}",
              textStyle: {
                color: "#333",
                fontSize: 12
              }
            },
            // 饼图分类item样式
            itemStyle: {
              color: function(params) {
                // 自定义颜色
                var colorList = that.colors;
                return colorList[params.dataIndex];
              }
            },
            // 标签的延伸线的样式,默认为true
            labelLine: {
              show: true
            },
            // emphasis 表示当hover时的一些样式变化
            emphasis: {
              // hover时label展示样式,将覆盖上面的textStyle
              label: {
                show: true,
                fontSize: "14",
                fontWeight: "bold"
              }
            },
            data: that.data
          }
        ]
      };
      // 将配置注册到饼图对象
      chartPie.setOption(options);
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.drawPieChart();
    });
  },
  watch: {
    data() {
      setTimeout(this.drawPieChart(), 200);
    }
  }
};
</script>
<style scoped>
.chart {
  width: 95%;
  height: 95%;
}
</style>