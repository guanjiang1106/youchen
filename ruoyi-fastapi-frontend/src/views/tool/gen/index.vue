<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="表名称" prop="tableName">
        <el-input
          v-model="queryParams.tableName"
          placeholder="请输入表名称"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="表描述" prop="tableComment">
        <el-input
          v-model="queryParams.tableComment"
          placeholder="请输入表描述"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="创建时间">
        <el-date-picker
          v-model="dateRange"
          style="width: 240px"
          value-format="yyyy-MM-dd"
          type="daterange"
          range-separator="-"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
        ></el-date-picker>
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
          icon="el-icon-download"
          size="mini"
          :disabled="multiple"
          @click="handleGenTable"
          v-hasPermi="['tool:gen:code']"
        >生成</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="el-icon-plus"
          size="mini"
          @click="openCreateTable"
          v-hasRole="['admin']"
        >创建</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="info"
          plain
          icon="el-icon-upload"
          size="mini"
          @click="openImportTable"
          v-hasPermi="['tool:gen:import']"
        >导入</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleEditTable"
          v-hasPermi="['tool:gen:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['tool:gen:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-question"
          size="mini"
          @click="handleGuide"
        >操作指南</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="tableList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" align="center" width="55"></el-table-column>
      <el-table-column label="序号" type="index" width="50" align="center">
        <template slot-scope="scope">
          <span>{{(queryParams.pageNum - 1) * queryParams.pageSize + scope.$index + 1}}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="表名称"
        align="center"
        prop="tableName"
        :show-overflow-tooltip="true"
        width="120"
      />
      <el-table-column
        label="表描述"
        align="center"
        prop="tableComment"
        :show-overflow-tooltip="true"
        width="120"
      />
      <el-table-column
        label="实体"
        align="center"
        prop="className"
        :show-overflow-tooltip="true"
        width="120"
      />
      <el-table-column label="创建时间" align="center" prop="createTime" width="160" />
      <el-table-column label="更新时间" align="center" prop="updateTime" width="160" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            type="text"
            size="small"
            icon="el-icon-view"
            @click="handlePreview(scope.row)"
            v-hasPermi="['tool:gen:preview']"
          >预览</el-button>
          <el-button
            type="text"
            size="small"
            icon="el-icon-edit"
            @click="handleEditTable(scope.row)"
            v-hasPermi="['tool:gen:edit']"
          >编辑</el-button>
          <el-button
            type="text"
            size="small"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['tool:gen:remove']"
          >删除</el-button>
          <el-button
            type="text"
            size="small"
            icon="el-icon-refresh"
            @click="handleSynchDb(scope.row)"
            v-hasPermi="['tool:gen:edit']"
          >同步</el-button>
          <el-button
            type="text"
            size="small"
            icon="el-icon-s-grid"
            @click="handleCreateMenu(scope.row)"
            v-hasPermi="['tool:gen:edit']"
          >生成菜单</el-button>
          <el-button
            type="text"
            size="small"
            icon="el-icon-download"
            @click="handleGenTable(scope.row)"
            v-hasPermi="['tool:gen:code']"
          >生成代码</el-button>
          <el-button
            type="text"
            size="small"
            icon="el-icon-magic-stick"
            @click="handleRefactor(scope.row)"
            v-hasPermi="['tool:gen:edit']"
          >界面重构</el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.pageNum"
      :limit.sync="queryParams.pageSize"
      @pagination="getList"
    />
    <!-- 预览界面 -->
    <el-dialog :title="preview.title" :visible.sync="preview.open" width="80%" top="5vh" append-to-body class="scrollbar">
      <el-tabs v-model="preview.activeName">
        <el-tab-pane
          v-for="(value, key) in preview.data"
          :label="key.substring(key.lastIndexOf('/')+1,key.indexOf('.jinja2'))"
          :name="key.substring(key.lastIndexOf('/')+1,key.indexOf('.jinja2'))"
          :key="key"
        >
          <el-link :underline="false" icon="el-icon-document-copy" v-clipboard:copy="value" v-clipboard:success="clipboardSuccess" style="float:right">复制</el-link>
          <pre><code class="hljs" v-html="highlightedCode(value, key)"></code></pre>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>
    <import-table ref="import" @ok="handleQuery" />
    <create-table ref="create" @ok="handleQuery" />
    <refactor-dialog ref="refactor" @ok="handleQuery" />
  </div>
</template>

<script>
import { listTable, previewTable, delTable, genCode, synchDb, createMenu } from "@/api/tool/gen";
import importTable from "./importTable";
import createTable from "./createTable";
import refactorDialog from "./refactorDialog";
import hljs from "highlight.js/lib/highlight";
import "highlight.js/styles/github-gist.css";
hljs.registerLanguage("py", require("highlight.js/lib/languages/python"));
hljs.registerLanguage("html", require("highlight.js/lib/languages/xml"));
hljs.registerLanguage("vue", require("highlight.js/lib/languages/xml"));
hljs.registerLanguage("javascript", require("highlight.js/lib/languages/javascript"));
hljs.registerLanguage("sql", require("highlight.js/lib/languages/sql"));

