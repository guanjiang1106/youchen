<template>
  <div class="ui-showcase">
    <div class="showcase-header gradient-bg">
      <h1>🎨 现代化 UI 组件展示</h1>
      <p>宥辰开发平台 现代化设计系统</p>
    </div>

    <div class="showcase-content">
      <!-- 按钮展示 -->
      <section class="showcase-section">
        <h2 class="section-title">按钮组件</h2>
        <div class="modern-card">
          <div class="button-group">
            <el-button type="primary">主要按钮</el-button>
            <el-button type="success">成功按钮</el-button>
            <el-button type="warning">警告按钮</el-button>
            <el-button type="danger">危险按钮</el-button>
            <el-button type="info">信息按钮</el-button>
          </div>
          <div class="button-group">
            <button class="modern-btn primary">现代化主按钮</button>
            <button class="modern-btn secondary">现代化次按钮</button>
          </div>
        </div>
      </section>

      <!-- 输入框展示 -->
      <section class="showcase-section">
        <h2 class="section-title">输入框组件</h2>
        <div class="modern-card">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-input placeholder="Element UI 输入框" v-model="input1"></el-input>
            </el-col>
            <el-col :span="12">
              <input type="text" class="modern-input" placeholder="现代化输入框" v-model="input2" />
            </el-col>
          </el-row>
        </div>
      </section>

      <!-- 卡片展示 -->
      <section class="showcase-section">
        <h2 class="section-title">卡片组件</h2>
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="modern-card">
              <h3>标准卡片</h3>
              <p>这是一个现代化的卡片组件，具有圆角和阴影效果。</p>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="modern-card glass">
              <h3>玻璃态卡片</h3>
              <p>这是一个玻璃态效果的卡片，具有模糊背景。</p>
            </div>
          </el-col>
          <el-col :span="8">
            <el-card>
              <div slot="header">Element UI 卡片</div>
              <p>这是 Element UI 的卡片组件，已应用现代化样式。</p>
            </el-card>
          </el-col>
        </el-row>
      </section>

      <!-- 表格展示 -->
      <section class="showcase-section">
        <h2 class="section-title">表格组件</h2>
        <div class="modern-card">
          <el-table :data="tableData" style="width: 100%">
            <el-table-column prop="date" label="日期" width="180"></el-table-column>
            <el-table-column prop="name" label="姓名" width="180"></el-table-column>
            <el-table-column prop="address" label="地址"></el-table-column>
            <el-table-column label="操作" width="200">
              <template slot-scope="scope">
                <el-button size="mini" type="primary">编辑</el-button>
                <el-button size="mini" type="danger">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </section>

      <!-- 标签展示 -->
      <section class="showcase-section">
        <h2 class="section-title">标签组件</h2>
        <div class="modern-card">
          <div class="tag-group">
            <el-tag type="primary">主要标签</el-tag>
            <el-tag type="success">成功标签</el-tag>
            <el-tag type="warning">警告标签</el-tag>
            <el-tag type="danger">危险标签</el-tag>
            <el-tag type="info">信息标签</el-tag>
          </div>
        </div>
      </section>

      <!-- 表单展示 -->
      <section class="showcase-section">
        <h2 class="section-title">表单组件</h2>
        <div class="modern-card">
          <el-form :model="form" label-width="100px">
            <el-form-item label="用户名">
              <el-input v-model="form.username"></el-input>
            </el-form-item>
            <el-form-item label="密码">
              <el-input type="password" v-model="form.password"></el-input>
            </el-form-item>
            <el-form-item label="性别">
              <el-radio-group v-model="form.gender">
                <el-radio label="male">男</el-radio>
                <el-radio label="female">女</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="爱好">
              <el-checkbox-group v-model="form.hobbies">
                <el-checkbox label="reading">阅读</el-checkbox>
                <el-checkbox label="sports">运动</el-checkbox>
                <el-checkbox label="music">音乐</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item label="状态">
              <el-switch v-model="form.status"></el-switch>
            </el-form-item>
            <el-form-item>
              <el-button type="primary">提交</el-button>
              <el-button>取消</el-button>
            </el-form-item>
          </el-form>
        </div>
      </section>

      <!-- 消息提示展示 -->
      <section class="showcase-section">
        <h2 class="section-title">消息提示</h2>
        <div class="modern-card">
          <div class="button-group">
            <el-button @click="showMessage('success')">成功消息</el-button>
            <el-button @click="showMessage('warning')">警告消息</el-button>
            <el-button @click="showMessage('error')">错误消息</el-button>
            <el-button @click="showMessage('info')">信息消息</el-button>
          </div>
        </div>
      </section>

      <!-- 进度条展示 -->
      <section class="showcase-section">
        <h2 class="section-title">进度条</h2>
        <div class="modern-card">
          <el-progress :percentage="50"></el-progress>
          <el-progress :percentage="75" status="success"></el-progress>
          <el-progress :percentage="100" status="warning"></el-progress>
        </div>
      </section>

      <!-- 统计卡片展示 -->
      <section class="showcase-section">
        <h2 class="section-title">统计卡片</h2>
        <el-row :gutter="20">
          <el-col :span="6" v-for="(stat, index) in stats" :key="index">
            <div class="stat-card">
              <div class="stat-icon" :style="{ background: stat.gradient }">
                <i :class="stat.icon"></i>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ stat.value }}</div>
                <div class="stat-label">{{ stat.label }}</div>
              </div>
            </div>
          </el-col>
        </el-row>
      </section>

      <!-- 动画展示 -->
      <section class="showcase-section">
        <h2 class="section-title">动画效果</h2>
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="modern-card fade-in">
              <h3>淡入动画</h3>
              <p>fade-in</p>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="modern-card slide-in-right">
              <h3>滑入动画</h3>
              <p>slide-in-right</p>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="modern-card pulse">
              <h3>脉冲动画</h3>
              <p>pulse</p>
            </div>
          </el-col>
        </el-row>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UIShowcase',
  data() {
    return {
      input1: '',
      input2: '',
      form: {
        username: '',
        password: '',
        gender: 'male',
        hobbies: [],
        status: true
      },
      tableData: [
        {
          date: '2024-01-01',
          name: '张三',
          address: '上海市普陀区金沙江路 1518 弄'
        },
        {
          date: '2024-01-02',
          name: '李四',
          address: '上海市普陀区金沙江路 1517 弄'
        },
        {
          date: '2024-01-03',
          name: '王五',
          address: '上海市普陀区金沙江路 1519 弄'
        }
      ],
      stats: [
        {
          icon: 'el-icon-user',
          value: '1,234',
          label: '总用户数',
          gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        },
        {
          icon: 'el-icon-document',
          value: '5,678',
          label: '文档数量',
          gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
        },
        {
          icon: 'el-icon-s-data',
          value: '89.5%',
          label: '系统性能',
          gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
        },
        {
          icon: 'el-icon-star-on',
          value: '4.8',
          label: '用户评分',
          gradient: 'linear-gradient(135deg, #ffd89b 0%, #ff6b6b 100%)'
        }
      ]
    };
  },
  methods: {
    showMessage(type) {
      const messages = {
        success: '操作成功！',
        warning: '请注意检查！',
        error: '操作失败！',
        info: '这是一条提示信息'
      };
      this.$message({
        type: type,
        message: messages[type]
      });
    }
  }
};
</script>

