<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="搜索" prop="searchText">
        <el-input
          v-model="queryParams.searchText"
          placeholder="请输入技能名称或描述"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="el-icon-refresh"
          size="mini"
          @click="handleRefresh"
        >刷新</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="el-icon-data-analysis"
          size="mini"
          @click="handleStats"
        >统计</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-row :gutter="20" v-loading="loading">
      <el-col
        v-for="skill in filteredSkills"
        :key="skill.name"
        :xs="24"
        :sm="12"
        :md="8"
        :lg="6"
        class="mb-3"
      >
        <el-card class="skill-card" shadow="hover">
          <div slot="header" class="skill-header">
            <span class="skill-emoji">{{ skill.emoji || '📦' }}</span>
            <span class="skill-name">{{ skill.name }}</span>
            <el-tag v-if="skill.use_count > 0" size="small" type="success">
              {{ skill.use_count }}次
            </el-tag>
          </div>
          
          <div class="skill-body">
            <p class="skill-description">{{ skill.description }}</p>
            
            <div v-if="skill.requires && skill.requires.bins && skill.requires.bins.length" class="skill-requires">
              <el-tag
                v-for="bin in skill.requires.bins"
                :key="bin"
                size="small"
                class="mr-1 mb-1"
              >
                {{ bin }}
              </el-tag>
            </div>
            
            <div class="skill-footer">
              <el-button size="small" @click="handleDetail(skill)">
                查看详情
              </el-button>
              <el-button size="small" type="primary" @click="handleViewDoc(skill)">
                查看文档
              </el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 技能详情对话框 -->
    <el-dialog
      :title="`${currentSkill ? currentSkill.emoji || '📦' : ''} ${currentSkill ? currentSkill.name : ''} - ${currentSkill ? currentSkill.description : ''}`"
      :visible.sync="detailVisible"
      width="800px"
      append-to-body
    >
      <el-descriptions v-if="currentSkill" :column="2" border>
        <el-descriptions-item label="名称">
          {{ currentSkill.name }}
        </el-descriptions-item>
        <el-descriptions-item label="使用次数">
          {{ currentSkill.use_count || 0 }}
        </el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">
          {{ currentSkill.description }}
        </el-descriptions-item>
        <el-descriptions-item label="最后使用" :span="2">
          {{ currentSkill.last_used || '未使用' }}
        </el-descriptions-item>
        <el-descriptions-item label="依赖要求" :span="2">
          <el-tag
            v-for="bin in (currentSkill.requires && currentSkill.requires.bins) || []"
            :key="bin"
            class="mr-1"
          >
            {{ bin }}
          </el-tag>
          <span v-if="!currentSkill.requires || !currentSkill.requires.bins || !currentSkill.requires.bins.length">无</span>
        </el-descriptions-item>
      </el-descriptions>

      <div slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关 闭</el-button>
        <el-button type="primary" @click="handleViewDoc(currentSkill)">
          查看完整文档
        </el-button>
      </div>
    </el-dialog>

    <!-- 技能文档对话框 -->
    <el-dialog
      :title="`${currentSkill ? currentSkill.emoji || '📦' : ''} ${currentSkill ? currentSkill.name : ''} - 技能文档`"
      :visible.sync="docVisible"
      width="90%"
      top="5vh"
      append-to-body
      custom-class="skill-doc-dialog"
    >
      <div class="skill-doc">
        <el-button
          type="primary"
          size="small"
          class="mb-2"
          @click="handleCopyDoc"
        >
          <i class="el-icon-document-copy"></i> 复制文档
        </el-button>
        <div class="markdown-body" v-html="renderedDoc"></div>
      </div>

      <div slot="footer" class="dialog-footer">
        <el-button @click="docVisible = false">关 闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getSkillList, getSkillDetail } from "@/api/ai/skill";