export default {
  name: "Gen",
  components: { importTable, createTable, refactorDialog },
  data() {
    return {
      // 遮罩层
      loading: true,
      // 唯一标识符
      uniqueId: "",
      // 选中数组
      ids: [],
      // 选中表数组
      tableNames: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 显示搜索条件
      showSearch: true,
      // 总条数
      total: 0,
      // 表数据
      tableList: [],
      // 日期范围
      dateRange: "",
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        tableName: undefined,
        tableComment: undefined
      },
      // 预览参数
      preview: {
        open: false,
        title: "代码预览",
        data: {},
        activeName: "do.py"
      }
    };
  },
  created() {
    this.getList();
  },
  activated() {
    const time = this.$route.query.t;
    if (time != null && time != this.uniqueId) {
      this.uniqueId = time;
      this.queryParams.pageNum = Number(this.$route.query.pageNum);
      this.getList();
    }
  },
  methods: {
    /** 查询表集合 */
    getList() {
      this.loading = true;
      listTable(this.addDateRange(this.queryParams, this.dateRange)).then(response => {
          this.tableList = response.rows;
          this.total = response.total;
          this.loading = false;
        }
      );
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    /** 生成代码操作 */
    handleGenTable(row) {
      const tableNames = row.tableName || this.tableNames;
      if (tableNames == "") {
        this.$modal.msgError("请选择要生成的数据");
        return;
      }
      if(row.genType === "1") {
        genCode(row.tableName).then(response => {
          // 显示后端返回的详细消息
          this.$modal.msgSuccess(response.msg || "生成代码成功");
        });
      } else {
        const zipName = Array.isArray(tableNames) ? "ruoyi.zip" : tableNames + ".zip"
        this.$download.zip("/tool/gen/batchGenCode?tables=" + tableNames, zipName)
      }
    },
    /** 同步数据库操作 */
    handleSynchDb(row) {
      const tableName = row.tableName;
      this.$modal.confirm('确认要强制同步"' + tableName + '"表结构吗？').then(function() {
        return synchDb(tableName);
      }).then(() => {
        this.$modal.msgSuccess("同步成功");
      }).catch(() => {});
    },

    /** 生成菜单操作 */
    handleCreateMenu(row) {
      const tableId = row.tableId;
      const tableName = row.tableName;
      this.$modal.confirm('确认要为"' + tableName + '"生成菜单吗？将根据生成信息配置自动创建菜单和按钮权限。', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function() {
        return createMenu(tableId);
      }).then((response) => {
        this.$modal.msgSuccess(response.msg || "菜单生成成功");
      }).catch(() => {});
    },

    /** 打开导入表弹窗 */
    openImportTable() {
      this.$refs.import.show();
    },
    /** 打开创建表弹窗 */
    openCreateTable() {
      this.$refs.create.show();
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.dateRange = [];
      this.resetForm("queryForm");
      this.handleQuery();
    },
    /** 预览按钮 */
    handlePreview(row) {
      previewTable(row.tableId).then(response => {
        this.preview.data = response.data;
        this.preview.open = true;
        this.preview.activeName = "do.py";
      });
    },
    /** 高亮显示 */
    highlightedCode(code, key) {
      const vmName = key.substring(key.lastIndexOf("/") + 1, key.indexOf(".jinja2"));
      var language = vmName.substring(vmName.indexOf(".") + 1, vmName.length);
      const result = hljs.highlight(language, code || "", true);
      return result.value || '&nbsp;';
    },
    /** 复制代码成功 */
    clipboardSuccess() {
      this.$modal.msgSuccess("复制成功");
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.tableId);
      this.tableNames = selection.map(item => item.tableName);
      this.single = selection.length != 1;
      this.multiple = !selection.length;
    },
    /** 修改按钮操作 */
    handleEditTable(row) {
      const tableId = row.tableId || this.ids[0];
      const tableName = row.tableName || this.tableNames[0];
      const params = { pageNum: this.queryParams.pageNum };
      this.$tab.openPage("修改[" + tableName + "]生成配置", '/tool/gen-edit/index/' + tableId, params);
    },
    /** 操作指南按钮 */
    handleGuide() {
      this.$tab.openPage("代码生成器操作指南", '/tool/gen-guide/index');
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      const tableIds = row.tableId || this.ids;
      const tableName = row.tableName || this.tableNames.join(',');
      
      // 构建详细的删除提示信息
      const deleteMessage = `
        <div style="text-align: left; line-height: 1.8;">
          <p style="margin-bottom: 10px;"><strong>删除后将同时删除以下内容：</strong></p>
          <p style="margin-left: 20px;">1. 数据库表（包括表结构和数据）</p>
          <p style="margin-left: 20px;">2. 数据库中的代码生成配置记录</p>
          <p style="margin-left: 20px;">3. 已生成到本地的相关代码文件（如果存在）：</p>
          <p style="margin-left: 40px;">• Controller 层文件</p>
          <p style="margin-left: 40px;">• Service 层文件</p>
          <p style="margin-left: 40px;">• DAO 层文件</p>
          <p style="margin-left: 40px;">• Entity 实体文件（DO/VO）</p>
          <p style="margin-left: 40px;">• 前端 Vue 页面和 API 文件</p>
          <p style="margin-top: 15px; color: #F56C6C;"><strong>此操作不可恢复，请谨慎操作！</strong></p>
        </div>
      `;
      
      // 使用 MessageBox 显示删除选项
      this.$confirm(
        deleteMessage,
        '确认删除表"' + tableName + '"吗？',
        {
          confirmButtonText: '确定删除',
          cancelButtonText: '取消',
          type: 'warning',
          distinguishCancelAndClose: true,
          showClose: true,
          closeOnClickModal: false,
          closeOnPressEscape: false,
          center: false,
          dangerouslyUseHTMLString: true
        }
      ).then(() => {
        return delTable(tableIds);
      }).then((response) => {
        this.getList();
        this.$modal.msgSuccess(response.msg || "删除成功");
      }).catch(action => {
        // 用户点击取消或关闭
        if (action === 'cancel') {
          // 可以添加取消提示
        }
      });
    },
    /** 界面重构操作 */
    handleRefactor(row) {
      this.$refs.refactor.show(row);
    }
  }
};
</script>
