<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="工艺编码" prop="processCode">
        <el-input
          v-model="queryParams.processCode"
          placeholder="请输入工艺编码"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="工艺名称" prop="processName">
        <el-input
          v-model="queryParams.processName"
          placeholder="请输入工艺名称"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="工艺类型" prop="processType">
        <el-select v-model="queryParams.processType" placeholder="请选择工艺类型" clearable>
          <el-option label="类型 1" value="1" />
          <el-option label="类型 2" value="2" />
          <el-option label="类型 3" value="3" />
        </el-select>
      </el-form-item>
      <el-form-item label="所需设备" prop="requiredEquipment">
        <el-input
          v-model="queryParams.requiredEquipment"
          placeholder="请输入所需设备"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="操作员等级要求" prop="operatorLevel">
        <el-input-number v-model="queryParams.operatorLevel" :min="1" :max="5" placeholder="请输入等级" style="width: 100px" />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择状态" clearable>
          <el-option label="启用" value="1" />
          <el-option label="禁用" value="0" />
        </el-select>
      </el-form-item>
      <el-form-item label="版本号" prop="version">
        <el-input
          v-model="queryParams.version"
          placeholder="请输入版本号"
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
          v-hasPermi="['module_admin:info:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="el-icon-edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['module_admin:info:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['module_admin:info:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          @click="handleExport"
          v-hasPermi="['module_admin:info:export']"
        >导出</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="info"
          plain
          icon="el-icon-s-operation"
          @click="handleGenerateRandom"
          v-hasPermi="['module_admin:info:generate_random_data']"
        >生成随机数据</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="infoList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="主键 ID" align="center" prop="id" />
      <el-table-column label="工艺编码" align="center" prop="processCode" />
      <el-table-column label="工艺名称" align="center" prop="processName" />
      <el-table-column label="工艺类型" align="center" prop="processType">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.processType == 1" type="success">类型 1</el-tag>
          <el-tag v-else-if="scope.row.processType == 2" type="warning">类型 2</el-tag>
          <el-tag v-else-if="scope.row.processType == 3" type="danger">类型 3</el-tag>
          <span v-else>{{ scope.row.processType }}</span>
        </template>
      </el-table-column>
      <el-table-column label="工艺描述" align="center" prop="description" :show-overflow-tooltip="true" />
      <el-table-column label="标准工时" align="center" prop="standardHours" />
      <el-table-column label="所需设备" align="center" prop="requiredEquipment" />
      <el-table-column label="操作员等级要求" align="center" prop="operatorLevel" />
      <el-table-column label="状态" align="center" prop="status">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.status"
            active-value="1"
            inactive-value="0"
            @change="handleStatusChange(scope.row)"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column label="版本号" align="center" prop="version" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['module_admin:info:edit']"
          >修改</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['module_admin:info:remove']"
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

    <!-- 添加或修改工艺信息对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="工艺编码" prop="processCode">
          <el-input v-model="form.processCode" placeholder="请输入工艺编码" />
        </el-form-item>
        <el-form-item label="工艺名称" prop="processName">
          <el-input v-model="form.processName" placeholder="请输入工艺名称" />
        </el-form-item>
        <el-form-item label="工艺类型" prop="processType">
          <el-select v-model="form.processType" placeholder="请选择工艺类型">
            <el-option label="类型 1" value="1" />
            <el-option label="类型 2" value="2" />
            <el-option label="类型 3" value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="工艺描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="请输入内容" />
        </el-form-item>
        <el-form-item label="标准工时" prop="standardHours">
          <el-input-number v-model="form.standardHours" :precision="2" :step="0.5" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="所需设备" prop="requiredEquipment">
          <el-input v-model="form.requiredEquipment" placeholder="请输入所需设备" />
        </el-form-item>
        <el-form-item label="操作员等级" prop="operatorLevel">
          <el-input-number v-model="form.operatorLevel" :min="1" :max="5" style="width: 100%" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio label="1">启用</el-radio>
            <el-radio label="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="版本号" prop="version">
          <el-input v-model="form.version" placeholder="请输入版本号" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 生成随机数据对话框 -->
    <el-dialog title="生成随机数据" :visible.sync="randomOpen" width="400px" append-to-body>
      <el-form ref="randomForm" :model="randomForm" :rules="randomRules" label-width="80px">
        <el-form-item label="生成数量" prop="count">
          <el-input-number v-model="randomForm.count" :min="1" :max="100" :step="1" style="width: 100%" />
          <div style="color: #999; font-size: 12px; margin-top: 5px;">单次最多生成 100 条数据</div>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitRandomForm">确 定</el-button>
        <el-button @click="randomOpen = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { listInfo, getInfo, delInfo, addInfo, updateInfo, generateRandomData } from "@/api/module_admin/info";

export default {
  name: "Info",
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
      // 工艺信息表格数据
      infoList: [],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 是否显示生成随机数据弹出层
      randomOpen: false,
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        processCode: null,
        processName: null,
        processType: null,
        description: null,
        standardHours: null,
        requiredEquipment: null,
        operatorLevel: null,
        status: null,
        version: null,
      },
      // 表单参数
      form: {},
      // 随机数据表单参数
      randomForm: {
        count: 10
      },
      // 表单校验
      rules: {
        processCode: [
          { required: true, message: "工艺编码不能为空", trigger: "blur" }
        ],
        processName: [
          { required: true, message: "工艺名称不能为空", trigger: "blur" }
        ],
        processType: [
          { required: true, message: "工艺类型不能为空", trigger: "change" }
        ],
        status: [
          { required: true, message: "状态不能为空", trigger: "change" }
        ]
      },
      // 随机数据表单校验
      randomRules: {
        count: [
          { required: true, message: "请输入生成数量", trigger: "blur" },
          { type: 'number', min: 1, max: 100, message: "数量必须在 1 到 100 之间", trigger: "blur" }
        ]
      }
    };
  },
  created() {
    this.getList();
  },
  methods: {
    /** 查询工艺信息列表 */
    getList() {
      this.loading = true;
      listInfo(this.queryParams).then(response => {
        this.infoList = response.rows;
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
        processCode: null,
        processName: null,
        processType: null,
        description: null,
        standardHours: null,
        requiredEquipment: null,
        operatorLevel: null,
        status: "1",
        version: null,
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
      this.open = true;
      this.title = "添加工艺信息";
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const id = row.id || this.ids;
      getInfo(id).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改工艺信息";
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          if (this.form.id != null) {
            updateInfo(this.form).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addInfo(this.form).then(response => {
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
      this.$modal.confirm('是否确认删除工艺信息编号为"' + ids + '"的数据项？').then(function() {
        return delInfo(ids);
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {});
    },
    /** 导出按钮操作 */
    handleExport() {
      this.download('module_admin/info/export', {
        ...this.queryParams
      }, `info_${new Date().getTime()}.xlsx`);
    },
    /** 生成随机数据按钮操作 */
    handleGenerateRandom() {
      this.randomForm = { count: 10 };
      this.randomOpen = true;
    },
    /** 提交生成随机数据表单 */
    submitRandomForm() {
      this.$refs["randomForm"].validate(valid => {
        if (valid) {
          generateRandomData(this.randomForm.count).then(response => {
            this.$modal.msgSuccess(response.msg);
            this.randomOpen = false;
            this.getList();
          });
        }
      });
    },
    /** 对象状态修改 */
    handleStatusChange(row) {
      let text = row.status === "1" ? "启用" : "禁用";
      this.$modal.confirm('确认要"' + text + '""' + row.processName + '"工艺信息吗？').then(() => {
        return updateInfo(row);
      }).then(() => {
        this.$modal.msgSuccess(text + "成功");
      }).catch(function() {
        row.status = row.status === "1" ? "0" : "1";
      });
    }
  },
};
</script>