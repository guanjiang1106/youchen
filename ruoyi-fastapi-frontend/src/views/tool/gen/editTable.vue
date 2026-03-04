<template>
  <el-card>
    <el-tabs v-model="activeName">
      <el-tab-pane label="基本信息" name="basic">
        <basic-info-form ref="basicInfo" :info="info" />
      </el-tab-pane>
      <el-tab-pane label="字段信息" name="columnInfo">
        <el-table 
          ref="dragTable" 
          :data="columns" 
          row-key="columnId" 
          :max-height="tableHeight"
          border
          size="small"
          class="gen-table"
          style="width: 100%">
          <el-table-column label="序号" type="index" width="50" align="center" class-name="allowDrag"/>
          <el-table-column label="字段列名" prop="columnName" width="120" :show-overflow-tooltip="true" class-name="allowDrag"/>
          <el-table-column label="字段描述" width="120">
            <template slot-scope="scope">
              <el-input v-model="scope.row.columnComment" size="small" placeholder="字段描述"></el-input>
            </template>
          </el-table-column>
          <el-table-column label="物理类型" width="120">
            <template slot-scope="scope">
              <el-select v-model="scope.row.columnType" size="small" style="width: 100%">
                <el-option label="varchar" value="varchar" />
                <el-option label="char" value="char" />
                <el-option label="text" value="text" />
                <el-option label="mediumtext" value="mediumtext" />
                <el-option label="longtext" value="longtext" />
                <el-option label="int" value="int" />
                <el-option label="bigint" value="bigint" />
                <el-option label="tinyint" value="tinyint" />
                <el-option label="smallint" value="smallint" />
                <el-option label="decimal" value="decimal" />
                <el-option label="float" value="float" />
                <el-option label="double" value="double" />
                <el-option label="datetime" value="datetime" />
                <el-option label="timestamp" value="timestamp" />
                <el-option label="date" value="date" />
                <el-option label="time" value="time" />
                <el-option label="blob" value="blob" />
                <el-option label="json" value="json" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="Python类型" width="110">
            <template slot-scope="scope">
              <el-select v-model="scope.row.pythonType" size="small" style="width: 100%">
                <el-option label="str" value="str" />
                <el-option label="int" value="int" />
                <el-option label="float" value="float" />
                <el-option label="Decimal" value="Decimal" />
                <el-option label="date" value="date" />
                <el-option label="time" value="time" />
                <el-option label="datetime" value="datetime" />
                <el-option label="bytes" value="bytes" />
                <el-option label="dict" value="dict" />
                <el-option label="list" value="list" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="Python属性" width="120">
            <template slot-scope="scope">
              <el-input v-model="scope.row.pythonField" size="small" placeholder="属性名"></el-input>
            </template>
          </el-table-column>

          <el-table-column label="插入" width="50" align="center">
            <template slot-scope="scope">
              <el-checkbox true-label="1" false-label="0" v-model="scope.row.isInsert"></el-checkbox>
            </template>
          </el-table-column>
          <el-table-column label="编辑" width="50" align="center">
            <template slot-scope="scope">
              <el-checkbox true-label="1" false-label="0" v-model="scope.row.isEdit"></el-checkbox>
            </template>
          </el-table-column>
          <el-table-column label="列表" width="50" align="center">
            <template slot-scope="scope">
              <el-checkbox true-label="1" false-label="0" v-model="scope.row.isList"></el-checkbox>
            </template>
          </el-table-column>
          <el-table-column label="查询" width="50" align="center">
            <template slot-scope="scope">
              <el-checkbox true-label="1" false-label="0" v-model="scope.row.isQuery"></el-checkbox>
            </template>
          </el-table-column>
          <el-table-column label="必填" width="50" align="center">
            <template slot-scope="scope">
              <el-checkbox true-label="1" false-label="0" v-model="scope.row.isRequired"></el-checkbox>
            </template>
          </el-table-column>
          <el-table-column label="唯一" width="50" align="center">
            <template slot-scope="scope">
              <el-checkbox true-label="1" false-label="0" v-model="scope.row.isUnique"></el-checkbox>
            </template>
          </el-table-column>
          <el-table-column label="查询方式" width="100">
            <template slot-scope="scope">
              <el-select v-model="scope.row.queryType" size="small" style="width: 100%">
                <el-option label="=" value="EQ" />
                <el-option label="!=" value="NE" />
                <el-option label=">" value="GT" />
                <el-option label=">=" value="GTE" />
                <el-option label="<" value="LT" />
                <el-option label="<=" value="LTE" />
                <el-option label="LIKE" value="LIKE" />
                <el-option label="BETWEEN" value="BETWEEN" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="显示类型" width="120">
            <template slot-scope="scope">
              <el-select v-model="scope.row.htmlType" size="small" style="width: 100%">
                <el-option label="文本框" value="input" />
                <el-option label="文本域" value="textarea" />
                <el-option label="下拉框" value="select" />
                <el-option label="单选框" value="radio" />
                <el-option label="复选框" value="checkbox" />
                <el-option label="日期控件" value="datetime" />
                <el-option label="图片上传" value="imageUpload" />
                <el-option label="文件上传" value="fileUpload" />
                <el-option label="富文本" value="editor" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="字典类型" width="150">
            <template slot-scope="scope">
              <el-select 
                v-model="scope.row.dictType" 
                clearable 
                filterable 
                placeholder="选择字典" 
                size="small" 
                style="width: 100%"
                :class="{'has-conflict': scope.row.dictType && scope.row.linkTable}">
                <el-option
                  v-for="dict in dictOptions"
                  :key="dict.dictType"
                  :label="dict.dictName"
                  :value="dict.dictType">
                  <span style="float: left">{{ dict.dictName }}</span>
                  <span style="float: right; color: #8492a6; font-size: 12px">{{ dict.dictType }}</span>
              </el-option>
              </el-select>
              <div v-if="scope.row.dictType && scope.row.linkTable" class="conflict-tip">
                <i class="el-icon-warning"></i> 与关联表冲突
              </div>
            </template>
          </el-table-column>
          <el-table-column label="关联表配置" width="280">
            <template slot-scope="scope">
              <div v-if="['select', 'radio', 'checkbox'].includes(scope.row.htmlType)" style="display: flex; flex-direction: column; gap: 4px;">
                <el-select 
                  v-model="scope.row.linkTable" 
                  clearable 
                  filterable 
                  placeholder="选择关联表"
                  size="small"
                  style="width: 100%;"
                  :class="{'has-conflict': scope.row.dictType && scope.row.linkTable}"
                  @change="onLinkTableChange(scope.row)">
                  <el-option
                    v-for="table in tables"
                    :key="table.tableName"
                    :label="table.tableComment"
                    :value="table.tableName">
                    <span style="float: left">{{ table.tableComment }}</span>
                    <span style="float: right; color: #8492a6; font-size: 12px">{{ table.tableName }}</span>
                  </el-option>
                </el-select>
                <div v-if="scope.row.dictType && scope.row.linkTable" class="conflict-tip">
                  <i class="el-icon-warning"></i> 与字典类型冲突
                </div>
                <div v-if="scope.row.linkTable" style="display: flex; gap: 4px;">
                  <el-input 
                    v-model="scope.row.linkLabelField" 
                    placeholder="标签字段"
                    size="small"
                    readonly
                    style="flex: 1; cursor: pointer;"
                    :class="{'field-required': !scope.row.linkLabelField}"
                    @click.native="openFieldSelector(scope.row, 'label')">
                    <template slot="prepend">标签</template>
                    <i slot="suffix" class="el-icon-search" style="cursor: pointer;"></i>
                  </el-input>
                  <el-input 
                    v-model="scope.row.linkValueField" 
                    placeholder="值字段"
                    size="small"
                    readonly
                    style="flex: 1; cursor: pointer;"
                    :class="{'field-required': !scope.row.linkValueField}"
                    @click.native="openFieldSelector(scope.row, 'value')">
                    <template slot="prepend">值</template>
                    <i slot="suffix" class="el-icon-search" style="cursor: pointer;"></i>
                  </el-input>
                </div>
              </div>
              <span v-else style="color: #c0c4cc; font-size: 12px;">-</span>
            </template>
          </el-table-column>
          <el-table-column label="显示页签" width="100">
            <template slot-scope="scope">
              <el-select v-model="scope.row.tabPage" placeholder="页签" size="small" style="width: 100%">
                <el-option label="基本信息" value="basic" />
                <el-option label="详细信息" value="detail" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="排序" width="80" align="center">
            <template slot-scope="scope">
              <el-input-number 
                v-model="scope.row.sort" 
                :min="0" 
                :max="9999"
                controls-position="right"
                size="small"
                style="width: 100%"
              ></el-input-number>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="生成信息" name="genInfo">
        <gen-info-form ref="genInfo" :info="info" :tables="tables" :menus="menus"/>
      </el-tab-pane>
    </el-tabs>
    <el-form label-width="100px">
      <el-form-item style="text-align: center;margin-left:-100px;margin-top:10px;">
        <el-button type="primary" @click="submitForm()">提交</el-button>
        <el-button @click="close()">返回</el-button>
      </el-form-item>
    </el-form>

    <!-- 字段选择对话框 -->
    <el-dialog 
      :title="fieldSelectorTitle" 
      :visible.sync="fieldSelectorVisible" 
      width="600px"
      append-to-body>
      <div v-if="currentEditRow" style="margin-bottom: 15px; padding: 10px; background-color: #f5f7fa; border-radius: 4px;">
        <div style="font-size: 13px; color: #606266;">
          <strong>当前字段：</strong>
          <span style="color: #409EFF;">{{ currentEditRow.columnComment || currentEditRow.columnName }}</span>
          <span style="margin-left: 10px; color: #909399;">
            ({{ currentEditRow.columnName }})
          </span>
        </div>
        <div style="font-size: 12px; color: #909399; margin-top: 5px;">
          <strong>字段类型：</strong>
          <el-tag size="mini" type="info">{{ currentEditRow.columnType }}</el-tag>
          <el-tag size="mini" type="success" style="margin-left: 5px;">{{ currentEditRow.pythonType }}</el-tag>
          <span v-if="currentFieldType === 'value'" style="margin-left: 10px; color: #E6A23C;">
            ⚠️ 请选择类型兼容的字段
          </span>
        </div>
      </div>
      <el-table 
        :data="linkTableFields" 
        highlight-current-row
        @current-change="handleFieldSelect"
        max-height="400px"
        border
        size="small">
        <el-table-column label="字段名" prop="columnName" width="150">
          <template slot-scope="scope">
            <span style="font-family: monospace; color: #409EFF;">{{ scope.row.columnName }}</span>
          </template>
        </el-table-column>
        <el-table-column label="字段描述" prop="columnComment" show-overflow-tooltip>
          <template slot-scope="scope">
            <span>{{ scope.row.columnComment || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="物理类型" prop="columnType" width="100">
          <template slot-scope="scope">
            <el-tag 
              size="mini" 
              :type="getFieldTypeTagType(scope.row)">
              {{ scope.row.columnType }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Python类型" prop="pythonType" width="90">
          <template slot-scope="scope">
            <el-tag size="mini" type="success">{{ scope.row.pythonType }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button @click="fieldSelectorVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmFieldSelect">确定</el-button>
      </div>
    </el-dialog>
  </el-card>
</template>

<script>
import { getGenTable, updateGenTable } from "@/api/tool/gen";
import { optionselect as getDictOptionselect } from "@/api/system/dict/type";
import { listMenu as getMenuTreeselect } from "@/api/system/menu";
import basicInfoForm from "./basicInfoForm";
import genInfoForm from "./genInfoForm";
import Sortable from 'sortablejs'

export default {
  name: "GenEdit",
  components: {
    basicInfoForm,
    genInfoForm
  },
  data() {
    return {
      // 选中选项卡的 name
      activeName: "columnInfo",
      // 表格的高度
      tableHeight: document.documentElement.scrollHeight - 245 + "px",
      // 表信息
      tables: [],
      // 表列信息
      columns: [],
      // 字典信息
      dictOptions: [],
      // 菜单信息
      menus: [],
      // 表详细信息
      info: {},
      // 字段选择器相关
      fieldSelectorVisible: false,
      fieldSelectorTitle: '选择字段',
      linkTableFields: [],
      currentEditRow: null,
      currentFieldType: null, // 'label' 或 'value'
      selectedField: null,
      // 关联表字段信息缓存
      linkTableFieldsCache: {}
    };
  },
  created() {
    const tableId = this.$route.params && this.$route.params.tableId;
    if (tableId) {
      // 获取表详细信息
      getGenTable(tableId).then(res => {
        this.columns = res.data.rows;
        // 初始化字段默认值
        this.columns.forEach((column, index) => {
          // 设置排序
          if (!column.sort) {
            column.sort = (index + 1) * 10;
          }
          // 设置默认页签
          if (!column.tabPage) {
            // 审计字段默认放在详细信息页签
            const detailFields = ['create_by', 'create_time', 'update_by', 'update_time', 'remark'];
            column.tabPage = detailFields.includes(column.columnName) ? 'detail' : 'basic';
          }
          // 初始化关联表字段
          if (!column.linkTable) {
            column.linkTable = '';
          }
          if (!column.linkLabelField) {
            column.linkLabelField = '';
          }
          if (!column.linkValueField) {
            column.linkValueField = '';
          }
        });
        this.info = res.data.info;
        this.tables = res.data.tables;
      });
      /** 查询字典下拉列表 */
      getDictOptionselect().then(response => {
        this.dictOptions = response.data;
      });
      /** 查询菜单下拉列表 */
      getMenuTreeselect().then(response => {
        this.menus = this.handleTree(response.data, "menuId");
      });
    }
  },
  methods: {
    /** 关联表变化时的处理 */
    onLinkTableChange(row) {
      if (!row.linkTable) {
        row.linkLabelField = '';
        row.linkValueField = '';
      } else {
        // 清空之前的字段选择
        row.linkLabelField = '';
        row.linkValueField = '';
        this.$message.success(`已选择关联表：${row.linkTable}，请点击输入框选择字段`);
      }
    },
    /** 打开字段选择器 */
    openFieldSelector(row, fieldType) {
      if (!row.linkTable) {
        this.$message.warning('请先选择关联表');
        return;
      }
      
      this.currentEditRow = row;
      this.currentFieldType = fieldType;
      this.fieldSelectorTitle = fieldType === 'label' ? '选择标签字段' : '选择值字段';
      
      // 获取关联表的字段信息
      const linkTable = this.tables.find(t => t.tableName === row.linkTable);
      if (linkTable && linkTable.tableId) {
        // 检查缓存
        if (this.linkTableFieldsCache[row.linkTable]) {
          this.linkTableFields = this.linkTableFieldsCache[row.linkTable];
          this.fieldSelectorVisible = true;
          this.highlightSelectedField(row, fieldType);
        } else {
          // 从后端获取表字段信息并缓存
          getGenTable(linkTable.tableId).then(res => {
            this.linkTableFields = res.data.rows || [];
            // 缓存字段信息
            this.linkTableFieldsCache[row.linkTable] = this.linkTableFields;
            this.fieldSelectorVisible = true;
            this.highlightSelectedField(row, fieldType);
          }).catch(() => {
            this.$message.error('获取表字段信息失败');
          });
        }
      } else {
        this.$message.error('未找到关联表信息');
      }
    },
    /** 高亮已选择的字段 */
    highlightSelectedField(row, fieldType) {
      this.$nextTick(() => {
        const currentField = fieldType === 'label' ? row.linkLabelField : row.linkValueField;
        if (currentField) {
          const index = this.linkTableFields.findIndex(f => f.columnName === currentField);
          if (index >= 0) {
            this.selectedField = this.linkTableFields[index];
          }
        }
      });
    },
    /** 获取字段类型标签颜色 */
    getFieldTypeTagType(field) {
      if (!this.currentEditRow || this.currentFieldType !== 'value') {
        return 'info';
      }
      
      const currentType = this.normalizeColumnType(this.currentEditRow.columnType);
      const fieldType = this.normalizeColumnType(field.columnType);
      const currentPythonType = this.currentEditRow.pythonType;
      const fieldPythonType = field.pythonType;
      
      const isCompatible = this.areTypesCompatible(currentType, fieldType, currentPythonType, fieldPythonType);
      
      return isCompatible ? 'success' : 'danger';
    },
    /** 选择字段 */
    handleFieldSelect(row) {
      this.selectedField = row;
    },
    /** 确认选择字段 */
    confirmFieldSelect() {
      if (!this.selectedField) {
        this.$message.warning('请选择一个字段');
        return;
      }
      
      // 如果是选择值字段，检查类型兼容性
      if (this.currentFieldType === 'value' && this.currentEditRow) {
        const currentType = this.normalizeColumnType(this.currentEditRow.columnType);
        const selectedType = this.normalizeColumnType(this.selectedField.columnType);
        const currentPythonType = this.currentEditRow.pythonType;
        const selectedPythonType = this.selectedField.pythonType;
        
        const isCompatible = this.areTypesCompatible(currentType, selectedType, currentPythonType, selectedPythonType);
        
        if (!isCompatible) {
          // 类型不兼容，显示警告确认框
          this.$confirm(
            `<div style="text-align: left;">
              <p style="margin-bottom: 10px; color: #E6A23C;">
                <i class="el-icon-warning" style="font-size: 18px;"></i>
                <strong> 字段类型不兼容警告</strong>
              </p>
              <div style="padding: 10px; background-color: #fef0f0; border-left: 3px solid #F56C6C; margin-bottom: 10px;">
                <p style="margin: 5px 0; color: #606266;">
                  <strong>当前字段：</strong>
                  <span style="color: #409EFF;">${this.currentEditRow.columnComment || this.currentEditRow.columnName}</span>
                </p>
                <p style="margin: 5px 0; color: #909399;">
                  类型：<el-tag size="mini">${this.currentEditRow.columnType}</el-tag> / 
                  <el-tag size="mini">${currentPythonType}</el-tag>
                </p>
              </div>
              <div style="padding: 10px; background-color: #fef0f0; border-left: 3px solid #F56C6C;">
                <p style="margin: 5px 0; color: #606266;">
                  <strong>选择的值字段：</strong>
                  <span style="color: #F56C6C;">${this.selectedField.columnComment || this.selectedField.columnName}</span>
                </p>
                <p style="margin: 5px 0; color: #909399;">
                  类型：<el-tag size="mini">${this.selectedField.columnType}</el-tag> / 
                  <el-tag size="mini">${selectedPythonType}</el-tag>
                </p>
              </div>
              <p style="margin-top: 15px; color: #606266; line-height: 1.6;">
                这两个字段的类型不兼容，可能导致：<br/>
                • 数据存储错误<br/>
                • 查询条件失效<br/>
                • 运行时类型转换异常<br/>
              </p>
              <p style="margin-top: 10px; color: #E6A23C;">
                <strong>建议：</strong>选择类型兼容的字段（如 ID 字段对应 ID 字段）
              </p>
            </div>`,
            '类型不兼容',
            {
              confirmButtonText: '仍然使用',
              cancelButtonText: '重新选择',
              type: 'warning',
              dangerouslyUseHTMLString: true,
              customClass: 'type-mismatch-confirm-dialog'
            }
          ).then(() => {
            // 用户确认使用不兼容的字段
            this.applyFieldSelection();
          }).catch(() => {
            // 用户取消，不做任何操作，让用户重新选择
            this.$message.info('请重新选择类型兼容的字段');
          });
          return;
        }
      }
      
      // 类型兼容或选择标签字段，直接应用
      this.applyFieldSelection();
    },
    /** 应用字段选择 */
    applyFieldSelection() {
      if (this.currentFieldType === 'label') {
        this.currentEditRow.linkLabelField = this.selectedField.columnName;
      } else {
        this.currentEditRow.linkValueField = this.selectedField.columnName;
      }
      
      this.fieldSelectorVisible = false;
      this.selectedField = null;
      this.$message.success('字段选择成功');
    },
    /** 提交按钮 */
    submitForm() {
      // 先进行字段配置校验
      console.log('开始字段配置校验...');
      console.log('当前字段数据:', this.columns);
      
      const validationResult = this.validateColumns();
      console.log('校验结果:', validationResult);
      
      if (!validationResult.valid) {
        // 使用更友好的弹窗显示错误信息
        this.$alert(validationResult.message, '字段配置校验失败', {
          confirmButtonText: '我知道了',
          type: 'warning',
          dangerouslyUseHTMLString: true,
          customClass: 'validation-error-dialog'
        });
        // 自动切换到字段信息标签页
        this.activeName = 'columnInfo';
        return;
      }

      const basicForm = this.$refs.basicInfo.$refs.basicInfoForm;
      const genForm = this.$refs.genInfo.$refs.genInfoForm;
      Promise.all([basicForm, genForm].map(this.getFormPromise)).then(res => {
        const validateResult = res.every(item => !!item);
        if (validateResult) {
          const genTable = Object.assign({}, basicForm.model, genForm.model);
          genTable.columns = this.columns;
          genTable.params = {
            treeCode: genTable.treeCode,
            treeName: genTable.treeName,
            treeParentCode: genTable.treeParentCode,
            parentMenuId: genTable.parentMenuId
          };
          updateGenTable(genTable).then(res => {
            this.$modal.msgSuccess(res.msg);
            if (res.code === 200) {
              this.close();
            }
          });
        } else {
          this.$modal.msgError("表单校验未通过，请重新检查提交内容");
        }
      });
    },
    /** 校验字段配置 */
    validateColumns() {
      const errors = [];
      
      this.columns.forEach((column, index) => {
        const rowNum = index + 1;
        const fieldName = column.columnComment || column.columnName;
        
        // 标准化字段值（将空字符串转为 null）
        const dictType = column.dictType && column.dictType.trim() !== '' ? column.dictType : null;
        const linkTable = column.linkTable && column.linkTable.trim() !== '' ? column.linkTable : null;
        
        // 调试日志
        console.log(`检查第 ${rowNum} 行 [${fieldName}]:`, {
          dictType: dictType,
          linkTable: linkTable,
          htmlType: column.htmlType,
          原始dictType: column.dictType,
          原始linkTable: column.linkTable
        });
        
        // 检查字典类型和关联表是否同时配置
        if (dictType && linkTable) {
          console.log(`发现冲突: 第 ${rowNum} 行 [${fieldName}] 同时配置了字典类型和关联表`);
          errors.push({
            row: rowNum,
            field: fieldName,
            message: '字典类型和关联表只能选择其中一个，不能同时配置',
            type: 'conflict'
          });
        }
        
        // 检查关联表配置的完整性
        if (linkTable) {
          // 只有下拉框、单选框、复选框才需要关联表
          if (!['select', 'radio', 'checkbox'].includes(column.htmlType)) {
            errors.push({
              row: rowNum,
              field: fieldName,
              message: '只有显示类型为"下拉框"、"单选框"或"复选框"时才能配置关联表',
              type: 'config'
            });
          } else {
            // 检查是否配置了标签字段和值字段
            const linkLabelField = column.linkLabelField && column.linkLabelField.trim() !== '' ? column.linkLabelField : null;
            const linkValueField = column.linkValueField && column.linkValueField.trim() !== '' ? column.linkValueField : null;
            
            if (!linkLabelField) {
              errors.push({
                row: rowNum,
                field: fieldName,
                message: '已配置关联表，但未选择标签字段',
                type: 'incomplete'
              });
            }
            if (!linkValueField) {
              errors.push({
                row: rowNum,
                field: fieldName,
                message: '已配置关联表，但未选择值字段',
                type: 'incomplete'
              });
            } else {
              // 检查关联表值字段类型与当前字段类型是否匹配
              const typeCheckResult = this.checkLinkFieldTypeMatch(column);
              if (!typeCheckResult.match) {
                errors.push({
                  row: rowNum,
                  field: fieldName,
                  message: `关联表值字段类型不匹配：当前字段类型为 ${column.columnType}(${column.pythonType})，关联表值字段类型为 ${typeCheckResult.linkFieldType}(${typeCheckResult.linkPythonType})`,
                  type: 'typeMismatch'
                });
              }
            }
          }
        }
        
        // 检查字典类型配置的合理性
        if (dictType) {
          // 只有下拉框、单选框、复选框才需要字典
          if (!['select', 'radio', 'checkbox'].includes(column.htmlType)) {
            errors.push({
              row: rowNum,
              field: fieldName,
              message: '只有显示类型为"下拉框"、"单选框"或"复选框"时才能配置字典类型',
              type: 'config'
            });
          }
        }
        
        // 检查下拉框、单选框、复选框是否配置了数据源
        if (['select', 'radio', 'checkbox'].includes(column.htmlType)) {
          if (!dictType && !linkTable) {
            errors.push({
              row: rowNum,
              field: fieldName,
              message: `显示类型为"${this.getHtmlTypeLabel(column.htmlType)}"时，必须配置字典类型或关联表作为数据源`,
              type: 'required'
            });
          }
        }
        
        // 检查必填字段
        if (!column.columnComment || column.columnComment.trim() === '') {
          errors.push({
            row: rowNum,
            field: column.columnName,
            message: '字段描述不能为空',
            type: 'required'
          });
        }
        
        if (!column.pythonField || column.pythonField.trim() === '') {
          errors.push({
            row: rowNum,
            field: fieldName,
            message: 'Python属性不能为空',
            type: 'required'
          });
        }
      });
      
      if (errors.length > 0) {
        // 构建友好的HTML格式错误提示信息
        let message = '<div style="text-align: left; max-height: 400px; overflow-y: auto;">';
        message += '<p style="margin-bottom: 10px; color: #606266;">请修正以下问题后再提交：</p>';
        message += '<ul style="margin: 0; padding-left: 20px; line-height: 1.8;">';
        
        errors.forEach((error, index) => {
          const icon = this.getErrorIcon(error.type);
          message += `<li style="margin-bottom: 8px;">`;
          message += `<span style="color: #909399;">第 ${error.row} 行</span> `;
          message += `<strong style="color: #409EFF;">[${error.field}]</strong>：`;
          message += `${icon} ${error.message}`;
          message += `</li>`;
        });
        
        message += '</ul></div>';
        
        return {
          valid: false,
          message: message
        };
      }
      
      return {
        valid: true,
        message: ''
      };
    },
    /** 检查关联表字段类型是否匹配 */
    checkLinkFieldTypeMatch(column) {
      if (!column.linkTable || !column.linkValueField) {
        return { match: true };
      }
      
      // 获取关联表信息
      const linkTable = this.tables.find(t => t.tableName === column.linkTable);
      if (!linkTable || !linkTable.tableId) {
        return { match: true }; // 找不到表信息，跳过检查
      }
      
      // 从已加载的表字段信息中查找
      // 注意：这里需要确保关联表的字段信息已经加载
      // 由于字段信息是异步加载的，我们需要从 columns 中查找同表的字段
      // 或者从缓存中获取
      
      // 简化方案：根据字段名和类型进行基本的类型兼容性检查
      const currentType = this.normalizeColumnType(column.columnType);
      const currentPythonType = column.pythonType;
      
      // 如果关联表字段信息已缓存，进行精确匹配
      if (this.linkTableFieldsCache && this.linkTableFieldsCache[column.linkTable]) {
        const linkFields = this.linkTableFieldsCache[column.linkTable];
        const linkField = linkFields.find(f => f.columnName === column.linkValueField);
        
        if (linkField) {
          const linkType = this.normalizeColumnType(linkField.columnType);
          const linkPythonType = linkField.pythonType;
          
          // 检查类型是否兼容
          const isCompatible = this.areTypesCompatible(currentType, linkType, currentPythonType, linkPythonType);
          
          return {
            match: isCompatible,
            linkFieldType: linkField.columnType,
            linkPythonType: linkPythonType
          };
        }
      }
      
      // 如果没有缓存信息，根据字段名进行启发式检查
      // 通常 id 字段应该是整数类型
      if (column.linkValueField.toLowerCase().includes('id')) {
        const isIntegerType = ['int', 'bigint', 'tinyint', 'smallint'].includes(currentType);
        if (!isIntegerType) {
          return {
            match: false,
            linkFieldType: 'bigint (推测)',
            linkPythonType: 'int (推测)'
          };
        }
      }
      
      return { match: true };
    },
    /** 标准化列类型 */
    normalizeColumnType(columnType) {
      if (!columnType) return '';
      // 移除括号及其内容，如 varchar(100) -> varchar
      return columnType.toLowerCase().replace(/\(.*?\)/g, '').trim();
    },
    /** 检查两个类型是否兼容 */
    areTypesCompatible(type1, type2, pythonType1, pythonType2) {
      // 完全相同
      if (type1 === type2 && pythonType1 === pythonType2) {
        return true;
      }
      
      // 整数类型组
      const integerTypes = ['int', 'bigint', 'tinyint', 'smallint', 'integer'];
      const isType1Integer = integerTypes.includes(type1);
      const isType2Integer = integerTypes.includes(type2);
      
      if (isType1Integer && isType2Integer) {
        return true; // 整数类型之间可以兼容
      }
      
      // 字符串类型组
      const stringTypes = ['varchar', 'char', 'text', 'mediumtext', 'longtext'];
      const isType1String = stringTypes.includes(type1);
      const isType2String = stringTypes.includes(type2);
      
      if (isType1String && isType2String) {
        return true; // 字符串类型之间可以兼容
      }
      
      // 数值类型组
      const numericTypes = ['decimal', 'float', 'double', 'numeric'];
      const isType1Numeric = numericTypes.includes(type1);
      const isType2Numeric = numericTypes.includes(type2);
      
      if (isType1Numeric && isType2Numeric) {
        return true; // 数值类型之间可以兼容
      }
      
      // 日期时间类型组
      const dateTimeTypes = ['datetime', 'timestamp', 'date', 'time'];
      const isType1DateTime = dateTimeTypes.includes(type1);
      const isType2DateTime = dateTimeTypes.includes(type2);
      
      if (isType1DateTime && isType2DateTime) {
        return true; // 日期时间类型之间可以兼容
      }
      
      return false; // 其他情况不兼容
    },
    /** 获取错误类型对应的图标 */
    getErrorIcon(type) {
      const iconMap = {
        'conflict': '<span style="color: #F56C6C;">⚠️</span>',
        'incomplete': '<span style="color: #E6A23C;">⚠️</span>',
        'required': '<span style="color: #F56C6C;">✖</span>',
        'config': '<span style="color: #E6A23C;">⚠️</span>',
        'typeMismatch': '<span style="color: #F56C6C;">🔴</span>'
      };
      return iconMap[type] || '•';
    },
    /** 获取显示类型的中文标签 */
    getHtmlTypeLabel(htmlType) {
      const typeMap = {
        'input': '文本框',
        'textarea': '文本域',
        'select': '下拉框',
        'radio': '单选框',
        'checkbox': '复选框',
        'datetime': '日期控件',
        'imageUpload': '图片上传',
        'fileUpload': '文件上传',
        'editor': '富文本'
      };
      return typeMap[htmlType] || htmlType;
    },
    getFormPromise(form) {
      return new Promise(resolve => {
        form.validate(res => {
          resolve(res);
        });
      });
    },
    /** 关闭按钮 */
    close() {
      const obj = { path: "/tool/gen", query: { t: Date.now(), pageNum: this.$route.query.pageNum } };
      this.$tab.closeOpenPage(obj);
    }
  },
  mounted() {
    const el = this.$refs.dragTable.$el.querySelectorAll(".el-table__body-wrapper > table > tbody")[0];
    const sortable = Sortable.create(el, {
      handle: ".allowDrag",
      onEnd: evt => {
        const targetRow = this.columns.splice(evt.oldIndex, 1)[0];
        this.columns.splice(evt.newIndex, 0, targetRow);
        for (let index in this.columns) {
          this.columns[index].sort = parseInt(index) + 1;
        }
      }
    });
  }
};
</script>


<style scoped lang="scss">
// 字段信息表格样式优化
::v-deep .gen-table {
  // 表格单元格紧凑布局
  .el-table__cell {
    padding: 6px 0;
  }
  
  // 输入框样式
  .el-input__inner {
    padding: 0 8px;
    height: 28px;
    line-height: 28px;
  }
  
  // 下拉框样式
  .el-select {
    .el-input__inner {
      padding-right: 25px;
    }
  }
  
  // 数字输入框样式
  .el-input-number {
    width: 100%;
    
    .el-input__inner {
      padding-left: 8px;
      padding-right: 40px;
    }
  }
  
  // 复选框居中
  .el-checkbox {
    display: flex;
    justify-content: center;
  }
  
  // 输入框前缀样式
  .el-input-group__prepend {
    padding: 0 8px;
    font-size: 12px;
    background-color: #f5f7fa;
  }
  
  // 优化滚动条样式和交互
  .el-table__body-wrapper {
    // 增加滚动条的可点击区域
    &::-webkit-scrollbar {
      width: 12px;
      height: 12px;
    }
    
    &::-webkit-scrollbar-track {
      background: #f1f1f1;
      border-radius: 6px;
    }
    
    &::-webkit-scrollbar-thumb {
      background: #c1c1c1;
      border-radius: 6px;
      border: 2px solid #f1f1f1;
      
      &:hover {
        background: #a8a8a8;
      }
      
      &:active {
        background: #787878;
      }
    }
    
    // 确保滚动条始终可见
    overflow-x: auto !important;
    overflow-y: auto !important;
  }
  
  // 表格内容区域增加内边距，避免内容被滚动条遮挡
  .el-table__body {
    padding-bottom: 2px;
  }
}

// 固定列样式
::v-deep .el-table__fixed-right {
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  z-index: 3;
}

::v-deep .el-table__fixed {
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  z-index: 3;
  
  // 固定列的表头
  .el-table__fixed-header-wrapper {
    background-color: #fff;
  }
  
  // 固定列的单元格
  .el-table__cell {
    background-color: #fff;
  }
  
  // 固定列的表体
  .el-table__fixed-body-wrapper {
    background-color: #fff;
  }
}

// 固定列在hover时的背景色
::v-deep .el-table__body tr.hover-row > td {
  background-color: #f5f7fa !important;
}

::v-deep .el-table__fixed .el-table__body tr.hover-row > td {
  background-color: #f5f7fa !important;
}

// 确保固定列的边框正常显示
::v-deep .el-table__fixed::before {
  background-color: transparent;
}

// 表格边框样式
::v-deep .el-table--border {
  border: 1px solid #ebeef5;
  
  th, td {
    border-right: 1px solid #ebeef5;
  }
}

// 表头样式
::v-deep .el-table__header {
  th {
    background-color: #f5f7fa;
    color: #606266;
    font-weight: 600;
    font-size: 13px;
  }
}

// 拖拽行样式
::v-deep .allowDrag {
  cursor: move;
  user-select: none;
}

// 关联表配置区域样式
.link-table-config {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

// 冲突提示样式
.conflict-tip {
  color: #F56C6C;
  font-size: 12px;
  line-height: 1.5;
  padding: 2px 0;
  
  i {
    margin-right: 4px;
  }
}

// 有冲突的选择框样式
::v-deep .has-conflict {
  .el-input__inner {
    border-color: #F56C6C !important;
    background-color: #fef0f0;
  }
}

// 必填字段未填写的样式
::v-deep .field-required {
  .el-input__inner {
    border-color: #E6A23C !important;
    background-color: #fdf6ec;
  }
}

// 校验错误弹窗样式
::v-deep .validation-error-dialog {
  width: 600px;
  max-width: 90%;
  
  .el-message-box__message {
    max-height: 450px;
    overflow-y: auto;
    
    // 美化滚动条
    &::-webkit-scrollbar {
      width: 8px;
    }
    
    &::-webkit-scrollbar-track {
      background: #f1f1f1;
      border-radius: 4px;
    }
    
    &::-webkit-scrollbar-thumb {
      background: #c1c1c1;
      border-radius: 4px;
      
      &:hover {
        background: #a8a8a8;
      }
    }
  }
  
  ul {
    list-style: none;
    
    li {
      padding: 6px 0;
      border-bottom: 1px solid #f0f0f0;
      
      &:last-child {
        border-bottom: none;
      }
      
      &:hover {
        background-color: #f5f7fa;
        padding-left: 8px;
        transition: all 0.2s;
      }
    }
  }
}

// 类型不匹配确认对话框样式
::v-deep .type-mismatch-confirm-dialog {
  width: 550px;
  max-width: 90%;
  
  .el-message-box__message {
    line-height: 1.6;
    
    p {
      margin: 8px 0;
    }
  }
  
  .el-message-box__btns {
    .el-button--primary {
      background-color: #E6A23C;
      border-color: #E6A23C;
      
      &:hover {
        background-color: #ebb563;
        border-color: #ebb563;
      }
    }
  }
}
</style>
