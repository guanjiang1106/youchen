<template>
  <div class="app-container guide-container">
    <el-card class="guide-card">
      <div slot="header" class="guide-header">
        <i class="el-icon-document"></i>
        <span>平台开发指南</span>
      </div>

      <el-tabs v-model="activeTab" type="border-card">
        <!-- 系统介绍 -->
        <el-tab-pane label="系统介绍" name="intro">
          <div class="guide-content">
            <h2>平台简介</h2>
            <p>宥辰开发平台(YouChen-FastAPI)是一套全部开源的快速开发平台，毫无保留给个人及企业免费使用。</p>
            
            <el-row :gutter="20" style="margin-top: 20px;">
              <el-col :span="8">
                <el-card shadow="hover" class="tech-card">
                  <div class="tech-icon">🎨</div>
                  <h3>前端技术</h3>
                  <ul>
                    <li>Vue 2.x</li>
                    <li>Element UI</li>
                    <li>Axios</li>
                    <li>Vuex</li>
                  </ul>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card shadow="hover" class="tech-card">
                  <div class="tech-icon">⚡</div>
                  <h3>后端技术</h3>
                  <ul>
                    <li>Python 3.10+</li>
                    <li>FastAPI</li>
                    <li>SQLAlchemy</li>
                    <li>MySQL 5.7+ / PostgreSQL 12+</li>
                    <li>Redis 5.0+</li>
                    <li>OAuth2 & JWT</li>
                  </ul>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card shadow="hover" class="tech-card">
                  <div class="tech-icon">📱</div>
                  <h3>移动端技术</h3>
                  <ul>
                    <li>uni-app</li>
                    <li>Vue 2.x</li>
                    <li>TailwindCSS</li>
                  </ul>
                </el-card>
              </el-col>
            </el-row>

            <h2 style="margin-top: 40px;">平台架构</h2>
            <el-card class="architecture-card">
              <el-row :gutter="20">
                <el-col :span="8">
                  <div class="arch-layer">
                    <h4>🖥️ 前端层</h4>
                    <p>ruoyi-fastapi-frontend</p>
                    <ul>
                      <li>Vue 管理后台</li>
                      <li>Element UI 组件</li>
                      <li>路由权限控制</li>
                    </ul>
                  </div>
                </el-col>
                <el-col :span="8">
                  <div class="arch-layer">
                    <h4>📱 移动端层</h4>
                    <p>ruoyi-fastapi-app</p>
                    <ul>
                      <li>uni-app 跨平台</li>
                      <li>H5 / 小程序</li>
                      <li>响应式设计</li>
                    </ul>
                  </div>
                </el-col>
                <el-col :span="8">
                  <div class="arch-layer">
                    <h4>⚙️ 后端层</h4>
                    <p>ruoyi-fastapi-backend</p>
                    <ul>
                      <li>FastAPI 框架</li>
                      <li>异步 ORM</li>
                      <li>RESTful API</li>
                    </ul>
                  </div>
                </el-col>
              </el-row>
            </el-card>

            <h2 style="margin-top: 40px;">目录结构说明</h2>
            <el-row :gutter="20">
              <el-col :span="12">
                <h3>📁 后端目录结构</h3>
                <el-card class="dir-card">
                  <pre><code>ruoyi-fastapi-backend/
├── common/              # 公共组件（禁止修改）
├── config/              # 配置文件（禁止修改）
├── exceptions/          # 异常处理（禁止修改）
├── middlewares/         # 中间件（禁止修改）
├── utils/               # 工具类（禁止修改）
├── module_admin/        # 系统管理模块（核心）
├── module_ai/           # AI 功能模块
├── module_task/         # 定时任务模块
├── module_generator/    # 代码生成器模块
├── module_business/     # 业务模块（新增代码放这里）
├── alembic/             # 数据库迁移
├── sql/                 # SQL 脚本
├── app.py               # 应用入口
└── server.py            # 服务启动</code></pre>
                </el-card>
              </el-col>
              <el-col :span="12">
                <h3>📁 前端目录结构</h3>
                <el-card class="dir-card">
                  <pre><code>ruoyi-fastapi-frontend/