export default {
  name: "AiSkill",
  data() {
    return {
      // 查询参数
      queryParams: {
        searchText: ''
      },
      // 显示搜索条件
      showSearch: true,
      // 加载状态
      loading: false,
      // 技能列表
      skills: [],
      // 详情对话框
      detailVisible: false,
      // 文档对话框
      docVisible: false,
      // 当前技能
      currentSkill: null
    };
  },
  computed: {
    // 过滤后的技能列表
    filteredSkills() {
      if (!this.queryParams.searchText) {
        return this.skills;
      }
      const searchText = this.queryParams.searchText.toLowerCase();
      return this.skills.filter(skill =>
        skill.name.toLowerCase().includes(searchText) ||
        skill.description.toLowerCase().includes(searchText)
      );
    },
    // 渲染的文档内容（简单的换行处理）
    renderedDoc() {
      if (!this.currentSkill || !this.currentSkill.content) {
        return '';
      }
      // 简单的文本格式化，保留换行和代码块
      return this.currentSkill.content
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\n/g, '<br>')
        .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
        .replace(/`([^`]+)`/g, '<code>$1</code>');
    }
  },
  created() {
    this.getList();
  },
  methods: {
    /** 查询技能列表 */
    getList() {
      this.loading = true;
      getSkillList().then(response => {
        this.skills = response.data.skills || [];
        this.loading = false;
      }).catch(() => {
        this.loading = false;
      });
    },
    /** 搜索按钮操作 */
    handleQuery() {
      // 过滤逻辑在 computed 中处理
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.queryParams.searchText = '';
      this.handleQuery();
    },
    /** 刷新按钮操作 */
    handleRefresh() {
      this.queryParams.searchText = '';
      this.getList();
    },
    /** 统计按钮操作 */
    handleStats() {
      this.loading = true;
      import("@/api/ai/skill").then(({ getSkillStats }) => {
        getSkillStats().then(response => {
          const stats = response.data;
          let message = `<div style="text-align: left;">
            <p><strong>技能总数：</strong>${stats.total_skills}</p>
            <p><strong>已使用技能：</strong>${stats.used_skills}</p>
            <p><strong>总使用次数：</strong>${stats.total_uses}</p>
            <p><strong>最常用技能：</strong></p>
            <ul>`;
          
          stats.top_skills.forEach(skill => {
            message += `<li>${skill.emoji || '📦'} ${skill.name}: ${skill.use_count}次</li>`;
          });
          
          message += `</ul></div>`;
          
          this.$alert(message, '技能使用统计', {
            dangerouslyUseHTMLString: true,
            confirmButtonText: '确定'
          });
          this.loading = false;
        }).catch(() => {
          this.loading = false;
        });
      });
    },
    /** 查看详情 */
    handleDetail(skill) {
      this.loading = true;
      getSkillDetail(skill.name).then(response => {
        this.currentSkill = response.data;
        this.detailVisible = true;
        this.loading = false;
      }).catch(() => {
        this.loading = false;
      });
    },
    /** 查看文档 */
    handleViewDoc(skill) {
      if (!skill.content) {
        this.loading = true;
        getSkillDetail(skill.name).then(response => {
          this.currentSkill = response.data;
          this.docVisible = true;
          this.loading = false;
        }).catch(() => {
          this.loading = false;
        });
      } else {
        this.currentSkill = skill;
        this.docVisible = true;
      }
    },
    /** 复制文档 */
    handleCopyDoc() {
      if (!this.currentSkill || !this.currentSkill.content) {
        return;
      }
      const textarea = document.createElement('textarea');
      textarea.value = this.currentSkill.content;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      this.$modal.msgSuccess('文档已复制到剪贴板');
    }
  }
};
</script>

<style scoped lang="scss">
.skill-card {
  height: 100%;
  
  ::v-deep .el-card__header {
    padding: 12px 15px;
  }
  
  .skill-header {
    display: flex;
    align-items: center;
    gap: 8px;
    
    .skill-emoji {
      font-size: 24px;
    }
    
    .skill-name {
      flex: 1;
      font-weight: bold;
      font-size: 16px;
    }
  }
  
  .skill-body {
    .skill-description {
      color: #666;
      font-size: 14px;
      margin-bottom: 12px;
      min-height: 40px;
      line-height: 1.5;
    }
    
    .skill-requires {
      margin-bottom: 12px;
      min-height: 24px;
    }
    
    .skill-footer {
      display: flex;
      gap: 8px;
      
      .el-button {
        flex: 1;
      }
    }
  }
}

.skill-doc {
  .markdown-body {
    padding: 20px;
    background: #f5f5f5;
    border-radius: 4px;
    max-height: 600px;
    overflow-y: auto;
    
    ::v-deep {
      h1, h2, h3, h4, h5, h6 {
        margin-top: 1em;
        margin-bottom: 0.5em;
      }
      
      code {
        background: #e7e7e7;
        padding: 2px 4px;
        border-radius: 3px;
      }
      
      pre {
        background: #2d2d2d;
        color: #f8f8f2;
        padding: 15px;
        border-radius: 5px;
        overflow-x: auto;
        
        code {
          background: transparent;
          padding: 0;
        }
      }
    }
  }
}

::v-deep .skill-doc-dialog {
  .el-dialog__body {
    padding: 10px 20px;
  }
}

.mb-3 {
  margin-bottom: 20px;
}

.mr-1 {
  margin-right: 5px;
}

.mb-1 {
  margin-bottom: 5px;
}

.mb-2 {
  margin-bottom: 10px;
}
</style>
