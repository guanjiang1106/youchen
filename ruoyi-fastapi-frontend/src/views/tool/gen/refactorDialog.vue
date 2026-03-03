<template>
  <el-dialog
    title="界面重构"
    :visible.sync="visible"
    width="70%"
    :close-on-click-modal="false"
    append-to-body
  >
    <el-form ref="form" :model="form" :rules="rules" label-width="100px">
      <el-form-item label="选择模型" prop="modelId">
        <el-select v-model="form.modelId" placeholder="请选择AI模型" style="width: 100%">
          <el-option
            v-for="model in modelList"
            :key="model.modelId"
            :label="model.modelName"
            :value="model.modelId"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="选择表" prop="tableIds">
        <el-select 
          v-model="form.tableIds" 
          multiple 
          placeholder="请选择要重构的表（可多选）" 
          style="width: 100%"
          @change="handleTableChange"
        >
          <el-option
            v-for="table in allTables"
            :key="table.tableId"
            :label="`${table.tableName} (${table.tableComment})`"
            :value="table.tableId"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="表信息" v-if="selectedTablesInfo.length > 0">
        <el-collapse accordion>
          <el-collapse-item 
            v-for="tableInfo in selectedTablesInfo" 
            :key="tableInfo.tableId"
            :title="`${tableInfo.tableName} - ${tableInfo.tableComment}`"
          >
            <el-table :data="tableInfo.columns" border size="small" max-height="200">
              <el-table-column prop="columnName" label="字段名" width="150" />
              <el-table-column prop="columnComment" label="字段描述" show-overflow-tooltip />
            </el-table>
          </el-collapse-item>
        </el-collapse>
      </el-form-item>

      <el-form-item label="保留原功能">
        <el-switch
          v-model="form.keepOriginal"
          active-text="保留原有增删改查功能"
          inactive-text="完全重构（不保留）"
        />
        <div style="color: #909399; font-size: 12px; margin-top: 5px;">
          <div v-if="form.keepOriginal" style="color: #67C23A;">
            ✓ 开启：保留原有的增删改查、表单、表格等所有功能，在此基础上增强
          </div>
          <div v-else style="color: #E6A23C;">
            ✗ 关闭：完全重新生成，不保留任何原有功能，根据需求从零开始设计
          </div>
        </div>
      </el-form-item>

      <!-- 新增按钮功能配置 -->
      <el-form-item label="新增按钮" v-if="form.keepOriginal">
        <el-switch
          v-model="form.addNewButton"
          active-text="启用新增按钮功能"
          inactive-text="不新增按钮"
        />
        <div style="color: #909399; font-size: 12px; margin-top: 5px;">
          <div v-if="form.addNewButton" style="color: #409EFF;">
            ✓ 启用：在保留原功能基础上，新增一个自定义按钮及其功能
          </div>
          <div v-else style="color: #909399;">
            ✗ 不启用：仅保留原有功能，不新增按钮
          </div>
        </div>
      </el-form-item>

      <!-- 按钮名称 -->
      <el-form-item label="按钮名称" prop="newButtonName" v-if="form.keepOriginal && form.addNewButton">
        <el-input
          v-model="form.newButtonName"
          placeholder="请输入按钮名称，例如：批量导出、数据统计、快速审核"
          clearable
        />
        <div style="color: #909399; font-size: 12px; margin-top: 5px;">
          按钮的具体功能请在下方"重构需求"中描述
        </div>
      </el-form-item>

      <el-form-item label="重构需求" prop="requirement">
        <el-input
          v-model="form.requirement"
          type="textarea"
          :rows="8"
          :placeholder="getRequirementPlaceholder()"
        />
      </el-form-item>
    </el-form>

    <div slot="footer" class="dialog-footer">
      <el-button @click="visible = false">取 消</el-button>
      <el-button type="primary" :loading="loading" @click="handleRefactor">开始重构</el-button>
    </div>

    <!-- 重构结果对话框 -->
    <el-dialog
      title="重构结果"
      :visible.sync="resultVisible"
      width="85%"
      append-to-body
      :close-on-click-modal="false"
    >
      <el-tabs v-model="activeTab">
        <el-tab-pane label="index.vue" name="index">
          <div class="code-header">
            <div class="code-tips">
              <i class="el-icon-info"></i>
              <span>前端页面组件，包含界面布局、表格、表单、搜索等功能</span>
            </div>
            <div class="code-actions">
              <el-button 
                size="mini" 
                icon="el-icon-edit" 
                @click="editCode('index')"
              >{{ editMode.index ? '完成' : '编辑' }}</el-button>
              <el-button
                size="mini"
                icon="el-icon-document-copy"
                v-clipboard:copy="resultCode.index"
                v-clipboard:success="clipboardSuccess"
              >复制</el-button>
            </div>
          </div>
          <el-input
            v-if="editMode.index"
            v-model="resultCode.index"
            type="textarea"
            :rows="20"
            class="code-editor"
          />
          <pre v-else><code class="hljs" v-html="highlightedCode(resultCode.index, 'vue')"></code></pre>
          
          <!-- 错误信息显示 -->
          <el-alert
            v-if="codeErrors.index"
            :title="'代码错误'"
            type="error"
            :closable="false"
            show-icon
            style="margin-top: 10px;"
          >
            <div slot="default">
              <pre style="white-space: pre-wrap; word-wrap: break-word; font-size: 12px; margin: 0;">{{ codeErrors.index }}</pre>
            </div>
          </el-alert>
        </el-tab-pane>
        
        <el-tab-pane label="controller.py" name="controller" v-if="resultCode.controller">
          <div class="code-header">
            <div class="code-tips">
              <i class="el-icon-info"></i>
              <span>后端控制器层，定义 API 接口路由和请求处理</span>
            </div>
            <div class="code-actions">
              <el-button 
                v-if="editMode.controller"
                size="mini" 
                icon="el-icon-magic-stick" 
                @click="formatCode('controller')"
              >格式化</el-button>
              <el-button 
                size="mini" 
                icon="el-icon-edit" 
                @click="editCode('controller')"
              >{{ editMode.controller ? '完成' : '编辑' }}</el-button>
              <el-button
                size="mini"
                icon="el-icon-document-copy"
                v-clipboard:copy="resultCode.controller"
                v-clipboard:success="clipboardSuccess"
              >复制</el-button>
            </div>
          </div>
          <el-input
            v-if="editMode.controller"
            v-model="resultCode.controller"
            type="textarea"
            :rows="20"
            class="code-editor"
          />
          <pre v-else><code class="hljs" v-html="highlightedCode(resultCode.controller, 'python')"></code></pre>
          
          <!-- 错误信息显示 -->
          <el-alert
            v-if="codeErrors.controller"
            :title="'代码错误'"
            type="error"
            :closable="false"
            show-icon
            style="margin-top: 10px;"
          >
            <div slot="default">
              <pre style="white-space: pre-wrap; word-wrap: break-word; font-size: 12px; margin: 0;">{{ codeErrors.controller }}</pre>
            </div>
          </el-alert>
        </el-tab-pane>
        
        <el-tab-pane label="service.py" name="service" v-if="resultCode.service">
          <div class="code-header">
            <div class="code-tips">
              <i class="el-icon-info"></i>
              <span>后端服务层，实现业务逻辑和数据处理</span>
            </div>
            <div class="code-actions">
              <el-button 
                v-if="editMode.service"
                size="mini" 
                icon="el-icon-magic-stick" 
                @click="formatCode('service')"
              >格式化</el-button>
              <el-button 
                size="mini" 
                icon="el-icon-edit" 
                @click="editCode('service')"
              >{{ editMode.service ? '完成' : '编辑' }}</el-button>
              <el-button
                size="mini"
                icon="el-icon-document-copy"
                v-clipboard:copy="resultCode.service"
                v-clipboard:success="clipboardSuccess"
              >复制</el-button>
            </div>
          </div>
          <el-input
            v-if="editMode.service"
            v-model="resultCode.service"
            type="textarea"
            :rows="20"
            class="code-editor"
          />
          <pre v-else><code class="hljs" v-html="highlightedCode(resultCode.service, 'python')"></code></pre>
          
          <!-- 错误信息显示 -->
          <el-alert
            v-if="codeErrors.service"
            :title="'代码错误'"
            type="error"
            :closable="false"
            show-icon
            style="margin-top: 10px;"
          >
            <div slot="default">
              <pre style="white-space: pre-wrap; word-wrap: break-word; font-size: 12px; margin: 0;">{{ codeErrors.service }}</pre>
            </div>
          </el-alert>
        </el-tab-pane>
        
        <el-tab-pane label="api.js" name="api" v-if="resultCode.api">
          <div class="code-header">
            <div class="code-tips">
              <i class="el-icon-info"></i>
              <span>前端 API 接口定义，封装后端接口调用</span>
            </div>
            <div class="code-actions">
              <el-button 
                size="mini" 
                icon="el-icon-edit" 
                @click="editCode('api')"
              >{{ editMode.api ? '完成' : '编辑' }}</el-button>
              <el-button
                size="mini"
                icon="el-icon-refresh"
                type="warning"
                :loading="regenerateLoading.api"
                @click="regenerateCode('api')"
              >重新生成</el-button>
              <el-button
                size="mini"
                icon="el-icon-document-copy"
                v-clipboard:copy="resultCode.api"
                v-clipboard:success="clipboardSuccess"
              >复制</el-button>
            </div>
          </div>
          <el-input
            v-if="editMode.api"
            v-model="resultCode.api"
            type="textarea"
            :rows="20"
            class="code-editor"
          />
          <pre v-else><code class="hljs" v-html="highlightedCode(resultCode.api, 'javascript')"></code></pre>
          
          <!-- 错误信息显示 -->
          <el-alert
            v-if="codeErrors.api"
            :title="'代码错误'"
            type="error"
            :closable="false"
            show-icon
            style="margin-top: 10px;"
          >
            <div slot="default">
              <pre style="white-space: pre-wrap; word-wrap: break-word; font-size: 12px; margin: 0;">{{ codeErrors.api }}</pre>
            </div>
          </el-alert>
        </el-tab-pane>
          </div>
          <el-input
            v-if="editMode.api"
            v-model="resultCode.api"
            type="textarea"
            :rows="20"
            class="code-editor"
          />
          <pre v-else><code class="hljs" v-html="highlightedCode(resultCode.api, 'javascript')"></code></pre>
        </el-tab-pane>
      </el-tabs>
      <div slot="footer" class="dialog-footer">
        <el-button @click="resultVisible = false">关 闭</el-button>
        <el-button 
          type="warning" 
          icon="el-icon-magic-stick"
          @click="fixAllCode"
        >一键修复</el-button>
        <el-button type="primary" @click="handleApplyRefactor">应用重构</el-button>
      </div>
    </el-dialog>
  </el-dialog>