├── public/              # 静态资源
├── src/
│   ├── api/            # API 接口
│   ├── assets/         # 资源文件
│   ├── components/     # 公共组件
│   ├── layout/         # 布局组件
│   ├── router/         # 路由配置
│   ├── store/          # Vuex 状态管理
│   ├── utils/          # 工具类
│   ├── views/          # 页面视图
│   │   ├── system/    # 系统管理页面
│   │   ├── tool/      # 系统工具页面
│   │   └── business/  # 业务页面（新增页面放这里）
│   ├── App.vue
│   └── main.js
└── package.json</code></pre>
                </el-card>
              </el-col>
            </el-row>

            <h2 style="margin-top: 40px;">核心功能模块</h2>
            <el-collapse v-model="activeModules" accordion>
              <el-collapse-item title="🔐 权限管理" name="auth">
                <ul>
                  <li><strong>用户管理：</strong>系统用户配置、角色分配、部门归属</li>
                  <li><strong>角色管理：</strong>角色菜单权限分配、数据范围权限划分</li>
                  <li><strong>菜单管理：</strong>系统菜单配置、操作权限、按钮权限标识</li>
                  <li><strong>部门管理：</strong>组织机构配置（公司、部门、小组）</li>
                  <li><strong>岗位管理：</strong>用户担任职务配置</li>
                </ul>
              </el-collapse-item>
              <el-collapse-item title="📊 系统监控" name="monitor">
                <ul>
                  <li><strong>在线用户：</strong>当前系统活跃用户状态监控</li>
                  <li><strong>服务监控：</strong>CPU、内存、磁盘、堆栈等信息监控</li>
                  <li><strong>缓存监控：</strong>Redis 缓存信息查询、命令统计</li>
                  <li><strong>操作日志：</strong>系统操作日志记录和查询</li>
                  <li><strong>登录日志：</strong>登录日志记录查询（含异常）</li>
                </ul>
              </el-collapse-item>
              <el-collapse-item title="🛠️ 系统工具" name="tools">
                <ul>
                  <li><strong>代码生成：</strong>一键生成前后端代码（Python、Vue、JS）</li>
                  <li><strong>表单构建：</strong>拖拽生成表单元素和 HTML 代码</li>
                  <li><strong>系统接口：</strong>自动生成 API 接口文档（Swagger）</li>
                  <li><strong>定时任务：</strong>在线任务调度（添加、修改、删除、执行日志）</li>
                </ul>
              </el-collapse-item>
              <el-collapse-item title="🤖 AI 功能" name="ai">
                <ul>
                  <li><strong>AI 模型管理：</strong>支持多种 AI 模型配置和切换</li>
                  <li><strong>AI 对话：</strong>智能对话功能</li>
                  <li><strong>AI 技能系统：</strong>可扩展的技能加载机制</li>
                  <li><strong>AI 辅助开发：</strong>自动生成代码、创建表结构</li>
                </ul>
              </el-collapse-item>
              <el-collapse-item title="⚙️ 系统配置" name="config">
                <ul>
                  <li><strong>字典管理：</strong>系统固定数据维护</li>
                  <li><strong>参数管理：</strong>系统动态参数配置</li>
                  <li><strong>通知公告：</strong>系统通知公告信息发布</li>
                </ul>
              </el-collapse-item>
            </el-collapse>

            <h2 style="margin-top: 40px;">特色功能</h2>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-card class="feature-highlight">
                  <h3>🤖 AI 辅助开发</h3>
                  <p>内置完整的 AI 开发规则，支持：</p>
                  <ul>
                    <li>自动创建数据库表</li>
                    <li>一键生成前后端代码</li>
                    <li>智能修改功能</li>
                    <li>保护框架完整性</li>
                    <li>极速开发（需求到功能只需几分钟）</li>
                  </ul>
                </el-card>
              </el-col>
              <el-col :span="12">
                <el-card class="feature-highlight">
                  <h3>🚀 代码生成器</h3>
                  <p>强大的代码生成能力：</p>
                  <ul>
                    <li>配置数据库表信息</li>
                    <li>一键生成完整 CRUD 代码</li>
                    <li>自动生成权限控制</li>
                    <li>支持下载或本地生成</li>
                    <li>模板可定制</li>
                  </ul>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>

        <!-- 开发说明 -->
        <el-tab-pane label="开发说明" name="development">
          <div class="guide-content">
            <h2>环境准备</h2>
            <el-row :gutter="20">
              <el-col :span="8">
                <el-card class="env-card">
                  <h3>🖥️ 前端环境</h3>
                  <ul>
                    <li>Node.js 14+</li>
                    <li>npm 或 yarn</li>
                  </ul>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card class="env-card">
                  <h3>⚙️ 后端环境</h3>
                  <ul>
                    <li>Python 3.10+</li>
                    <li>pip</li>
                    <li>MySQL 5.7+ 或 PostgreSQL 12+</li>
                    <li>Redis 5.0+</li>
                  </ul>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card class="env-card">
                  <h3>📱 移动端环境</h3>
                  <ul>
                    <li>Node.js 14+</li>
                    <li>yarn</li>
                    <li>HBuilderX（可选）</li>
                  </ul>
                </el-card>
              </el-col>
            </el-row>

            <h2 style="margin-top: 40px;">快速启动</h2>
            
            <h3>1. 克隆项目</h3>
            <el-card class="code-card">
              <pre><code>git clone https://github.com/guanjiang1106/youchen.git
