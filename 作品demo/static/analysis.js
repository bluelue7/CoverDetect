import * as echarts from 'echarts';

// 基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('main'));
window.addEventListener('resize', function () {
  myChart.resize();
});
// 绘制图表
myChart.setOption({
  backgroundColor: 'white',
  title: {
    text: '检测结果分析',
    left: 'center',
    top: 20,
    textStyle: {
      color: '#746e6e'
    }
  },
  tooltip: {
    trigger: 'item'
  },
  visualMap: {
    show: false,
    min: 80,
    max: 600,
    inRange: {
      colorLightness: [0, 1]
    }
  },
  series: [
    {
      name: '检测结果分析',
      type: 'pie',
      radius: '55%',
      center: ['50%', '50%'],
      data: [
        {value: 335, name: 'good'},
        {value: 310, name: 'broken'},
        {value: 274, name: 'circle'},
        {value: 235, name: 'lose'},
        {value: 400, name: 'uncovered'}
      ].sort(function (a, b) {
        return a.value - b.value;
      }),
      roseType: 'radius',
      label: {
        color: '#4b1f12',
        fontWeight: 'bold'
      },
      labelLine: {
        lineStyle: {
          color: '#9d6858'
        },
        smooth: 0.2,
        length: 10,
        length2: 20
      },
      itemStyle: {
        color: '#c23531',

      },
      animationType: 'scale',
      animationEasing: 'elasticOut',
      animationDelay: function (idx) {
        return Math.random() * 200;
      }
    }
  ]
});