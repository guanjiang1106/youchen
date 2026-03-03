<template>
  <div class="app-container">
    <!-- 驾驶舱视图 -->
    <el-row :gutter="20" v-if="showDashboard" class="dashboard-container">
      <!-- 关键指标卡片 -->
      <el-col :span="6">
        <el-card shadow="hover" class="metric-card">
          <div class="metric-header">
            <span class="metric-title">总预测销售额</span>
            <el-tag type="success" size="small">今日</el-tag>
          </div>
          <div class="metric-value">{{ formatCurrency(totalPredictedAmount) }}</div>
          <div class="metric-trend">
            <span class="trend-up"><i class="el-icon-top"></i> 12.5%</span>
            <span class="trend-label">较昨日</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="metric-card">
          <div class="metric-header">
            <span class="metric-title">平均置信度</span>
            <el-tag type="warning" size="small">实时</el-tag>
          </div>
          <div class="metric-value">{{ averageConfidence }}%</div>
          <div class="metric-trend">
            <span class="trend-stable"><i class="el-icon-minus"></i> 0.0%</span>
            <span class="trend-label">较昨日</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="metric-card">
          <div class="metric-header">
            <span class="metric-title">覆盖区域数</span>
            <el-tag type="primary" size="small">统计</el-tag>
          </div>
          <div class="metric-value">{{ uniqueRegions }}</div>
          <div class="metric-trend">
            <span class="trend-up"><i class="el-icon-top"></i> 3</span>
            <span class="trend-label">新增区域</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="metric-card">
          <div class="metric-header">
            <span class="metric-title">模型版本分布</span>
            <el-tag type="info" size="small">分析</el-tag>
          </div>
          <div class="metric-value">{{ modelVersionsCount }}</div>
          <div class="metric-trend">
            <span class="trend-text">活跃模型：{{ latestModelVersion || '无' }}</span>
          </div>
        </el-card>
      </el-col>

      <!-- 图表区域 -->
      <el-col :span="12" style="margin-top: 20px;">
        <el-card shadow="always" class="chart-card">
          <div slot="header" class="clearfix">
            <span><i class="el-icon-data-line"></i> 销售预测趋势 (按日期)</span>
            <el-button style="float: right; padding: 3px 0" type="text" @click="refreshCharts">刷新</el-button>
          </div>
          <div ref="trendChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12" style="margin-top: 20px;">
        <el-card shadow="always" class="chart-card">
          <div slot="header" class="clearfix">
            <span><i class="el-icon-pie-chart"></i> 区域销售分布</span>
          </div>
          <div ref="regionChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
      <el-col :span="24" style="margin-top: 20px;">
        <el-card shadow="always" class="chart-card">
          <div slot="header" class="clearfix">
            <span><i class="el-icon-rank"></i> 置信度分布直方图</span>
          </div>
          <div ref="confidenceChart" style="height: 250px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 切换按钮 -->
    <el-row :gutter="10" class="mb8" style="display: flex; justify-content: space-between; align-items: center;">
      <div>
        <el-button 
          :type="showDashboard ? 'primary' : 'info'" 
          icon="el-icon-data-board" 
          size="small" 
          @click="toggleDashboard"
        >
          {{ showDashboard ? '切换至列表视图' : '切换至驾驶舱视图' }}
        </el-button>
      </div>
      <div v-if="!showDashboard">
        <el-button
          type="primary"
          plain
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
          v-hasPermi="['module_admin:forecast:add']"
        >新增</el-button>
        <el-button
          type="success"
          plain
          icon="el-icon-edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['module_admin:forecast:edit']"
        >修改</el-button>
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['module_admin:forecast:remove']"
        >删除</el-button>
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          @click="handleExport"
          v-hasPermi="['module_admin:forecast:export']"
        >导出</el-button>
        <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
      </div>
    </el-row>

    <!-- 搜索表单 -->
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch && !showDashboard" label-width="68px">
      <el-form-item label="产品 ID" prop="productId">
        <el-input
          v-model="queryParams.productId"
          placeholder="请输入产品 ID"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="区域代码" prop="regionCode">
        <el-input
          v-model="queryParams.regionCode"
          placeholder="请输入区域代码"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="预测日期" prop="forecastDate">
        <el-date-picker
          v-model="queryParams.forecastDate"
          type="date"
          value-format="yyyy-MM-dd"
          placeholder="请选择日期"
          clearable
        />
      </el-form-item>
      <el-form-item label="置信度" prop="confidenceLevel">
        <el-input
          v-model="queryParams.confidenceLevel"
          placeholder="请输入置信度"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="模型版本" prop="modelVersion">
        <el-input
          v-model="queryParams.modelVersion"
          placeholder="请输入模型版本"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 数据表格 -->
    <el-table v-loading="loading" :data="forecastList" @selection-change="handleSelectionChange" v-show="!showDashboard">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="ID" align="center" prop="id" width="80" />
      <el-table-column label="产品 ID" align="center" prop="productId" />
      <el-table-column label="区域代码" align="center" prop="regionCode" />
      <el-table-column label="预测日期" align="center" prop="forecastDate" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.forecastDate, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="预测销售额 (元)" align="center" prop="predictedAmount">
        <template slot-scope="scope">
          <span>{{ formatCurrency(scope.row.predictedAmount) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="置信度" align="center" prop="confidenceLevel">
        <template slot-scope="scope">
          <el-tag :type="getConfidenceTagType(scope.row.confidenceLevel)">{{ scope.row.confidenceLevel }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="模型版本" align="center" prop="modelVersion" />
      <el-table-column label="创建时间" align="center" prop="createdAt" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.createdAt, '{y}-{m}-{d} {h}:{i}:{s}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width" width="200">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['module_admin:forecast:edit']"
          >修改</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['module_admin:forecast:remove']"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0 && !showDashboard"
      :total="total"
      :page.sync="queryParams.pageNum"
      :limit.sync="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="产品 ID" prop="productId">
          <el-input v-model="form.productId" placeholder="请输入产品 ID" />
        </el-form-item>
        <el-form-item label="区域代码" prop="regionCode">
          <el-input v-model="form.regionCode" placeholder="请输入区域代码" />
        </el-form-item>
        <el-form-item label="预测日期" prop="forecastDate">
          <el-date-picker clearable
            v-model="form.forecastDate"
            type="date"
            value-format="yyyy-MM-dd"
            placeholder="请选择日期">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="预测销售额" prop="predictedAmount">
          <el-input-number v-model="form.predictedAmount" :min="0" :precision="2" step="100" style="width: 100%;" placeholder="请输入金额" />
        </el-form-item>
        <el-form-item label="置信度 (0-100)" prop="confidenceLevel">
          <el-slider v-model="form.confidenceLevel" :min="0" :max="100" show-input></el-slider>
        </el-form-item>
        <el-form-item label="模型版本" prop="modelVersion">
          <el-input v-model="form.modelVersion" placeholder="请输入模型版本" />
        </el-form-item>
      </el-form>
      <template slot="footer">
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { listForecast, getForecast, delForecast, addForecast, updateForecast } from "@/api/module_admin/forecast";
import * as echarts from 'echarts';

export default {
  name: "Forecast",
  data() {
    return {
      // 驾驶舱控制
      showDashboard: false,
      charts: {
        trend: null,
        region: null,
        confidence: null
      },
      // 驾驶舱统计数据
      totalPredictedAmount: 0,
      averageConfidence: 0,
      uniqueRegions: 0,
      modelVersionsCount: 0,
      latestModelVersion: '',
      
      // 原有数据
      loading: true,
      ids: [],
      single: true,
      multiple: true,
      showSearch: true,
      total: 0,
      forecastList: [],
      title: "",
      open: false,
      activeTabName: 'basic',
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        productId: null,
        regionCode: null,
        forecastDate: null,
        predictedAmount: null,
        confidenceLevel: null,
        modelVersion: null,
        createdAt: null,
        updatedAt: null,
      },
      form: {},
      rules: {
        productId: [
          { required: true, message: "产品 ID 不能为空", trigger: "blur" }
        ],
        regionCode: [
          { required: true, message: "区域代码不能为空", trigger: "blur" }
        ],
        forecastDate: [
          { required: true, message: "预测日期不能为空", trigger: "blur" }
        ],
        predictedAmount: [
          { required: true, message: "预测销售额不能为空", trigger: "blur" }
        ],
        confidenceLevel: [
          { required: true, message: "置信度不能为空", trigger: "blur" }
        ],
      }
    };
  },
  created() {
    this.getList();
  },
  mounted() {
    window.addEventListener('resize', this.handleResize);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
    this.disposeCharts();
  },
  methods: {
    /** 切换驾驶舱/列表视图 */
    toggleDashboard() {
      this.showDashboard = !this.showDashboard;
      if (this.showDashboard) {
        this.$nextTick(() => {
          this.calculateDashboardMetrics();
          this.initCharts();
        });
      } else {
        this.disposeCharts();
      }
    },
    
    /** 计算驾驶舱指标 */
    calculateDashboardMetrics() {
      if (!this.forecastList || this.forecastList.length === 0) {
        this.totalPredictedAmount = 0;
        this.averageConfidence = 0;
        this.uniqueRegions = 0;
        this.modelVersionsCount = 0;
        this.latestModelVersion = '';
        return;
      }

      // 总销售额
      this.totalPredictedAmount = this.forecastList.reduce((sum, item) => sum + (parseFloat(item.predictedAmount) || 0), 0);
      
      // 平均置信度
      const validConfidence = this.forecastList.filter(item => item.confidenceLevel !== null && item.confidenceLevel !== undefined);
      this.averageConfidence = validConfidence.length > 0 
        ? (validConfidence.reduce((sum, item) => sum + parseFloat(item.confidenceLevel), 0) / validConfidence.length).toFixed(1)
        : 0;
      
      // 唯一区域数
      const regions = new Set(this.forecastList.map(item => item.regionCode));
      this.uniqueRegions = regions.size;
      
      // 模型版本统计
      const versions = new Set(this.forecastList.map(item => item.modelVersion));
      this.modelVersionsCount = versions.size;
      
      // 最新模型版本 (简单取最后一个非空)
      const validVersions = this.forecastList.map(item => item.modelVersion).filter(v => v);
      this.latestModelVersion = validVersions.length > 0 ? validVersions[validVersions.length - 1] : '';
    },
    
    /** 初始化图表 */
    initCharts() {
      this.$nextTick(() => {
        this.initTrendChart();
        this.initRegionChart();
        this.initConfidenceChart();
      });
    },
    
    /** 销毁图表 */
    disposeCharts() {
      Object.values(this.charts).forEach(chart => {
        if (chart) chart.dispose();
      });
      this.charts = { trend: null, region: null, confidence: null };
    },
    
    /** 窗口大小变化处理 */
    handleResize() {
      Object.values(this.charts).forEach(chart => {
        if (chart) chart.resize();
      });
    },
    
    /** 刷新图表 */
    refreshCharts() {
      this.calculateDashboardMetrics();
      this.disposeCharts();
      this.initCharts();
    },
    
    /** 初始化趋势图 */
    initTrendChart() {
      const chartDom = this.$refs.trendChart;
      if (!chartDom) return;
      
      this.charts.trend = echarts.init(chartDom);
      
      // 按日期分组汇总销售额
      const dateMap = {};
      this.forecastList.forEach(item => {
        const date = item.forecastDate;
        if (!dateMap[date]) dateMap[date] = 0;
        dateMap[date] += parseFloat(item.predictedAmount) || 0;
      });
      
      const dates = Object.keys(dateMap).sort();
      const values = dates.map(date => dateMap[date]);
      
      const option = {
        tooltip: {
          trigger: 'axis',
          formatter: '{b}: ¥{c}'
        },
        xAxis: {
          type: 'category',
          data: dates,
          axisLabel: { rotate: 45 }
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: value => '¥' + (value / 10000).toFixed(1) + '万'
          }
        },
        series: [{
          data: values,
          type: 'line',
          smooth: true,
          areaStyle: {
            opacity: 0.3
          },
          itemStyle: {
            color: '#409EFF'
          }
        }]
      };
      
      this.charts.trend.setOption(option);
    },
    
    /** 初始化区域分布图 */
    initRegionChart() {
      const chartDom = this.$refs.regionChart;
      if (!chartDom) return;
      
      this.charts.region = echarts.init(chartDom);
      
      // 按区域分组汇总销售额
      const regionMap = {};
      this.forecastList.forEach(item => {
        const region = item.regionCode || '未知';
        if (!regionMap[region]) regionMap[region] = 0;
        regionMap[region] += parseFloat(item.predictedAmount) || 0;
      });
      
      const data = Object.entries(regionMap).map(([name, value]) => ({ name, value }));
      
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: ¥{c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          type: 'scroll'
        },
        series: [{
          name: '区域销售',
          type: 'pie',
          radius: '50%',
          data: data,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          },
          label: {
            formatter: '{b}: ¥{c}'
          }
        }]
      };
      
      this.charts.region.setOption(option);
    },
    
    /** 初始化置信度分布图 */
    initConfidenceChart() {
      const chartDom = this.$refs.confidenceChart;
      if (!chartDom) return;
      
      this.charts.confidence = echarts.init(chartDom);
      
      // 分箱统计置信度分布 (0-20, 20-40, 40-60, 60-80, 80-100)
      const bins = [0, 0, 0, 0, 0];
      const binLabels = ['0-20', '20-40', '40-60', '60-80', '80-100'];
      
      this.forecastList.forEach(item => {
        const level = parseFloat(item.confidenceLevel);
        if (!isNaN(level)) {
          const index = Math.min(Math.floor(level / 20), 4);
          bins[index]++;
        }
      });
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' }
        },
        xAxis: {
          type: 'category',
          data: binLabels,
          name: '置信度区间'
        },
        yAxis: {
          type: 'value',
          name: '记录数量'
        },
        series: [{
          data: bins,
          type: 'bar',
          barWidth: '60%',
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#83bff6' },
              { offset: 0.5, color: '#188df0' },
              { offset: 1, color: '#188df0' }
            ])
          }
        }]
      };
      
      this.charts.confidence.setOption(option);
    },
    
    /** 格式化货币 */
    formatCurrency(value) {
      if (value === null || value === undefined) return '0.00';
      return '¥' + parseFloat(value).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
    
    /** 获取置信度标签类型 */
    getConfidenceTagType(level) {
      if (level >= 80) return 'success';
      if (level >= 60) return 'primary';
      if (level >= 40) return 'warning';
      return 'danger';
    },
    
    /** 查询列表 */
    getList() {
      this.loading = true;
      listForecast(this.queryParams).then(response => {
        this.forecastList = response.rows;
        this.total = response.total;
        this.loading = false;
        // 如果在驾驶舱模式，刷新数据
        if (this.showDashboard) {
          this.$nextTick(() => {
            this.calculateDashboardMetrics();
            this.refreshCharts();
          });
        }
      });
    },
    cancel() {
      this.open = false;
      this.reset();
    },
    reset() {
      this.form = {
        id: null,
        productId: null,
        regionCode: null,
        forecastDate: null,
        predictedAmount: null,
        confidenceLevel: 50,
        modelVersion: null,
        createdAt: null,
        updatedAt: null,
      };
      this.resetForm("form");
    },
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    resetQuery() {
      this.resetForm("queryForm");
      this.handleQuery();
    },
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.id);
      this.single = selection.length != 1;
      this.multiple = !selection.length;
    },
    handleAdd() {
      this.reset();
      this.activeTabName = 'basic';
      this.open = true;
      this.title = "添加销售预测";
    },
    handleUpdate(row) {
      this.reset();
      this.activeTabName = 'basic';
      const id = row.id || this.ids;
      getForecast(id).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改销售预测";
      });
    },
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          if (this.form.id != null) {
            updateForecast(this.form).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addForecast(this.form).then(response => {
              this.$modal.msgSuccess("新增成功");
              this.open = false;
              this.getList();
            });
          }
        }
      });
    },
    handleDelete(row) {
      const ids = row.id || this.ids;
      this.$modal.confirm('是否确认删除编号为"' + ids + '"的数据项？').then(function() {
        return delForecast(ids);
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {});
    },
    handleExport() {
      this.download('module_admin/forecast/export', {
        ...this.queryParams
      }, `forecast_${new Date().getTime()}.xlsx`);
    },
    renderField(insert, edit) {
      return this.form.id == null ? insert : edit;
    }
  },
};
</script>

