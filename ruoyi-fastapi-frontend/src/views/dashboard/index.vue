<template>
  <div class="dashboard-container">
    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <div class="welcome-left">
        <a-avatar size="large" :src="currentUser.avatar" />
        <div class="welcome-info">
          <div class="welcome-title">
            {{ getGreeting() }}，{{ currentUser.name }}
          </div>
          <div class="welcome-subtitle">{{ currentUser.title }}</div>
        </div>
      </div>
      <div class="welcome-right">
        <span class="current-time">{{ currentTime }}</span>
      </div>
    </div>

    <!-- 数据统计卡片 -->
    <a-row :gutter="16" class="stats-row">
      <a-col :xs="24" :sm="12" :lg="6">
        <a-card class="stat-card" :bordered="false">
          <div class="stat-content">
            <div class="stat-icon user-icon">
              <a-icon type="user" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.userCount }}</div>
              <div class="stat-label">用户总数</div>
            </div>
          </div>
        </a-card>
      </a-col>
      <a-col :xs="24" :sm="12" :lg="6">
        <a-card class="stat-card" :bordered="false">
          <div class="stat-content">
            <div class="stat-icon visit-icon">
              <a-icon type="eye" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.visitCount }}</div>
              <div class="stat-label">今日访问</div>
            </div>
          </div>
        </a-card>
      </a-col>
      <a-col :xs="24" :sm="12" :lg="6">
        <a-card class="stat-card" :bordered="false">
          <div class="stat-content">
            <div class="stat-icon order-icon">
              <a-icon type="file-text" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.orderCount }}</div>
              <div class="stat-label">订单数量</div>
            </div>
          </div>
        </a-card>
      </a-col>
      <a-col :xs="24" :sm="12" :lg="6">
        <a-card class="stat-card" :bordered="false">
          <div class="stat-content">
            <div class="stat-icon revenue-icon">
              <a-icon type="dollar" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.revenue }}</div>
              <div class="stat-label">营收金额</div>
            </div>
          </div>
        </a-card>
      </a-col>
    </a-row>

    <!-- 快捷入口 -->
    <a-card title="快捷入口" :bordered="false" class="quick-links-card">
      <div class="quick-links">
        <a-button type="link" @click="navigateTo('/system/user')">
          <a-icon type="user" />
          用户管理
        </a-button>
        <a-button type="link" @click="navigateTo('/system/role')">
          <a-icon type="team" />
          角色管理
        </a-button>
        <a-button type="link" @click="navigateTo('/system/menu')">
          <a-icon type="menu" />
          菜单管理
        </a-button>
        <a-button type="link" @click="navigateTo('/system/dept')">
          <a-icon type="apartment" />
          部门管理
        </a-button>
        <a-button type="link" @click="navigateTo('/system/post')">
          <a-icon type="idcard" />
          岗位管理
        </a-button>
        <a-button type="link" @click="navigateTo('/system/dict')">
          <a-icon type="book" />
          字典管理
        </a-button>
        <a-button type="link" @click="navigateTo('/monitor/operlog')">
          <a-icon type="file-search" />
          操作日志
        </a-button>
        <a-button type="link" @click="navigateTo('/monitor/logininfor')">
          <a-icon type="login" />
          登录日志
        </a-button>
      </div>
    </a-card>

    <!-- 系统信息 -->
    <a-row :gutter="16" class="info-row">
      <a-col :xs="24" :lg="12">
        <a-card title="系统信息" :bordered="false">
          <div class="info-list">
            <div class="info-item">
              <span class="info-label">系统版本：</span>
              <span class="info-value">RuoYi-FastAPI v1.9.0</span>
            </div>
            <div class="info-item">
              <span class="info-label">后端框架：</span>
              <span class="info-value">FastAPI + SQLAlchemy</span>
            </div>
            <div class="info-item">
              <span class="info-label">前端框架：</span>
              <span class="info-value">Vue 2.x + Ant Design Vue</span>
            </div>
            <div class="info-item">
              <span class="info-label">数据库：</span>
              <span class="info-value">MySQL / PostgreSQL</span>
            </div>
          </div>
        </a-card>
      </a-col>
      <a-col :xs="24" :lg="12">
        <a-card title="最近操作" :bordered="false">
          <a-list
            :data-source="recentActions"
            :loading="loading"
            size="small"
          >
            <a-list-item slot="renderItem" slot-scope="item">
              <a-list-item-meta>
                <div slot="title">{{ item.title }}</div>
                <div slot="description">{{ item.time }}</div>
              </a-list-item-meta>
            </a-list-item>
          </a-list>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import { Avatar, Button, Card, Col, Icon, List, Row } from "ant-design-vue";
import "ant-design-vue/dist/antd.css";
import Vue from "vue";
import { mapGetters } from "vuex";

Vue.component(Avatar.name, Avatar);
Vue.component(Button.name, Button);
Vue.component(Card.name, Card);
Vue.component(Col.name, Col);
Vue.component(Icon.name, Icon);
Vue.component(List.name, List);
Vue.component(List.Item.name, List.Item);
Vue.component(List.Item.Meta.name, List.Item.Meta);
Vue.component(Row.name, Row);