cd youchen</code></pre>
            </el-card>

            <h3>2. 后端启动</h3>
            <el-steps :active="5" direction="vertical" style="margin: 20px 0;">
              <el-step title="安装依赖">
                <div slot="description">
                  <el-card class="code-card">
                    <pre><code># MySQL 用户
pip3 install -r requirements.txt

# PostgreSQL 用户
pip3 install -r requirements-pg.txt</code></pre>
                  </el-card>
                </div>
              </el-step>
              <el-step title="配置环境">
                <div slot="description">
                  <p>编辑 <code>.env.dev</code> 文件，配置数据库和 Redis</p>
                  <el-alert type="warning" :closable="false" show-icon style="margin-top: 10px;">
                    重要：确保 DB_TYPE 配置正确（mysql 或 postgresql）
                  </el-alert>
                </div>
              </el-step>
              <el-step title="创建数据库">
                <div slot="description">
                  <p>新建数据库 <code>youchen-fastapi</code>（默认名称，可修改）</p>
                </div>
              </el-step>
              <el-step title="导入 SQL">
                <div slot="description">
                  <ul>
                    <li>MySQL：运行 <code>sql/youchen-fastapi.sql</code></li>
                    <li>PostgreSQL：运行 <code>sql/youchen-fastapi-pg.sql</code></li>
                  </ul>
                </div>
              </el-step>
              <el-step title="启动服务">
                <div slot="description">
                  <el-card class="code-card">
                    <pre><code>python3 app.py --env=dev</code></pre>
                  </el-card>
                  <p style="margin-top: 10px;">访问：<a href="http://localhost:8000/docs" target="_blank">http://localhost:8000/docs</a></p>
                </div>
              </el-step>
            </el-steps>

            <h3>3. 前端启动</h3>
            <el-card class="code-card">
              <pre><code>cd ruoyi-fastapi-frontend
npm install
npm run dev</code></pre>
            </el-card>
            <p style="margin-top: 10px;">访问：<a href="http://localhost:80" target="_blank">http://localhost:80</a></p>
            <p>默认账号：<code>admin</code> / <code>admin123</code></p>

            <h3>4. 移动端启动（可选）</h3>
            <el-card class="code-card">
              <pre><code>cd ruoyi-fastapi-app