<style lang="scss" scoped>
@import '@/assets/styles/modern-theme.scss';

.ui-showcase {
  min-height: 100vh;
  background: #f5f7fa;
}

.showcase-header {
  padding: 60px 40px;
  text-align: center;
  color: #fff;
  margin-bottom: 40px;

  h1 {
    font-size: 48px;
    font-weight: 700;
    margin: 0 0 16px 0;
  }

  p {
    font-size: 20px;
    margin: 0;
    opacity: 0.9;
  }
}

.showcase-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 40px 60px;
}

.showcase-section {
  margin-bottom: 48px;

  .section-title {
    font-size: 28px;
    font-weight: 600;
    color: #2c3e50;
    margin: 0 0 24px 0;
    padding-bottom: 12px;
    border-bottom: 3px solid;
    border-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%) 1;
  }
}

.button-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 16px;

  &:last-child {
    margin-bottom: 0;
  }
}

.tag-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
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
    }
  }
}

@media (max-width: 768px) {
  .showcase-header {
    padding: 40px 20px;

    h1 {
      font-size: 32px;
    }

    p {
      font-size: 16px;
    }
  }

  .showcase-content {
    padding: 0 20px 40px;
  }

  .button-group {
    flex-direction: column;

    button {
      width: 100%;
    }
  }
}
</style>