export default {
  name: "DashBoard",
  data() {
    return {
      currentTime: "",
      stats: {
        userCount: 0,
        visitCount: 0,
        orderCount: 0,
        revenue: "¥0",
      },
      recentActions: [],
      loading: false,
      timeInterval: null,
    };
  },
  computed: {
    ...mapGetters(["name", "avatar"]),
    currentUser() {
      return {
        name: this.name || "管理员",
        avatar:
          this.avatar ||
          "https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png",
        title: "系统管理员",
      };
    },
  },
  mounted() {
    this.updateTime();
    this.timeInterval = setInterval(this.updateTime, 1000);
    this.loadDashboardData();
  },
  beforeDestroy() {
    if (this.timeInterval) {
      clearInterval(this.timeInterval);
    }
  },
  methods: {
    getGreeting() {
      const hour = new Date().getHours();
      if (hour < 6) return "凌晨好";
      if (hour < 9) return "早上好";
      if (hour < 12) return "上午好";
      if (hour < 14) return "中午好";
      if (hour < 17) return "下午好";
      if (hour < 19) return "傍晚好";
      if (hour < 22) return "晚上好";
      return "夜深了";
    },
    updateTime() {
      const now = new Date();
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, "0");
      const date = String(now.getDate()).padStart(2, "0");
      const hours = String(now.getHours()).padStart(2, "0");
      const minutes = String(now.getMinutes()).padStart(2, "0");
      const seconds = String(now.getSeconds()).padStart(2, "0");
      const weekDays = [
        "星期日",
        "星期一",
        "星期二",
        "星期三",
        "星期四",
        "星期五",
        "星期六",
      ];
      const weekDay = weekDays[now.getDay()];
      this.currentTime = `${year}-${month}-${date} ${hours}:${minutes}:${seconds} ${weekDay}`;
    },
    loadDashboardData() {
      // 这里可以调用实际的API获取数据
      // 示例：使用模拟数据
      this.loading = true;
      setTimeout(() => {
        this.stats = {
          userCount: 1234,
          visitCount: 5678,
          orderCount: 89,
          revenue: "¥12,345",
        };
        this.recentActions = [
          { title: "用户 admin 登录系统", time: "2分钟前" },
          { title: "新增用户 张三", time: "10分钟前" },
          { title: "修改角色权限", time: "30分钟前" },
          { title: "系统配置更新", time: "1小时前" },
          { title: "数据备份完成", time: "2小时前" },
        ];
        this.loading = false;
      }, 500);
    },
    navigateTo(path) {
      this.$router.push(path);
    },
  },
};
</script>

<style lang="less" scoped>
.dashboard-container {
  padding: 24px;
  background: #f0f2f5;
  min-height: calc(100vh - 64px);
}

.welcome-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 32px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

  .welcome-left {
    display: flex;
    align-items: center;
    gap: 20px;

    .welcome-info {
      color: white;

      .welcome-title {
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 8px;
      }

      .welcome-subtitle {
        font-size: 14px;
        opacity: 0.9;
      }
    }
  }

  .welcome-right {
    .current-time {
      color: white;
      font-size: 16px;
      font-weight: 500;
      opacity: 0.95;
    }
  }
}

.stats-row {
  margin-bottom: 24px;

  .stat-card {
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    transition: all 0.3s;

    &:hover {
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
      transform: translateY(-2px);
    }

    .stat-content {
      display: flex;
      align-items: center;
      gap: 16px;

      .stat-icon {
        width: 56px;
        height: 56px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        color: white;

        &.user-icon {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        &.visit-icon {
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }

        &.order-icon {
          background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }

        &.revenue-icon {
          background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        }
      }

      .stat-info {
        flex: 1;

        .stat-value {
          font-size: 28px;
          font-weight: 600;
          color: #262626;
          line-height: 1.2;
        }

        .stat-label {
          font-size: 14px;
          color: #8c8c8c;
          margin-top: 4px;
        }
      }
    }
  }
}

.quick-links-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  margin-bottom: 24px;

  .quick-links {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 8px;

    .ant-btn-link {
      height: auto;
      padding: 12px 16px;
      text-align: left;
      border-radius: 8px;
      transition: all 0.3s;
      color: #595959;

      &:hover {
        background: #f5f5f5;
        color: #1890ff;
      }

      i {
        margin-right: 8px;
        font-size: 16px;
      }
    }
  }
}

.info-row {
  .ant-card {
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    height: 100%;

    .info-list {
      .info-item {
        padding: 12px 0;
        border-bottom: 1px solid #f0f0f0;
        display: flex;
        justify-content: space-between;

        &:last-child {
          border-bottom: none;
        }

        .info-label {
          color: #8c8c8c;
          font-size: 14px;
        }

        .info-value {
          color: #262626;
          font-size: 14px;
          font-weight: 500;
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 16px;
  }

  .welcome-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;

    .welcome-right {
      width: 100%;
      text-align: right;
    }
  }

  .quick-links {
    grid-template-columns: repeat(2, 1fr) !important;
  }
}
</style>