yarn
yarn dev:h5          # H5
yarn dev:mp-weixin   # 微信小程序</code></pre>
            </el-card>

            <h2 style="margin-top: 40px;">开发规范</h2>
            
            <el-alert
              title="核心原则：新增功能，不改框架！"
              type="error"
              :closable="false"
              show-icon
              style="margin-bottom: 20px;">
            </el-alert>

            <h3>禁止修改的核心文件</h3>
            <el-table :data="protectedFiles" border>
              <el-table-column prop="path" label="目录/文件" width="250"></el-table-column>
              <el-table-column prop="desc" label="说明"></el-table-column>
            </el-table>

            <h3 style="margin-top: 30px;">新增功能标准流程</h3>
            <el-timeline>
              <el-timeline-item timestamp="方式一：使用代码生成器（推荐）" placement="top">
                <el-card>
                  <ol>
                    <li>创建数据库表</li>
                    <li>导入表到代码生成器</li>
                    <li>配置字段信息</li>
                    <li>一键生成代码</li>
                    <li>生成菜单和权限</li>
                  </ol>
                  <p style="color: #67C23A; margin-top: 10px;">✅ 推荐：快速、规范、完整</p>
                </el-card>
              </el-timeline-item>
              <el-timeline-item timestamp="方式二：使用 AI 辅助开发" placement="top">
                <el-card>
                  <ol>
                    <li>描述需求给 AI</li>
                    <li>AI 自动创建表</li>
                    <li>AI 调用代码生成器</li>
                    <li>AI 配置菜单权限</li>
                  </ol>
                  <p style="color: #67C23A; margin-top: 10px;">✅ 推荐：极速、智能、零错误</p>
                </el-card>
              </el-timeline-item>
              <el-timeline-item timestamp="方式三：手动创建模块" placement="top">
                <el-card>
                  <ol>
                    <li>在 <code>module_business/</code> 创建模块目录</li>
                    <li>按照标准结构创建文件（controller/service/dao/entity）</li>
                    <li>参考现有模块编写代码</li>
                    <li>手动配置菜单和权限</li>
                  </ol>
                  <p style="color: #E6A23C; margin-top: 10px;">⚠️ 适用：复杂业务逻辑、特殊需求</p>
                </el-card>
              </el-timeline-item>
            </el-timeline>

            <h3 style="margin-top: 30px;">代码规范要点</h3>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-card class="rule-card">
                  <h4>命名规范</h4>
                  <ul>
                    <li>类名：PascalCase（大驼峰）</li>
                    <li>函数名：snake_case（下划线）</li>
                    <li>变量名：snake_case（下划线）</li>
                    <li>常量：UPPER_CASE（全大写）</li>
                  </ul>
                </el-card>
              </el-col>
              <el-col :span="12">
                <el-card class="rule-card">
                  <h4>代码要求</h4>
                  <ul>
                    <li>必须添加类型注解</li>
                    <li>必须包含事务处理</li>
                    <li>必须添加异常处理</li>
                    <li>必须添加权限控制</li>
                  </ul>
                </el-card>
              </el-col>
            </el-row>

            <h2 style="margin-top: 40px;">部署发布</h2>
            
            <h3>生产环境配置</h3>
            <el-steps :active="3" direction="vertical">
              <el-step title="配置生产环境">
                <div slot="description">
                  <p>编辑 <code>.env.prod</code> 文件，配置生产环境的数据库和 Redis</p>
                </div>
              </el-step>
              <el-step title="构建前端">
                <div slot="description">
                  <el-card class="code-card">
                    <pre><code>npm run build:prod</code></pre>
                  </el-card>
                </div>
              </el-step>
              <el-step title="启动后端">
                <div slot="description">
                  <el-card class="code-card">
                    <pre><code>python3 app.py --env=prod</code></pre>
                  </el-card>
                </div>
              </el-step>
            </el-steps>

            <h3 style="margin-top: 30px;">Docker 部署</h3>
            <el-card class="code-card">
              <pre><code># MySQL 版本
docker compose -f docker-compose.my.yml up -d --build

