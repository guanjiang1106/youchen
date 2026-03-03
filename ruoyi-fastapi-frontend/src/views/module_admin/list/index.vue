<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="设备编码" prop="deviceCode">
        <el-input
          v-model="queryParams.deviceCode"
          placeholder="请输入设备编码"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="设备名称" prop="deviceName">
        <el-input
          v-model="queryParams.deviceName"
          placeholder="请输入设备名称"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="设备类型" prop="deviceType">
        <el-input
          v-model="queryParams.deviceType"
          placeholder="请输入设备类型"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="品牌" prop="brand">
        <el-input
          v-model="queryParams.brand"
          placeholder="请输入品牌"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="型号" prop="model">
        <el-input
          v-model="queryParams.model"
          placeholder="请输入型号"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="序列号" prop="serialNumber">
        <el-input
          v-model="queryParams.serialNumber"
          placeholder="请输入序列号"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="购买日期" prop="purchaseDate">
        <el-date-picker
          v-model="queryParams.purchaseDate"
          type="date"
          value-format="yyyy-MM-dd"
          placeholder="请选择购买日期"
          clearable
        />
      </el-form-item>
      <el-form-item label="保修期" prop="warrantyPeriod">
        <el-input
          v-model="queryParams.warrantyPeriod"
          placeholder="请输入保修期"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-input
          v-model="queryParams.status"
          placeholder="请输入状态"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="存放位置" prop="location">
        <el-input
          v-model="queryParams.location"
          placeholder="请输入存放位置"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="所属部门" prop="department">
        <el-input
          v-model="queryParams.department"
          placeholder="请输入所属部门"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="责任人" prop="responsiblePerson">
        <el-input
          v-model="queryParams.responsiblePerson"
          placeholder="请输入责任人"
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
          v-hasPermi="['module_admin:list:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="el-icon-edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['module_admin:list:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['module_admin:list:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          @click="handleExport"
          v-hasPermi="['module_admin:list:export']"
        >导出</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="info"
          plain
          icon="el-icon-s-operation"
          @click="handleGenerateRandom"
          v-hasPermi="['module_admin:list:random']"
        >随机</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="listList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="主键 ID" align="center" prop="id" />
      <el-table-column label="设备编码" align="center" prop="deviceCode" />
      <el-table-column label="设备名称" align="center" prop="deviceName" />
      <el-table-column label="设备类型" align="center" prop="deviceType" />
      <el-table-column label="品牌" align="center" prop="brand" />
      <el-table-column label="型号" align="center" prop="model" />
      <el-table-column label="序列号" align="center" prop="serialNumber" />
      <el-table-column label="购买日期" align="center" prop="purchaseDate" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.purchaseDate, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="保修期" align="center" prop="warrantyPeriod" />
      <el-table-column label="状态" align="center" prop="status" />
      <el-table-column label="存放位置" align="center" prop="location" />
      <el-table-column label="所属部门" align="center" prop="department" />
      <el-table-column label="责任人" align="center" prop="responsiblePerson" />
      <el-table-column label="备注" align="center" prop="remarks" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['module_admin:list:edit']"
          >修改</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['module_admin:list:remove']"
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

    <!-- 添加或修改设备清单对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="设备编码" prop="deviceCode">
        <el-input v-model="form.deviceCode" placeholder="请输入设备编码" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="设备名称" prop="deviceName">
        <el-input v-model="form.deviceName" placeholder="请输入设备名称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="设备类型" prop="deviceType">
        <el-input v-model="form.deviceType" placeholder="请输入设备类型" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="品牌" prop="brand">
        <el-input v-model="form.brand" placeholder="请输入品牌" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="型号" prop="model">
        <el-input v-model="form.model" placeholder="请输入型号" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="序列号" prop="serialNumber">
        <el-input v-model="form.serialNumber" placeholder="请输入序列号" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="购买日期" prop="purchaseDate">
        <el-date-picker clearable
          v-model="form.purchaseDate"
          type="date"
          value-format="yyyy-MM-dd"
          placeholder="请选择购买日期">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="保修期" prop="warrantyPeriod">
        <el-input v-model="form.warrantyPeriod" placeholder="请输入保修期" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="状态" prop="status">
        <el-input v-model="form.status" placeholder="请输入状态" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="存放位置" prop="location">
        <el-input v-model="form.location" placeholder="请输入存放位置" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="所属部门" prop="department">
        <el-input v-model="form.department" placeholder="请输入所属部门" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="责任人" prop="responsiblePerson">
        <el-input v-model="form.responsiblePerson" placeholder="请输入责任人" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="备注" prop="remarks">
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

    <!-- 生成随机数据对话框 -->
    <el-dialog title="生成随机数据" :visible.sync="openGenerate" width="300px" append-to-body>
      <el-form ref="generateForm" :model="generateForm" label-width="80px">
        <el-form-item label="数量" prop="count">
          <el-input-number v-model="generateForm.count" :min="1" :max="100" style="width: 100%;" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitGenerateForm">确 定</el-button>
          <el-button @click="openGenerate = false">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { listList, getList, delList, addList, updateList, generateRandom } from "@/api/module_admin/list";

export default {
  name: "List",
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
      // 设备清单表格数据
      listList: [],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 是否显示生成随机数据弹出层
      openGenerate: false,
      // 当前激活的标签页
      activeTabName: 'basic',
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        deviceCode: null,
        deviceName: null,
        deviceType: null,
        brand: null,
        model: null,
        serialNumber: null,
        purchaseDate: null,
        warrantyPeriod: null,
        status: null,
        location: null,
        department: null,
        responsiblePerson: null,
        remarks: null,
      },
      // 表单参数
      form: {},
      // 生成随机数据表单参数
      generateForm: {
        count: 10
      },
      // 表单校验
      rules: {
      }
    };
  },
  created() {
    this.getList();
  },
  methods: {
    /** 查询设备清单列表 */
    getList() {
      this.loading = true;
      listList(this.queryParams).then(response => {
        this.listList = response.rows;
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
        deviceCode: null,
        deviceName: null,
        deviceType: null,
        brand: null,
        model: null,
        serialNumber: null,
        purchaseDate: null,
        warrantyPeriod: null,
        status: null,
        location: null,
        department: null,
        responsiblePerson: null,
        remarks: null,
        createTime: null,
        updateTime: null,
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
      this.activeTabName = 'basic';
      this.open = true;
      this.title = "添加设备清单";
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      this.activeTabName = 'basic';
      const id = row.id || this.ids;
      getList(id).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改设备清单";
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          if (this.form.id != null) {
            updateList(this.form).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addList(this.form).then(response => {
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
      this.$modal.confirm('是否确认删除设备清单编号为"' + ids + '"的数据项？').then(function() {
        return delList(ids);
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {});
    },
    /** 导出按钮操作 */
    handleExport() {
      this.download('module_admin/list/export', {
        ...this.queryParams
      }, `list_${new Date().getTime()}.xlsx`);
    },
    /** 是否渲染字段 */
    renderField(insert, edit) {
      return this.form.id == null ? insert : edit;
    },
    /** 生成随机数据按钮操作 */
    handleGenerateRandom() {
      this.generateForm = { count: 10 };
      this.openGenerate = true;
    },
    /** 提交生成随机数据表单 */
    submitGenerateForm() {
      this.$refs["generateForm"].validate(valid => {
        if (valid) {
          generateRandom(this.generateForm.count).then(response => {
            this.$modal.msgSuccess(response.msg);
            this.openGenerate = false;
            this.getList();
          });
        }
      });
    }
  },
};
</script>