</template>

<script>
import { listModel } from "@/api/ai/model";
import { refactorFrontend, applyRefactor, getGenTable, listTable } from "@/api/tool/gen";
import hljs from "highlight.js/lib/highlight";
import "highlight.js/styles/github-gist.css";
hljs.registerLanguage("vue", require("highlight.js/lib/languages/xml"));
hljs.registerLanguage("javascript", require("highlight.js/lib/languages/javascript"));
hljs.registerLanguage("python", require("highlight.js/lib/languages/python"));

export default {
  name: "RefactorDialog",
  data() {
    return {
      visible: false,
      resultVisible: false,
      loading: false,
      activeTab: "index",
      modelList: [],
      allTables: [],
      selectedTablesInfo: [],
      editMode: {
        index: false,
        controller: false,
        service: false,
        api: false
      },
      regenerateLoading: {
        index: false,
        controller: false,
        service: false,
        api: false
      },
      codeErrors: {
        index: '',
        controller: '',
        service: '',
        api: ''
      },
      form: {
        modelId: null,
        tableIds: [],
        keepOriginal: true,
        addNewButton: false,
        newButtonName: '',
        requirement: ""
      },
      resultCode: {
        index: "",
        api: "",
        controller: "",
        service: ""
      },
      rules: {
        modelId: [
          { required: true, message: "请选择AI模型", trigger: "change" }
        ],
        tableIds: [
          { required: true, message: "请至少选择一个表", trigger: "change" }
        ],
        requirement: [
          { required: true, message: "请输入重构需求", trigger: "blur" },
          { min: 10, message: "需求描述至少10个字符", trigger: "blur" }
        ],
        newButtonName: [
          { required: true, message: "请输入按钮名称", trigger: "blur" },
          { min: 2, max: 20, message: "按钮名称长度在2-20个字符", trigger: "blur" }
        ]
      }
    };
  },
  methods: {
    /** 获取重构需求的占位符文本 */
    getRequirementPlaceholder() {
      if (this.form.keepOriginal) {
        if (this.form.addNewButton && this.form.newButtonName) {
          return `请描述要增强的功能和新增按钮"${this.form.newButtonName}"的功能，例如：

1. 新增"${this.form.newButtonName}"按钮的功能：
   - 点击按钮后弹出对话框
   - 对话框中显示选中数据的统计信息
   - 支持导出统计结果为Excel

2. 其他增强功能：
   - 添加数据统计卡片，显示总数和今日新增
   - 优化搜索功能，添加高级搜索面板
   - 列表增加快速操作按钮

注意：原有的增删改查功能会保留`;
        } else {
          return `请描述要增强的功能，例如：
1. 添加数据统计卡片，显示总数和今日新增
2. 优化搜索功能，添加高级搜索面板
3. 列表增加快速操作按钮
4. 表单使用分组布局

注意：原有的增删改查功能会保留`;
        }
      } else {
        return `请描述完整的界面需求，例如：
1. 使用卡片式布局展示数据
2. 每个卡片显示教师姓名、编号、状态
3. 支持按姓名搜索
4. 点击卡片查看详情

注意：将完全重新设计，不保留原有功能`;
      }
    },

    /** 显示对话框 */
    async show(row) {
      this.visible = true;
      this.form.tableIds = [row.tableId];
      this.form.keepOriginal = true;
      this.form.addNewButton = false;
      this.form.newButtonName = '';
      this.selectedTablesInfo = [];
      
      // 加载AI模型列表
      await this.loadModelList();
      
      // 加载所有表列表
      await this.loadAllTables();
      
      // 加载选中表的信息
      await this.handleTableChange(this.form.tableIds);
    },

    /** 加载AI模型列表 */
    async loadModelList() {
      try {
        const response = await listModel({ pageNum: 1, pageSize: 100 });
        this.modelList = response.rows || [];
        // 默认选择第一个模型
        if (this.modelList.length > 0) {
          this.form.modelId = this.modelList[0].modelId;
        }
      } catch (error) {
        this.$modal.msgError("加载模型列表失败");
      }
    },

    /** 加载所有表列表 */
    async loadAllTables() {
      try {
        const response = await listTable({ pageNum: 1, pageSize: 1000 });
        this.allTables = response.rows || [];
      } catch (error) {
        this.$modal.msgError("加载表列表失败");
      }
    },

    /** 处理表选择变化 */
    async handleTableChange(tableIds) {
      this.selectedTablesInfo = [];
      for (const tableId of tableIds) {
        try {
          const response = await getGenTable(tableId);
          const table = this.allTables.find(t => t.tableId === tableId);
          this.selectedTablesInfo.push({
            tableId: tableId,
            tableName: table.tableName,
            tableComment: table.tableComment,
            businessName: table.businessName,
            moduleName: table.moduleName,
            columns: response.data.rows || []
          });
        } catch (error) {
          console.error(`加载表${tableId}信息失败`, error);
        }
      }
    },

    /** 开始重构 */
    handleRefactor() {
      this.$refs.form.validate(async valid => {
        if (valid) {
          // 如果启用了新增按钮功能，需要验证按钮名称
          if (this.form.keepOriginal && this.form.addNewButton) {
            if (!this.form.newButtonName) {
              this.$modal.msgWarning("请填写按钮名称");
              return;
            }
          }

          this.loading = true;
          try {
            const response = await refactorFrontend({
              tableIds: this.form.tableIds,
              modelId: this.form.modelId,
              keepOriginal: this.form.keepOriginal,
              addNewButton: this.form.addNewButton,
              newButtonName: this.form.newButtonName,
              requirement: this.form.requirement
            });
            
            this.resultCode = response.data;
            
            // 重置编辑模式
            this.editMode = {
              index: false,
              controller: false,
              service: false,
              api: false
            };
            
            this.resultVisible = true;
            this.$modal.msgSuccess("重构完成");
          } catch (error) {
            // 显示详细的错误信息
            const errorMsg = error.message || error.msg || "重构失败";
            
            // 如果是代码语法错误，提供更友好的提示
            if (errorMsg.includes("语法错误") || errorMsg.includes("IndentationError") || errorMsg.includes("SyntaxError")) {
              // 解析错误信息
              const hasIndentError = errorMsg.includes("IndentationError");
              const hasSyntaxError = errorMsg.includes("SyntaxError");
              const hasTryExceptError = errorMsg.includes("expected 'except' or 'finally' block");
              const hasDuplicateExceptError = errorMsg.includes("except Exception as e:") && (errorMsg.match(/except Exception as e:/g) || []).length > 1;
              const hasServiceError = errorMsg.includes("Service 代码");
              const hasControllerError = errorMsg.includes("Controller 代码");
              
              let errorTitle = '代码生成失败';
              let errorDetails = '';
              
              if (hasDuplicateExceptError) {
                errorTitle = '重复的 Except 块';
                errorDetails = `
                  <p style="color: #E6A23C; font-weight: bold;">检测到重复的 except 块</p>
                  <p style="margin: 10px 0;">AI 生成的代码中有多个相同的 <code>except Exception as e:</code> 块，这会导致语法错误。</p>
                  <div style="background: #f5f5f5; padding: 10px; border-radius: 4px; margin: 10px 0; font-family: monospace; font-size: 12px;">
                    <div style="color: #F56C6C;">✗ 错误的写法：</div>
                    <pre style="margin: 5px 0;">try:
    # 代码
    pass
except Exception as e:
    await query_db.rollback()
    raise e
except Exception as e:  # ❌ 重复
    await query_db.rollback()
    raise e</pre>
                    <div style="color: #67C23A; margin-top: 10px;">✓ 正确的写法：</div>
                    <pre style="margin: 5px 0;">try:
    # 代码
    pass
except Exception as e:
    await query_db.rollback()
    raise e</pre>
                  </div>
                `;
              } else if (hasTryExceptError) {
                errorTitle = 'Try-Except 块不完整';
                errorDetails = `
                  <p style="color: #E6A23C; font-weight: bold;">检测到不完整的 try-except 块</p>
                  <p style="margin: 10px 0;">AI 生成的代码中有 <code>try:</code> 语句，但缺少对应的 <code>except:</code> 或 <code>finally:</code> 块。</p>
                  <div style="background: #f5f5f5; padding: 10px; border-radius: 4px; margin: 10px 0; font-family: monospace; font-size: 12px;">
                    <div style="color: #67C23A;">✓ 正确的写法：</div>
                    <pre style="margin: 5px 0;">try:
    # 代码
    pass
except Exception as e:
    await query_db.rollback()
    raise e</pre>
                  </div>
                `;
              } else if (hasIndentError) {
                errorTitle = 'Python 缩进错误';
                errorDetails = `
                  <p style="color: #E6A23C; font-weight: bold;">检测到 Python 代码缩进问题</p>
                  <p style="margin: 10px 0;">AI 生成的代码缩进不正确，这是常见问题。</p>
                `;
              } else if (hasSyntaxError && errorMsg.includes("non-default argument follows default argument")) {
                errorTitle = 'Python 参数顺序错误';
                errorDetails = `
                  <p style="color: #E6A23C; font-weight: bold;">检测到函数参数顺序问题</p>
                  <p style="margin: 10px 0;">非默认参数不能跟在默认参数后面。</p>
                `;
              } else {
                errorDetails = `
                  <p style="color: #E6A23C; font-weight: bold;">代码生成失败</p>
                  <p style="margin: 10px 0;">AI 生成的代码存在语法错误。</p>
                `;
              }
              
              this.$alert(
                `<div style="text-align: left;">
                  ${errorDetails}
                  <div style="background: #FFF7E6; padding: 12px; border-radius: 4px; margin: 15px 0; border-left: 3px solid #E6A23C;">
                    <p style="margin: 0 0 8px 0; font-weight: bold; color: #E6A23C;">
                      <i class="el-icon-magic-stick"></i> 快速解决方案
                    </p>
                    <p style="margin: 0; font-size: 14px;">
                      点击下方的 <strong>"一键修复"</strong> 按钮，系统会自动：
                    </p>
                    <ul style="margin: 8px 0 0 20px; padding: 0; font-size: 13px;">
                      <li>移除重复的 except 块</li>
                      <li>补全缺失的 except 块</li>
                      <li>修复代码缩进问题</li>
                      <li>调整函数参数顺序</li>
                    </ul>
                  </div>
                  <p style="margin: 10px 0; font-weight: bold;">其他解决方案：</p>
                  <ol style="margin: 5px 0; padding-left: 20px; line-height: 1.8;">
                    <li><strong>重新生成</strong>：简化需求描述后重试</li>
                    <li><strong>切换模型</strong>：尝试使用其他 AI 模型</li>
                    <li><strong>手动修复</strong>：点击"编辑"按钮手动调整代码</li>
                    <li><strong>分步实现</strong>：将复杂需求拆分成多个简单需求</li>
                  </ol>
                  ${hasServiceError ? '<p style="margin: 10px 0; color: #F56C6C;"><i class="el-icon-warning"></i> Service 层代码有问题</p>' : ''}
                  ${hasControllerError ? '<p style="margin: 10px 0; color: #F56C6C;"><i class="el-icon-warning"></i> Controller 层代码有问题</p>' : ''}
                  <details style="margin-top: 15px;">
                    <summary style="cursor: pointer; color: #909399; font-size: 13px;">
                      <i class="el-icon-document"></i> 查看详细错误信息
                    </summary>
                    <pre style="margin-top: 10px; padding: 10px; background: #f5f5f5; border-radius: 4px; font-size: 12px; max-height: 300px; overflow: auto; white-space: pre-wrap; word-wrap: break-word;">${this.escapeHtml(errorMsg)}</pre>
                  </details>
                </div>`,
                errorTitle,
                {
                  dangerouslyUseHTMLString: true,
                  confirmButtonText: '我知道了',
                  type: 'warning',
                  customClass: 'code-error-dialog'
                }
              );
            } else {
              this.$modal.msgError(errorMsg);
            }
          } finally {
            this.loading = false;
          }
        }
      });
    },

    /** 应用重构 */
    async handleApplyRefactor() {
      try {
        // 获取第一个表作为主表
        const mainTable = this.selectedTablesInfo[0];
        
        await this.$modal.confirm(`确认要应用重构结果吗？这将覆盖 ${mainTable.tableName} 对应的文件。`);
        
        const response = await applyRefactor({
          tableId: mainTable.tableId,
          indexCode: this.resultCode.index,
          apiCode: this.resultCode.api,
          controllerCode: this.resultCode.controller,
          serviceCode: this.resultCode.service
        });
        
        this.$modal.msgSuccess(response.msg || "应用成功");
        this.resultVisible = false;
        this.visible = false;
        this.$emit("ok");
      } catch (error) {
        if (error !== 'cancel') {
          this.$modal.msgError(error.message || "应用失败");
        }
      }
    },

    /** 高亮显示 */
    highlightedCode(code, language) {
      if (!code) return '';
      const result = hljs.highlight(language, code || "", true);
      return result.value || '&nbsp;';
    },

    /** 复制成功 */
    clipboardSuccess() {
      this.$modal.msgSuccess("复制成功");
    },

    /** 重新生成指定文件的代码 */
    async regenerateCode(fileType) {
      // 弹出对话框让用户输入错误信息或修改需求
      this.$prompt('请描述当前代码的问题或需要修改的地方：', '重新生成 ' + fileType, {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputType: 'textarea',
        inputPlaceholder: '例如：\n1. 代码有语法错误\n2. 缺少某个功能\n3. 需要调整逻辑\n\n请详细描述问题，AI会根据描述重新生成代码',
        inputValidator: (value) => {
          if (!value || value.trim().length < 5) {
            return '请至少输入5个字符的问题描述';
          }
          return true;
        }
      }).then(async ({ value }) => {
        this.regenerateLoading[fileType] = true;
        this.codeErrors[fileType] = ''; // 清空之前的错误信息
        
        try {
          // 构建重新生成的请求
          const regenerateReq = {
            tableIds: this.form.tableIds,
            modelId: this.form.modelId,
            keepOriginal: this.form.keepOriginal,
            addNewButton: this.form.addNewButton,
            newButtonName: this.form.newButtonName,
            requirement: this.form.requirement,
            fileType: fileType,  // 指定要重新生成的文件类型
            errorMessage: value,  // 错误信息或修改需求
            currentCode: this.resultCode[fileType]  // 当前的代码
          };
          
          const response = await refactorFrontend(regenerateReq);
          
          // 只更新指定文件的代码
          if (response.data && response.data[fileType]) {
            this.resultCode[fileType] = response.data[fileType];
            this.$modal.msgSuccess(`${fileType} 重新生成成功`);
          } else {
            this.$modal.msgWarning(`未能生成 ${fileType} 的代码`);
          }
        } catch (error) {
          const errorMsg = error.message || error.msg || "重新生成失败";
          this.codeErrors[fileType] = errorMsg;
          this.$modal.msgError(`重新生成失败：${errorMsg}`);
        } finally {
          this.regenerateLoading[fileType] = false;
        }
      }).catch(() => {
        // 用户取消
      });
    },

    /** 切换编辑模式 */
    editCode(type) {
      this.editMode[type] = !this.editMode[type];
      if (!this.editMode[type]) {
        this.$modal.msgSuccess("已保存修改");
      }
    },

    /** 格式化代码 */
    formatCode(type) {
      const code = this.resultCode[type];
      if (!code) return;

      try {
        // Python 代码缩进修复
        if (type === 'controller' || type === 'service') {
          this.resultCode[type] = this.fixPythonIndentation(code);
          this.$modal.msgSuccess("代码格式化完成");
        } else {
          this.$modal.msgWarning("暂不支持此类型代码的格式化");
        }
      } catch (error) {
        this.$modal.msgError("格式化失败：" + error.message);
      }
    },

    /** 修复 Python 代码缩进 */
    fixPythonIndentation(code) {
      const lines = code.split('\n');
      const formatted = [];
      let indentLevel = 0;
      let inDocstring = false;
      let docstringChar = '';
      let prevLineWasBlank = false;

      for (let i = 0; i < lines.length; i++) {
        let line = lines[i];
        const trimmedLine = line.trim();
        
        // 保留空行
        if (!trimmedLine) {
          formatted.push('');
          prevLineWasBlank = true;
          continue;
        }

        // 处理文档字符串
        const hasTripleQuote = trimmedLine.includes('"""') || trimmedLine.includes("'''");
        if (hasTripleQuote) {
          const quoteMatch = trimmedLine.match(/"""|\'\'\'/);
          if (quoteMatch) {
            const char = quoteMatch[0];
            const count = (trimmedLine.match(new RegExp(char.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')) || []).length;
            
            if (!inDocstring) {
              inDocstring = true;
              docstringChar = char;
              // 如果同一行有开始和结束，则不在文档字符串中
              if (count >= 2) {
                inDocstring = false;
              }
            } else if (trimmedLine.includes(docstringChar)) {
              inDocstring = false;
            }
          }
        }

        // 如果在文档字符串中，保持当前缩进级别
        if (inDocstring && !hasTripleQuote) {
          formatted.push('    '.repeat(indentLevel) + trimmedLine);
          continue;
        }

        // 处理减少缩进的关键字（在添加缩进之前）
        if (trimmedLine.startsWith('except') || 
            trimmedLine.startsWith('elif') || 
            trimmedLine.startsWith('else:') || 
            trimmedLine.startsWith('finally:')) {
          indentLevel = Math.max(0, indentLevel - 1);
        }

        // 添加缩进
        const indentedLine = '    '.repeat(indentLevel) + trimmedLine;
        formatted.push(indentedLine);

        // 处理增加缩进的情况
        if (trimmedLine.endsWith(':') && !trimmedLine.startsWith('#')) {
          indentLevel++;
        }

        // 处理减少缩进的情况（某些语句后）
        // return, raise, break, continue, pass 后面如果不是 except/elif/else/finally，则减少缩进
        if (trimmedLine.startsWith('return ') || 
            trimmedLine === 'return' ||
            trimmedLine.startsWith('raise ') ||
            trimmedLine === 'raise' ||
            trimmedLine.startsWith('break') || 
            trimmedLine.startsWith('continue') ||
            trimmedLine === 'pass') {
          
          // 查看下一个非空行
          let nextNonEmptyLine = '';
          for (let j = i + 1; j < lines.length; j++) {
            const nextTrimmed = lines[j].trim();
            if (nextTrimmed) {
              nextNonEmptyLine = nextTrimmed;
              break;
            }
          }
          
          // 如果下一行不是 except/elif/else/finally，则减少缩进
          if (nextNonEmptyLine && 
              !nextNonEmptyLine.startsWith('except') && 
              !nextNonEmptyLine.startsWith('elif') && 
              !nextNonEmptyLine.startsWith('else:') && 
              !nextNonEmptyLine.startsWith('finally:')) {
            indentLevel = Math.max(0, indentLevel - 1);
          }
        }

        prevLineWasBlank = false;
      }

      return formatted.join('\n');
    },

    /** 一键修复所有代码 */
    async fixAllCode() {
      try {
        let fixed = false;
        let fixDetails = [];
        
        // 修复 Service 代码
        if (this.resultCode.service) {
          const originalService = this.resultCode.service;
          let serviceCode = originalService;
          
          // 1. 检查并修复不完整的 try-except 块
          serviceCode = this.fixIncompleteTryExcept(serviceCode);
          
          // 2. 修复缩进
          serviceCode = this.fixPythonIndentation(serviceCode);
          
          if (originalService !== serviceCode) {
            this.resultCode.service = serviceCode;
            fixDetails.push('Service 代码');
            fixed = true;
          }
        }
        
        // 修复 Controller 代码
        if (this.resultCode.controller) {
          const originalController = this.resultCode.controller;
          let controllerCode = originalController;
          
          // 1. 修复参数顺序问题
          controllerCode = this.fixFunctionParameters(controllerCode);
          
          // 2. 检查并修复不完整的 try-except 块
          controllerCode = this.fixIncompleteTryExcept(controllerCode);
          
          // 3. 修复缩进
          controllerCode = this.fixPythonIndentation(controllerCode);
          
          if (originalController !== controllerCode) {
            this.resultCode.controller = controllerCode;
            fixDetails.push('Controller 代码');
            fixed = true;
          }
        }
        
        if (fixed) {
          this.$modal.msgSuccess(`代码修复完成（${fixDetails.join('、')}），请检查并应用`);
        } else {
          this.$modal.msgInfo("代码无需修复");
        }
      } catch (error) {
        this.$modal.msgError("自动修复失败：" + error.message);
      }
    },

    /** 修复不完整的 try-except 块 */
    fixIncompleteTryExcept(code) {
      let lines = code.split('\n');
      
      // 第零遍：检测并移除重复的 except 块
      // 策略：找到所有连续的相同 except 块，只保留第一个
      const linesToKeep = [];
      let i = 0;
      
      while (i < lines.length) {
        const line = lines[i];
        const trimmed = line.trim();
        
        // 检查是否是 except 块的开始
        if (trimmed.startsWith('except Exception as e:')) {
          const indent = line.length - line.trimStart().length;
          linesToKeep.push(i); // 保留第一个 except
          
          // 检查接下来的行是否是相同的 except 块
          let j = i + 1;
          let exceptBlockLines = [i];
          
          // 收集当前 except 块的所有行
          while (j < lines.length) {
            const nextLine = lines[j];
            const nextTrimmed = nextLine.trim();
            const nextIndent = nextLine.length - nextLine.trimStart().length;
            
            if (!nextTrimmed) {
              j++;
              continue;
            }
            
            if (nextIndent > indent) {
              exceptBlockLines.push(j);
              linesToKeep.push(j);
              j++;
            } else {
              break;
            }
          }
          
          // 跳过后续相同的 except 块
          while (j < lines.length) {
            const nextLine = lines[j];
            const nextTrimmed = nextLine.trim();
            const nextIndent = nextLine.length - nextLine.trimStart().length;
            
            if (!nextTrimmed) {
              linesToKeep.push(j);
              j++;
              continue;
            }
            
            if (nextTrimmed.startsWith('except Exception as e:') && nextIndent === indent) {
              // 这是一个重复的 except 块，跳过它及其内容
              j++; // 跳过 except 行
              while (j < lines.length) {
                const blockLine = lines[j];
                const blockTrimmed = blockLine.trim();
                const blockIndent = blockLine.length - blockLine.trimStart().length;
                
                if (!blockTrimmed) {
                  j++;
                  continue;
                }
                
                if (blockIndent > indent) {
                  j++; // 跳过 except 块内容
                } else {
                  break;
                }
              }
            } else {
              break;
            }
          }
          
          i = j;
        } else {
          linesToKeep.push(i);
          i++;
        }
      }
      
      // 重建代码，只保留需要的行
      lines = linesToKeep.map(index => lines[index]);
      
      const tryBlocks = []; // 记录所有 try 块的信息
      
      // 第一遍：找出所有 try 块及其范围
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const trimmed = line.trim();
        const indent = line.length - line.trimStart().length;
        
        if (trimmed === 'try:') {
          tryBlocks.push({
            startLine: i,
            indent: indent,
            hasExcept: false,
            endLine: -1
          });
        }
        
        // 检测 except/finally 语句
        if ((trimmed.startsWith('except') || trimmed.startsWith('finally')) && tryBlocks.length > 0) {
          // 找到对应的 try 块
          for (let j = tryBlocks.length - 1; j >= 0; j--) {
            if (tryBlocks[j].indent === indent && !tryBlocks[j].hasExcept) {
              tryBlocks[j].hasExcept = true;
              break;
            }
          }
        }
      }
      
      // 第二遍：找出每个 try 块的结束位置
      for (const tryBlock of tryBlocks) {
        if (!tryBlock.hasExcept) {
          // 找到 try 块内容结束的位置（缩进减少的第一行）
          for (let i = tryBlock.startLine + 1; i < lines.length; i++) {
            const line = lines[i];
            const trimmed = line.trim();
            
            // 跳过空行和注释
            if (!trimmed || trimmed.startsWith('#')) {
              continue;
            }
            
            const indent = line.length - line.trimStart().length;
            
            // 如果缩进小于等于 try 的缩进，说明 try 块结束了
            if (indent <= tryBlock.indent) {
              tryBlock.endLine = i;
              break;
            }
          }
          
          // 如果没找到结束位置，说明 try 块到文件末尾
          if (tryBlock.endLine === -1) {
            tryBlock.endLine = lines.length;
          }
        }
      }
      
      // 第三遍：插入 except 块
      let insertedLines = 0;
      for (const tryBlock of tryBlocks) {
        if (!tryBlock.hasExcept) {
          const insertPos = tryBlock.endLine + insertedLines;
          const exceptIndent = ' '.repeat(tryBlock.indent);
          
          // 在指定位置插入 except 块
          lines.splice(insertPos, 0,
            exceptIndent + 'except Exception as e:',
            exceptIndent + '    await query_db.rollback()',
            exceptIndent + '    raise e'
          );
          
          insertedLines += 3;
        }
      }
      
      return lines.join('\n');
    },

    /** 修复函数参数顺序 */
    fixFunctionParameters(code) {
      // 修复参数顺序问题：非默认参数不能跟在默认参数后面
      const funcDefRegex = /(async\s+def\s+\w+\s*\([^)]*\))/g;
      return code.replace(funcDefRegex, (match) => {
        // 如果包含默认参数后跟非默认参数的情况，尝试修复
        if (match.includes('=') && match.includes('Annotated')) {
          // 简单的修复：移除可能的默认值
          return match.replace(/=\s*None,(\s*query_db:)/g, ',$1');
        }
        return match;
      });
    },

    /** HTML 转义 */
    escapeHtml(text) {
      const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
      };
      return text.replace(/[&<>"']/g, m => map[m]);
    }
  }
};
</script>

<style scoped>
.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  margin-bottom: 10px;
  border-bottom: 1px solid #e4e7ed;
}

.code-tips {
  display: flex;
  align-items: center;
  color: #606266;
  font-size: 13px;
}

.code-tips i {
  margin-right: 5px;
  color: #409eff;
}

.code-actions {
  display: flex;
  gap: 8px;
}

.code-editor {
  font-family: 'Courier New', Courier, monospace;
  font-size: 13px;
}

.code-editor >>> textarea {
  font-family: 'Courier New', Courier, monospace;
  font-size: 13px;
  line-height: 1.5;
}

pre {
  background-color: #f6f8fa;
  padding: 16px;
  border-radius: 6px;
  overflow: auto;
  max-height: 500px;
  margin: 0;
}

code {
  font-family: 'Courier New', Courier, monospace;
  font-size: 13px;
}
</style>

<style>
/* 全局样式：错误对话框 */
.code-error-dialog {
  width: 600px;
}

.code-error-dialog .el-message-box__message {
  line-height: 1.6;
}

.code-error-dialog pre {
  font-family: 'Courier New', Courier, monospace;
  line-height: 1.4;
}
</style>