# PostgreSQL 版本
docker compose -f docker-compose.pg.yml up -d --build</code></pre>
            </el-card>
            <el-alert type="warning" :closable="false" show-icon style="margin-top: 10px;">
              警告：默认未做数据持久化配置，请注意数据备份或自行配置持久化
            </el-alert>
          </div>
        </el-tab-pane>

        <!-- 常见问题 -->
        <el-tab-pane label="常见问题" name="faq">
          <div class="guide-content">
            <h2>常见问题解答</h2>
            
            <el-collapse v-model="activeFaq">
              <!-- 环境问题 -->
              <el-collapse-item title="Q1：启动时提示需要安装 asyncpg？" name="1">
                <el-alert type="error" :closable="false" show-icon>
                  <strong>错误信息：</strong>ModuleNotFoundError: No module named 'asyncpg'
                </el-alert>
                <p style="margin-top: 10px;"><strong>原因：</strong></p>
                <ul>
                  <li>使用 MySQL 数据库，但安装了 PostgreSQL 的依赖包</li>
                  <li>或者环境中混装了两种数据库的驱动</li>
                </ul>
                <p style="margin-top: 10px;"><strong>解决方案：</strong></p>
                <el-card class="code-card">
                  <pre><code># 方案一：重新安装正确的依赖（推荐）
pip3 uninstall -y asyncpg psycopg2
pip3 install -r requirements.txt

# 方案二：使用虚拟环境（最佳实践）
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip3 install -r requirements.txt

