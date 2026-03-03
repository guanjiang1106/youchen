<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="产品编码" prop="productCode">
        <el-input
          v-model="queryParams.productCode"
          placeholder="请输入产品编码"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="生产批次号" prop="batchNumber">
        <el-input
          v-model="queryParams.batchNumber"
          placeholder="请输入生产批次号"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="检验结果 (0:待检，1:合格，2:不合格)" prop="inspectionResult">
        <el-select
          v-model="queryParams.inspectionResult"
          placeholder="请选择检验结果"
          clearable
        >
          <el-option label="待检" value="0" />
          <el-option label="合格" value="1" />
          <el-option label="不合格" value="2" />
        </el-select>
      </el-form-item>
      <el-form-item label="缺陷数量" prop="defectCount">
        <el-input
          v-model="queryParams.defectCount"
          placeholder="请输入缺陷数量"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="检验员姓名" prop="inspectorName">
        <el-input
          v-model="queryParams.inspectorName"
          placeholder="请输入检验员姓名"
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
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
          v-hasPermi="['module_admin:table:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="el-icon-edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['module_admin:table:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['module_admin:table:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          @click="handleExport"
          v-hasPermi="['module_admin:table:export']"
        >导出</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="info"
          plain
          icon="el-icon-s-operation"
          @click="handleGenerateRandom"
          v-hasPermi="['module_admin:table:random']"
        >随机数</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="tableList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="主键 ID" align="center" prop="id" />
      <el-table-column label="产品编码" align="center" prop="productCode" />
      <el-table-column label="生产批次号" align="center" prop="batchNumber" />
      <el-table-column label="检验结果" align="center" prop="inspectionResult">
        <template slot-scope="scope">
          <el-tag
            :type="getInspectionResultTag(scope.row.inspectionResult)"
            disable-transitions
          >{{ inspectionResultFormat(scope.row.inspectionResult) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="缺陷数量" align="center" prop="defectCount" />
      <el-table-column label="检验员姓名" align="center" prop="inspectorName" />
      <el-table-column label="备注说明" align="center" prop="remarks" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['module_admin:table:edit']"
          >修改</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['module_admin:table:remove']"
          >删除</el-button>
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

    <!-- 添加或修改质量检验记录对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="产品编码" prop="productCode">
          <el-input v-model="form.productCode" placeholder="请输入产品编码" />
        </el-form-item>
        <el-form-item label="生产批次号" prop="batchNumber">
          <el-input v-model="form.batchNumber" placeholder="请输入生产批次号" />
        </el-form-item>
        <el-form-item label="检验结果" prop="inspectionResult">
          <el-select v-model="form.inspectionResult" placeholder="请选择检验结果">
            <el-option label="待检" value="0" />
            <el-option label="合格" value="1" />
            <el-option label="不合格" value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="缺陷数量" prop="defectCount">
          <el-input-number v-model="form.defectCount" :min="0" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="检验员姓名" prop="inspectorName">
          <el-input v-model="form.inspectorName" placeholder="请输入检验员姓名" />
        </el-form-item>
        <el-form-item label="备注说明" prop="remarks">
          <el-input v-model="form.remarks" type="textarea" placeholder="请输入内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { listTable, getTable, delTable, addTable, updateTable, generateRandomData } from "@/api/module_admin/table";

export default {
  name: "Table",
  data() {
    return {
      // 遮罩层
      loading: true,
      // 选中数组
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 显示搜索条件
      showSearch: true,
      // 总条数
      total: 0,
      // 质量检验记录表格数据
      tableList: [],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        productCode: null,
        batchNumber: null,
        inspectionResult: null,
        defectCount: null,
        inspectorName: null,
      },
      // 表单参数
      form: {},
      // 表单校验
      rules: {
        productCode: [
          { required: true, message: "产品编码不能为空", trigger: "blur" }
        ],
        batchNumber: [
          { required: true, message: "生产批次号不能为空", trigger: "blur" }
        ],
        inspectionResult: [
          { required: true, message: "检验结果不能为空", trigger: "change" }
        ],
        defectCount: [
          { required: true, message: "缺陷数量不能为空", trigger: "blur" }
        ],
      }
    };
  },
  created() {
    this.getList();
  },
  methods: {
    /** 检验结果状态字典翻译 */
    inspectionResultFormat(value) {
      if (value === '0') return '待检';
      if (value === '1') return '合格';
      if (value === '2') return '不合格';
      return '';
    },
    /** 检验结果状态颜色映射 */
    getInspectionResultTag(value) {
      if (value === '0') return 'info';
      if (value === '1') return 'success';
      if (value === '2') return 'danger';
      return '';
    },
    /** 查询质量检验记录列表 */
    getList() {
      this.loading = true;
      listTable(this.queryParams).then(response => {
        this.tableList = response.rows;
        this.total = response.total;
        this.loading = false;
      });
    },
    /** 取消按钮 */
    cancel() {
      this.open = false;
      this.reset();
    },
    /** 表单重置 */
    reset() {
      this.form = {
        id: null,
        productCode: null,
        batchNumber: null,
        inspectionResult: null,
        defectCount: null,
        inspectorName: null,
        remarks: null,
      };
      this.resetForm("form");
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.resetForm("queryForm");
      this.handleQuery();
    },
    /** 多选框选中数据  */
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.id);
      this.single = selection.length != 1;
      this.multiple = !selection.length;
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加质量检验记录";
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const id = row.id || this.ids;
      getTable(id).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改质量检验记录";
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          if (this.form.id != null) {
            updateTable(this.form).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addTable(this.form).then(response => {
              this.$modal.msgSuccess("新增成功");
              this.open = false;
              this.getList();
            });
          }
        }
      });
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      const ids = row.id || this.ids;
      this.$modal.confirm('是否确认删除质量检验记录编号为"' + ids + '"的数据项？').then(function() {
        return delTable(ids);
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {});
    },
    /** 导出按钮操作 */
    handleExport() {
      this.download('module_admin/table/export', {
        ...this.queryParams
      }, `table_${new Date().getTime()}.xlsx`);
    },
    /** 生成随机数据按钮操作 */
    handleGenerateRandom() {
      this.$modal.confirm('是否确认生成随机质量检验记录数据？').then(function() {
        return generateRandomData();
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("生成成功");
      }).catch(() => {});
    }
  },
};
</script>