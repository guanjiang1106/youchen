<template>
  <div class="modern-dashboard">
    <!-- 欢迎横幅 -->
    <div class="welcome-banner gradient-bg">
      <div class="banner-content">
        <div class="welcome-text">
          <h1 class="greeting">{{ greeting }}，{{ userName }}</h1>
          <p class="subtitle">{{ currentDate }} | 今天也要加油哦 💪</p>
        </div>
        <div class="quick-actions">
          <button class="action-btn" @click="handleQuickAction('create')">
            <i class="el-icon-plus"></i>
            <span>新建</span>
          </button>
          <button class="action-btn" @click="handleQuickAction('search')">
            <i class="el-icon-search"></i>
            <span>搜索</span>
          </button>
          <button class="action-btn" @click="handleQuickAction('settings')">
            <i class="el-icon-setting"></i>
            <span>设置</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 数据统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card" v-for="(stat, index) in stats" :key="index" :style="{ animationDelay: `${index * 0.1}s` }">
        <div class="stat-icon" :style="{ background: stat.gradient }">
          <i :class="stat.icon"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
          <div class="stat-trend" :class="stat.trend > 0 ? 'up' : 'down'">
            <i :class="stat.trend > 0 ? 'el-icon-top' : 'el-icon-bottom'"></i>
            <span>{{ Math.abs(stat.trend) }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 图表和列表区域 -->
    <div class="content-grid">
      <!-- 图表区域 -->
      <div class="chart-section">
        <div class="modern-card">
          <div class="card-header">
            <h3 class="card-title">数据趋势</h3>
            <div class="card-actions">
              <button class="icon-btn" @click="refreshChart">
                <i class="el-icon-refresh"></i>
              </button>
              <button class="icon-btn">
                <i class="el-icon-more"></i>
              </button>
            </div>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <div class="chart-placeholder">
                <i class="el-icon-data-line" style="font-size: 48px; color: #dcdfe6; margin-bottom: 16px;"></i>
                <p style="color: #909399; font-size: 14px;">数据趋势图表</p>
                <p style="color: #c0c4cc; font-size: 12px;">可集成 ECharts 展示数据趋势</p>
              </div>
            </div>
          </div>
        </div>

        <div class="modern-card">
          <div class="card-header">
            <h3 class="card-title">分类统计</h3>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <div class="chart-placeholder">
                <i class="el-icon-pie-chart" style="font-size: 48px; color: #dcdfe6; margin-bottom: 16px;"></i>
                <p style="color: #909399; font-size: 14px;">分类统计图表</p>
                <p style="color: #c0c4cc; font-size: 12px;">可集成 ECharts 展示分类数据</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 列表区域 -->
      <div class="list-section">
        <div class="modern-card">
          <div class="card-header">
            <h3 class="card-title">最近活动</h3>
            <a href="javascript:void(0)" class="view-all" @click="viewAllActivities">查看全部 →</a>
          </div>
          <div class="card-body">
            <div class="activity-list">
              <div class="activity-item" v-for="(activity, index) in activities" :key="index">
                <div class="activity-icon" :style="{ background: activity.color }">
                  <i :class="activity.icon"></i>
                </div>
                <div class="activity-content">
                  <div class="activity-title">{{ activity.title }}</div>
                  <div class="activity-time">{{ activity.time }}</div>
                </div>
                <div class="activity-status" :class="activity.status">
                  {{ activity.statusText }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="modern-card">
          <div class="card-header">
            <h3 class="card-title">待办事项</h3>
          </div>
          <div class="card-body">
            <div class="todo-list">
              <div class="todo-item" v-for="(todo, index) in todos" :key="index">
                <el-checkbox v-model="todo.completed" @change="handleTodoChange(todo)">
                  <span :class="{ completed: todo.completed }">{{ todo.text }}</span>
                </el-checkbox>
                <span class="todo-priority" :class="todo.priority">{{ todo.priority }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getDashboardStats, getRecentActivities } from '@/api/dashboard'

export default {
  name: 'ModernDashboard',
  data() {
    return {
      loading: false,
      stats: [
        {
          icon: 'el-icon-user',
          value: '0',
          label: '总用户数',
          trend: 0,
          gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        },
        {
          icon: 'el-icon-document',
          value: '0',
          label: '今日操作',
          trend: 0,
          gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
        },
        {
          icon: 'el-icon-s-data',
          value: '0',
          label: '今日登录',
          trend: 0,
          gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
        },
        {
          icon: 'el-icon-star-on',
          value: '0%',
          label: '登录成功率',
          trend: 0,
          gradient: 'linear-gradient(135deg, #ffd89b 0%, #ff6b6b 100%)'
        }
      ],
      activities: [],
      todos: [
        { text: '查看系统日志', completed: false, priority: 'high' },
        { text: '检查用户反馈', completed: false, priority: 'medium' },
        { text: '更新系统配置', completed: false, priority: 'high' },
        { text: '数据备份', completed: false, priority: 'low' }
      ]
    };
  },
  computed: {
    userName() {
      return this.$store.state.user.name || '管理员';
    },
    greeting() {
      const hour = new Date().getHours();
      if (hour < 12) return '早上好';
      if (hour < 18) return '下午好';
      return '晚上好';
    },
    currentDate() {
      const date = new Date();
      const options = { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' };
      return date.toLocaleDateString('zh-CN', options);
    }
  },
  mounted() {
    this.loadDashboardData();
  },
  methods: {
    async loadDashboardData() {
      this.loading = true;
      try {
        // 加载统计数据
        await this.loadStats();
        // 加载最近活动
        await this.loadActivities();
      } catch (error) {
        console.error('加载首页数据失败:', error);
        this.$message.error('加载数据失败');
      } finally {
        this.loading = false;
      }
    },
    async loadStats() {
      try {
        const response = await getDashboardStats();
        if (response.code === 200 && response.data) {
          const data = response.data;
          
          // 更新统计卡片数据
          this.stats[0].value = this.formatNumber(data.totalUsers);
          this.stats[0].trend = data.userGrowth || 0;
          
          this.stats[1].value = this.formatNumber(data.todayLogs);
          this.stats[1].trend = data.logGrowth || 0;
          
          this.stats[2].value = this.formatNumber(data.todayLogins);
          this.stats[2].trend = data.loginGrowth || 0;
          
          this.stats[3].value = `${data.successRate}%`;
          this.stats[3].trend = data.successRateChange || 0;
        }
      } catch (error) {
        console.error('加载统计数据失败:', error);
      }
    },
    async loadActivities() {
      try {
        const response = await getRecentActivities();
        if (response.code === 200 && response.data) {
          this.activities = response.data;
        }
      } catch (error) {
        console.error('加载活动数据失败:', error);
      }
    },
    formatNumber(num) {
      if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'k';
      }
      return num.toString();
    },
    handleQuickAction(action) {
      const actionMap = {
        'create': () => {
          this.$router.push('/system/user');
        },
        'search': () => {
          this.$message.info('搜索功能开发中');
        },
        'settings': () => {
          this.$router.push('/system/config');
        }
      };
      
      if (actionMap[action]) {
        actionMap[action]();
      }
    },
    refreshChart() {
      this.loadDashboardData();
      this.$message.success('数据已刷新');
    },
    handleTodoChange(todo) {
      this.$message.success(todo.completed ? '任务已完成' : '任务未完成');
    },
    viewAllActivities() {
      // 跳转到操作日志页面
      this.$router.push('/monitor/operlog');
    },
    initCharts() {
      // 这里可以集成 ECharts 或其他图表库
      console.log('初始化图表');
    }
  }
};
</script>

<style lang="scss" scoped>
.modern-dashboard {
  padding: 24px;
  background: #f5f7fa;
  min-height: 100vh;
}

// 欢迎横幅
.welcome-banner {
  border-radius: 20px;
  padding: 40px;
  margin-bottom: 24px;
  color: #fff;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  animation: fadeIn 0.6s ease-out;

  .banner-content {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .welcome-text {
      .greeting {
        font-size: 32px;
        font-weight: 700;
        margin: 0 0 8px 0;
      }

      .subtitle {
        font-size: 16px;
        margin: 0;
        opacity: 0.9;
      }
    }

    .quick-actions {
      display: flex;
      gap: 12px;

      .action-btn {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        padding: 12px 24px;
        color: #fff;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 8px;

        i {
          font-size: 18px;
        }

        &:hover {
          background: rgba(255, 255, 255, 0.3);
          transform: translateY(-2px);
        }
      }
    }
  }
}

.gradient-bg {
  background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
  background-size: 400% 400%;
  animation: gradient 15s ease infinite;
}

@keyframes gradient {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

// 统计卡片网格
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.stat-card {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  animation: slideUp 0.6s ease-out;
  animation-fill-mode: both;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }

  .stat-icon {
    width: 64px;
    height: 64px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 28px;
  }

  .stat-content {
    flex: 1;

    .stat-value {
      font-size: 28px;
      font-weight: 700;
      color: #2c3e50;
      margin-bottom: 4px;
    }

    .stat-label {
      font-size: 14px;
      color: #7f8c8d;
      margin-bottom: 8px;
    }

    .stat-trend {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 13px;
      font-weight: 600;
      padding: 4px 8px;
      border-radius: 6px;

      &.up {
        color: #27ae60;
        background: rgba(39, 174, 96, 0.1);
      }

      &.down {
        color: #e74c3c;
        background: rgba(231, 76, 60, 0.1);
      }
    }
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

// 内容网格
.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.chart-section,
.list-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

// 现代卡片
.modern-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
  animation: fadeIn 0.6s ease-out;

  &:hover {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
  }

  .card-header {
    padding: 20px 24px;
    border-bottom: 1px solid #f0f0f0;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .card-title {
      font-size: 18px;
      font-weight: 600;
      color: #2c3e50;
      margin: 0;
    }

    .card-actions {
      display: flex;
      gap: 8px;

      .icon-btn {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        border: none;
        background: #f5f7fa;
        color: #7f8c8d;
        cursor: pointer;
        transition: all 0.3s ease;

        &:hover {
          background: #667eea;
          color: #fff;
        }
      }
    }

    .view-all {
      color: #667eea;
      font-size: 14px;
      text-decoration: none;
      transition: all 0.3s ease;

      &:hover {
        color: #764ba2;
      }
    }
  }

  .card-body {
    padding: 24px;
  }
}

// 图表容器
.chart-container {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  
  .chart-placeholder {
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
}

// 活动列表
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 16px;

  .activity-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px;
    border-radius: 12px;
    transition: all 0.3s ease;

    &:hover {
      background: #f8f9fa;
    }

    .activity-icon {
      width: 48px;
      height: 48px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-size: 20px;
    }

    .activity-content {
      flex: 1;

      .activity-title {
        font-size: 14px;
        font-weight: 500;
        color: #2c3e50;
        margin-bottom: 4px;
      }

      .activity-time {
        font-size: 12px;
        color: #95a5a6;
      }
    }

    .activity-status {
      padding: 4px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 500;

      &.success {
        color: #27ae60;
        background: rgba(39, 174, 96, 0.1);
      }

      &.info {
        color: #3498db;
        background: rgba(52, 152, 219, 0.1);
      }

      &.warning {
        color: #f39c12;
        background: rgba(243, 156, 18, 0.1);
      }
    }
  }
}

// 待办列表
.todo-list {
  display: flex;
  flex-direction: column;
  gap: 12px;

  .todo-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    border-radius: 8px;
    transition: all 0.3s ease;

    &:hover {
      background: #f8f9fa;
    }

    ::v-deep .el-checkbox {
      flex: 1;

      .el-checkbox__label {
        font-size: 14px;
        color: #2c3e50;

        .completed {
          text-decoration: line-through;
          color: #95a5a6;
        }
      }

      .el-checkbox__input.is-checked .el-checkbox__inner {
        background-color: #667eea;
        border-color: #667eea;
      }
    }

    .todo-priority {
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;

      &.high {
        color: #e74c3c;
        background: rgba(231, 76, 60, 0.1);
      }

      &.medium {
        color: #f39c12;
        background: rgba(243, 156, 18, 0.1);
      }

      &.low {
        color: #95a5a6;
        background: rgba(149, 165, 166, 0.1);
      }
    }
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

// 响应式设计
@media (max-width: 1200px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .modern-dashboard {
    padding: 16px;
  }

  .welcome-banner {
    padding: 24px;

    .banner-content {
      flex-direction: column;
      gap: 20px;
      align-items: flex-start;

      .welcome-text .greeting {
        font-size: 24px;
      }

      .quick-actions {
        width: 100%;
        justify-content: space-between;

        .action-btn {
          flex: 1;
          justify-content: center;
        }
      }
    }
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