# 方案三：如果确实需要 PostgreSQL
pip3 install -r requirements-pg.txt
# 并确保 .env.dev 中 DB_TYPE=postgresql</code></pre>
                </el-card>
                <p style="margin-top: 10px;"><strong>检查清单：</strong></p>
                <ul>
                  <li>确认 <code>.env.dev</code> 中的 <code>DB_TYPE</code> 配置正确（mysql 或 postgresql）</li>
                  <li>确认安装了对应数据库的依赖包</li>
                  <li>确认数据库连接信息正确</li>
                  <li>确认数据库服务已启动</li>
                </ul>
              </el-collapse-item>

              <el-collapse-item title="Q2：数据库连接失败？" name="2">
                <el-alert type="error" :closable="false" show-icon>
                  <strong>错误信息：</strong>Can't connect to MySQL server / Connection refused
                </el-alert>
                <p style="margin-top: 10px;"><strong>检查项：</strong></p>
                <ul>
                  <li>数据库服务是否启动</li>
                  <li><code>.env.dev</code> 中的数据库配置是否正确（主机、端口、用户名、密码）</li>
                  <li>数据库用户是否有足够的权限</li>
                  <li>防火墙是否允许数据库端口访问</li>
                  <li>数据库是否已创建（默认：youchen-fastapi）</li>
                </ul>
              </el-collapse-item>

              <el-collapse-item title="Q3：Redis 连接失败？" name="3">
                <el-alert type="error" :closable="false" show-icon>
                  <strong>错误信息：</strong>Error connecting to Redis
                </el-alert>
                <p style="margin-top: 10px;"><strong>检查项：</strong></p>
                <ul>
                  <li>Redis 服务是否启动</li>
                  <li><code>.env.dev</code> 中的 Redis 配置是否正确</li>
                  <li>Redis 密码是否正确（如果设置了密码）</li>
                  <li>Redis 端口是否被占用</li>
                </ul>
              </el-collapse-item>

              <el-collapse-item title="Q4：前端无法访问后端接口？" name="4">
                <el-alert type="error" :closable="false" show-icon>
                  <strong>错误信息：</strong>Network Error / CORS Error
                </el-alert>
                <p style="margin-top: 10px;"><strong>检查项：</strong></p>
                <ul>
                  <li>后端服务是否正常启动（访问 http://localhost:8000/docs 测试）</li>
                  <li>前端 <code>.env.development</code> 文件中的 API 地址是否正确</li>
                  <li>浏览器控制台是否有跨域错误</li>
                  <li>网络防火墙是否阻止了请求</li>
                </ul>
              </el-collapse-item>

              <!-- 代码生成问题 -->
              <el-collapse-item title="Q5：为什么提示"字典类型和关联表冲突"？" name="5">
                <el-alert type="error" :closable="false" show-icon>
                  <strong>原因：</strong>同一个字段同时配置了字典类型和关联表
                </el-alert>
                <p style="margin-top: 10px;"><strong>解决方案：</strong></p>
                <ul>
                  <li>如果数据源是系统字典，清空关联表配置，只保留字典类型</li>
                  <li>如果数据源是数据库表，清空字典类型，只保留关联表配置</li>
                </ul>
              </el-collapse-item>

              <el-collapse-item title="Q6：为什么提示"关联表值字段类型不匹配"？" name="6">
                <el-alert type="error" :closable="false" show-icon>
                  <strong>原因：</strong>当前字段类型与关联表值字段类型不兼容
                </el-alert>
                <p style="margin-top: 10px;"><strong>解决方案：</strong></p>
                <ul>
                  <li>方案1：修改当前字段类型为兼容类型（如果业务允许）</li>
                  <li>方案2：选择关联表中类型兼容的字段作为值字段</li>
                  <li>方案3：如果关联表没有合适的字段，考虑使用字典类型代替</li>
                </ul>
              </el-collapse-item>

              <el-collapse-item title="Q7：生成的代码在哪里？" name="7">
                <p><strong>下载代码包方式：</strong></p>
                <ul>
                  <li>代码会以 zip 文件形式下载到浏览器默认下载目录</li>
                  <li>解压后可以看到 backend 和 frontend 两个目录</li>
                </ul>
                <p style="margin-top: 10px;"><strong>生成到本地方式：</strong></p>
                <ul>
                  <li>后端代码：<code>ruoyi-fastapi-backend/module_business/</code></li>
                  <li>前端代码：<code>ruoyi-fastapi-frontend/src/views/business/</code></li>
                </ul>
              </el-collapse-item>

              <el-collapse-item title="Q8：生成菜单后看不到新菜单？" name="8">
                <p><strong>可能原因：</strong></p>
                <ul>
                  <li>菜单缓存未刷新</li>
                  <li>当前用户没有该菜单权限</li>
                </ul>
                <p style="margin-top: 10px;"><strong>解决方案：</strong></p>
                <ul>
                  <li>刷新页面（F5）或重新登录</li>
                  <li>在"系统管理 → 角色管理"中为角色分配菜单权限</li>
                </ul>
              </el-collapse-item>

              <el-collapse-item title="Q9：如何修改已生成的代码？" name="9">
                <p><strong>方法1：重新生成（推荐）</strong></p>
                <ul>
                  <li>修改字段配置</li>
                  <li>重新生成代码</li>
                  <li>覆盖原有文件</li>
                </ul>
                <p style="margin-top: 10px;"><strong>方法2：手动修改</strong></p>
                <ul>
                  <li>直接修改生成的代码文件</li>
                  <li>注意：下次重新生成会覆盖手动修改</li>
                </ul>
              </el-collapse-item>

              <!-- 开发问题 -->
              <el-collapse-item title="Q10：如何使用 AI 辅助开发？" name="10">
                <p><strong>使用步骤：</strong></p>
                <ol>
                  <li>确保项目已配置 AI 开发规则（<code>.kiro/steering/project-development-rules.md</code>）</li>
                  <li>使用 Kiro 或其他 AI 助手</li>
                  <li>描述需求，如："创建一个产品管理模块，包含产品名称、编码、价格等字段"</li>
                  <li>AI 会自动创建表、生成代码、配置菜单</li>
                  <li>重启后端服务，刷新前端页面</li>
                </ol>
                <p style="margin-top: 10px;"><strong>AI 可以做什么：</strong></p>
                <ul>
                  <li>创建新的业务模块</li>
                  <li>添加新字段和功能</li>
                  <li>修改业务逻辑</li>
                  <li>优化查询性能</li>
                  <li>修复 bug</li>
                </ul>
                <p style="margin-top: 10px;"><strong>AI 不会做什么（受保护）：</strong></p>
                <ul>
                  <li>修改框架核心文件</li>
                  <li>修改系统管理模块</li>
                  <li>修改中间件和异常处理</li>
                </ul>
              </el-collapse-item>

              <el-collapse-item title="Q11：如何添加自定义权限？" name="11">
                <p><strong>步骤：</strong></p>
                <ol>
                  <li>在 Controller 中使用 <code>UserInterfaceAuthDependency</code> 装饰器</li>
                  <li>指定权限标识，格式：<code>模块:功能:操作</code></li>
                  <li>在"系统管理 → 菜单管理"中添加按钮权限</li>
                  <li>在"系统管理 → 角色管理"中为角色分配权限</li>
                </ol>
                <p style="margin-top: 10px;"><strong>示例：</strong></p>
                <el-card class="code-card">
                  <pre><code>@product_controller.post(
    '/export',
    dependencies=[UserInterfaceAuthDependency('business:product:export')]
)
async def export_product(...):
    pass</code></pre>
                </el-card>
              </el-collapse-item>

              <el-collapse-item title="Q12：如何调试后端代码？" name="12">
                <p><strong>方法1：使用日志</strong></p>
                <el-card class="code-card">
                  <pre><code>from utils.log_util import logger