<style scoped>
.dashboard-container {
  background-color: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
}

.metric-card {
  text-align: center;
  transition: all 0.3s;
}

.metric-card:hover {
  transform: translateY(-5px);
}

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  color: #909399;
  font-size: 14px;
}

.metric-title {
  font-weight: bold;
}

.metric-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  margin: 10px 0;
}

.metric-trend {
  font-size: 13px;
  color: #606266;
}

.trend-up {
  color: #67C23A;
  margin-right: 5px;
}

.trend-down {
  color: #F56C6C;
  margin-right: 5px;
}

.trend-stable {
  color: #E6A23C;
  margin-right: 5px;
}

.trend-text {
  color: #409EFF;
}

.chart-card {
  height: 100%;
}

.chart-card .el-card__header {
  padding: 15px 20px;
  border-bottom: 1px solid #EBEEF5;
  box-sizing: border-box;
  background-color: #fafafa;
}

/* 优化表格样式 */
.el-table {
  font-size: 13px;
}

.el-table .cell {
  padding: 8px 0;
}

/* 优化表单样式 */
.el-form-item__label {
  font-weight: bold;
}

/* 响应式调整 */
@media screen and (max-width: 768px) {
  .metric-value {
    font-size: 20px;
  }
  
  .dashboard-container .el-col {
    margin-bottom: 15px;
  }
}
</style>