logger.info('调试信息')
logger.error('错误信息')</code></pre>
                </el-card>
                <p style="margin-top: 10px;"><strong>方法2：使用 IDE 调试</strong></p>
                <ul>
                  <li>在 IDE 中设置断点</li>
                  <li>以调试模式启动 <code>app.py</code></li>
                  <li>访问接口触发断点</li>
                </ul>
                <p style="margin-top: 10px;"><strong>方法3：查看日志文件</strong></p>
                <ul>
                  <li>日志文件位置：<code>logs/</code> 目录</li>
                  <li>按日期和级别分类</li>
                </ul>
              </el-collapse-item>
            </el-collapse>

            <h2 style="margin-top: 40px;">技术支持</h2>
            <el-card class="support-card">
              <p>如遇到其他问题，请：</p>
              <ol>
                <li>查看项目文档和开发规则（<code>.kiro/steering/project-development-rules.md</code>）</li>
                <li>查看日志文件（<code>logs/</code> 目录）</li>
                <li>在 GitHub 提交 Issue：<a href="https://github.com/guanjiang1106/youchen/issues" target="_blank">https://github.com/guanjiang1106/youchen/issues</a></li>
              </ol>
            </el-card>
          </div>
        </el-tab-pane>

      </el-tabs>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'GenGuide',
  data() {
    return {
      activeTab: 'intro',
      activeFaq: '1',
      activeModules: 'auth',
      // 禁止修改的文件
      protectedFiles: [
        { path: 'common/', desc: '公共组件（工具类、常量、注解等）' },
        { path: 'config/', desc: '配置文件（数据库、Redis、环境配置）' },
        { path: 'exceptions/', desc: '异常处理（全局异常、自定义异常）' },
        { path: 'middlewares/', desc: '中间件（请求处理、日志、CORS）' },
        { path: 'utils/', desc: '工具类（分页、响应、Excel、日志）' },
        { path: 'module_admin/', desc: '系统管理模块（用户、角色、菜单等核心功能）' },
        { path: 'app.py', desc: '应用入口文件' },
        { path: 'server.py', desc: '服务启动文件' },
        { path: 'alembic/', desc: '数据库迁移工具' }
      ]
    }
  }
}
</script>

<style scoped lang="scss">
.guide-container {
  padding: 20px;
}

.guide-card {
  .guide-header {
    font-size: 18px;
    font-weight: bold;
    color: #303133;
    
    i {
      margin-right: 8px;
      color: #409EFF;
    }
  }
}

.guide-content {
  padding: 20px;
  
  h2 {
    font-size: 20px;
    color: #303133;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid #409EFF;
  }
  
  h3 {
    font-size: 16px;
    color: #606266;
    margin: 20px 0 15px 0;
  }
  
  h4 {
    font-size: 14px;
    color: #303133;
    margin-bottom: 10px;
  }
  
  p {
    line-height: 1.8;
    color: #606266;
    margin: 10px 0;
  }
  
  ul, ol {
    padding-left: 20px;
    line-height: 2;
    color: #606266;
    
    li {
      margin: 5px 0;
    }
  }
  
  code {
    padding: 2px 6px;
    background-color: #f5f7fa;
    border: 1px solid #e4e7ed;
    border-radius: 3px;
    color: #e6a23c;
    font-family: 'Courier New', monospace;
  }
}

.feature-card {
  text-align: center;
  padding: 20px;
  height: 200px;
  
  .feature-icon {
    font-size: 48px;
    color: #409EFF;
    margin-bottom: 15px;
  }
  
  h3 {
    font-size: 16px;
    color: #303133;
    margin: 15px 0 10px 0;
  }
  
  p {
    font-size: 13px;
    color: #909399;
    line-height: 1.6;
  }
}

.code-card {
  background-color: #f5f7fa;
  border: 1px solid #e4e7ed;
  
  pre {
    margin: 0;
    padding: 0;
    
    code {
      display: block;
      padding: 15px;
      background: transparent;
      border: none;
      color: #303133;
      font-size: 13px;
      line-height: 1.6;
      overflow-x: auto;
    }
  }
}

.info-card {
  background-color: #f0f9ff;
  border: 1px solid #b3d8ff;
  margin-bottom: 15px;
  
  p {
    margin: 8px 0;
  }
  
  ul, ol {
    margin: 8px 0;
  }
}

.method-card {
  height: 220px;
  
  h4 {
    color: #409EFF;
    margin-bottom: 15px;
    
    i {
      margin-right: 5px;
    }
  }
  
  p {
    font-size: 13px;
    line-height: 1.8;
    margin: 8px 0;
  }
}

::v-deep .el-alert {
  margin: 15px 0;
  
  ul {
    margin: 10px 0 0 0;
  }
}

::v-deep .el-collapse-item__header {
  font-size: 15px;
  font-weight: 500;
  color: #303133;
}

::v-deep .el-collapse-item__content {
  padding: 20px;
  background-color: #fafafa;
}

::v-deep .el-steps {
  margin: 20px 0;
}

::v-deep .el-timeline {
  padding-left: 0;
}

::v-deep .el-timeline-item__timestamp {
  font-weight: bold;
  color: #409EFF;
}

.tech-card {
  text-align: center;
  padding: 20px;
  min-height: 220px;
  
  .tech-icon {
    font-size: 48px;
    margin-bottom: 15px;
  }
  
  h3 {
    font-size: 16px;
    color: #303133;
    margin: 15px 0;
  }
  
  ul {
    text-align: left;
    padding-left: 20px;
    
    li {
      line-height: 2;
      color: #606266;
    }
  }
}

.architecture-card {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  
  .arch-layer {
    background: white;
    padding: 20px;
    border-radius: 8px;
    min-height: 180px;
    
    h4 {
      font-size: 16px;
      color: #409EFF;
      margin-bottom: 10px;
    }
    
    p {
      font-size: 13px;
      color: #909399;
      margin-bottom: 15px;
    }
    
    ul {
      padding-left: 20px;
      
      li {
        line-height: 2;
        color: #606266;
        font-size: 13px;
      }
    }
  }
}

.dir-card {
  background-color: #f5f7fa;
  
  pre {
    margin: 0;
    
    code {
      display: block;
      padding: 15px;
      background: transparent;
      border: none;
      color: #303133;
      font-size: 12px;
      line-height: 1.6;
      overflow-x: auto;
    }
  }
}

.feature-highlight {
  min-height: 280px;
  
  h3 {
    color: #409EFF;
    margin-bottom: 15px;
  }
  
  p {
    margin: 10px 0;
  }
  
  ul {
    padding-left: 20px;
    
    li {
      line-height: 2;
      color: #606266;
    }
  }
}

.env-card {
  text-align: center;
  padding: 20px;
  min-height: 180px;
  
  h3 {
    font-size: 16px;
    color: #303133;
    margin-bottom: 15px;
  }
  
  ul {
    text-align: left;
    padding-left: 20px;
    
    li {
      line-height: 2;
      color: #606266;
    }
  }
}

.rule-card {
  min-height: 200px;
  
  h4 {
    color: #409EFF;
    margin-bottom: 15px;
  }
  
  ul {
    padding-left: 20px;
    
    li {
      line-height: 2;
      color: #606266;
    }
  }
}

.support-card {
  background-color: #f0f9ff;
  border: 1px solid #b3d8ff;
  
  p {
    margin-bottom: 10px;
  }
  
  ol {
    padding-left: 20px;
    
    li {
      line-height: 2;
      color: #606266;
      margin: 8px 0;
    }
  }
  
  a {
    color: #409EFF;
    text-decoration: none;
    
    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
