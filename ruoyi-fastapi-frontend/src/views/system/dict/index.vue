<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="字典名称" prop="dictName">
        <el-input
          v-model="queryParams.dictName"
          placeholder="请输入字典名称"
          clearable
          style="width: 240px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="字典类型" prop="dictType">
        <el-input
          v-model="queryParams.dictType"
          placeholder="请输入字典类型"
          clearable
          style="width: 240px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select
          v-model="queryParams.status"
          placeholder="字典状态"
          clearable
          style="width: 240px"
        >
          <el-option
            v-for="dict in dict.type.sys_normal_disable"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
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
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
          v-hasPermi="['system:dict:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['system:dict:edit']"
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
          v-hasPermi="['system:dict:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['system:dict:export']"
        >导出</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-refresh"
          size="mini"
          @click="handleRefreshCache"
          v-hasPermi="['system:dict:remove']"
        >刷新缓存</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="typeList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="字典编号" align="center" prop="dictId" />
      <el-table-column label="字典名称" align="center" prop="dictName" :show-overflow-tooltip="true" />
      <el-table-column label="字典类型" align="center" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <router-link :to="'/system/dict-data/index/' + scope.row.dictId" class="link-type">
            <span>{{ scope.row.dictType }}</span>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column label="状态" align="center" prop="status">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.sys_normal_disable" :value="scope.row.status"/>
        </template>
      </el-table-column>
      <el-table-column label="备注" align="center" prop="remark" :show-overflow-tooltip="true" />
      <el-table-column label="创建时间" align="center" prop="createTime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.createTime) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['system:dict:edit']"
          >修改</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['system:dict:remove']"
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

    <!-- 添加或修改参数配置对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="800px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="字典名称" prop="dictName">
          <el-input v-model="form.dictName" placeholder="请输入字典名称" />
        </el-form-item>
        <el-form-item label="字典类型" prop="dictType">
          <el-input v-model="form.dictType" placeholder="请输入字典类型" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio
              v-for="dict in dict.type.sys_normal_disable"
              :key="dict.value"
              :label="dict.value"
            >{{dict.label}}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" placeholder="请输入内容"></el-input>
        </el-form-item>
        
        <!-- 字典数据管理 -->
        <el-divider v-if="form.dictId" content-position="left">字典数据</el-divider>
        <div v-if="form.dictId">
          <el-button type="primary" size="small" icon="el-icon-plus" @click="handleAddData" style="margin-bottom: 10px">新增字典数据</el-button>
          <el-table :data="dictDataList" border size="small" max-height="300">
            <el-table-column label="字典标签" prop="dictLabel" width="120">
              <template slot-scope="scope">
                <el-input v-if="scope.row.editing" v-model="scope.row.dictLabel" size="small" placeholder="请输入标签"></el-input>
                <span v-else>{{ scope.row.dictLabel }}</span>
              </template>
            </el-table-column>
            <el-table-column label="字典键值" prop="dictValue" width="100">
              <template slot-scope="scope">
                <el-input v-if="scope.row.editing" v-model="scope.row.dictValue" size="small" placeholder="请输入键值"></el-input>
                <span v-else>{{ scope.row.dictValue }}</span>
              </template>
            </el-table-column>
            <el-table-column label="排序" prop="dictSort" width="80">
              <template slot-scope="scope">
                <el-input-number v-if="scope.row.editing" v-model="scope.row.dictSort" size="small" :min="0" controls-position="right"></el-input-number>
                <span v-else>{{ scope.row.dictSort }}</span>
              </template>
            </el-table-column>
            <el-table-column label="状态" prop="status" width="100">
              <template slot-scope="scope">
                <el-select v-if="scope.row.editing" v-model="scope.row.status" size="small">
                  <el-option label="正常" value="0"></el-option>
                  <el-option label="停用" value="1"></el-option>
                </el-select>
                <dict-tag v-else :options="dict.type.sys_normal_disable" :value="scope.row.status"/>
              </template>
            </el-table-column>
            <el-table-column label="备注" prop="remark" show-overflow-tooltip>
              <template slot-scope="scope">
                <el-input v-if="scope.row.editing" v-model="scope.row.remark" size="small" placeholder="请输入备注"></el-input>
                <span v-else>{{ scope.row.remark }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120" align="center">
              <template slot-scope="scope">
                <el-button v-if="scope.row.editing" type="text" size="small" @click="handleSaveData(scope.row, scope.$index)">保存</el-button>
                <el-button v-if="scope.row.editing" type="text" size="small" @click="handleCancelData(scope.row, scope.$index)">取消</el-button>
                <el-button v-if="!scope.row.editing" type="text" size="small" @click="handleEditData(scope.row)">编辑</el-button>
                <el-button v-if="!scope.row.editing" type="text" size="small" @click="handleDeleteData(scope.row, scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { listType, getType, delType, addType, updateType, refreshCache } from "@/api/system/dict/type";
import { listData, getData, delData, addData, updateData } from "@/api/system/dict/data";

export default {
  name: "Dict",
  dicts: ['sys_normal_disable'],
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
      // 字典表格数据
      typeList: [],
      // 字典数据列表
      dictDataList: [],
      // 字典数据备份（用于取消编辑）
      dictDataBackup: {},
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 日期范围
      dateRange: [],
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        dictName: undefined,
        dictType: undefined,
        status: undefined
      },
      // 表单参数
      form: {},
      // 表单校验
      rules: {
        dictName: [
          { required: true, message: "字典名称不能为空", trigger: "blur" }
        ],
        dictType: [
          { required: true, message: "字典类型不能为空", trigger: "blur" }
        ]
      }
    };
  },
  created() {
    this.getList();
  },
  methods: {
    /** 查询字典类型列表 */
    getList() {
      this.loading = true;
      listType(this.addDateRange(this.queryParams, this.dateRange)).then(response => {
          this.typeList = response.rows;
          this.total = response.total;
          this.loading = false;
        }
      );
    },
    // 取消按钮
    cancel() {
      this.open = false;
      this.reset();
    },
    // 表单重置
    reset() {
      this.form = {
        dictId: undefined,
        dictName: undefined,
        dictType: undefined,
        status: "0",
        remark: undefined
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
      this.dateRange = [];
      this.resetForm("queryForm");
      this.handleQuery();
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加字典类型";
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.dictId)
      this.single = selection.length!=1
      this.multiple = !selection.length
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const dictId = row.dictId || this.ids
      getType(dictId).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改字典类型";
        // 加载字典数据
        this.getDictDataList(dictId);
      });
    },
    /** 获取字典数据列表 */
    getDictDataList(dictId) {
      listData({ dictType: this.form.dictType, pageNum: 1, pageSize: 100 }).then(response => {
        this.dictDataList = response.rows.map(item => ({
          ...item,
          editing: false
        }));
      });
    },
    /** 新增字典数据 */
    handleAddData() {
      const newData = {
        dictCode: null,
        dictLabel: '',
        dictValue: '',
        dictType: this.form.dictType,
        dictSort: this.dictDataList.length + 1,
        status: '0',
        remark: '',
        editing: true,
        isNew: true
      };
      this.dictDataList.push(newData);
    },
    /** 编辑字典数据 */
    handleEditData(row) {
      // 备份原始数据
      this.dictDataBackup[row.dictCode] = { ...row };
      this.$set(row, 'editing', true);
    },
    /** 保存字典数据 */
    handleSaveData(row, index) {
      if (!row.dictLabel || !row.dictValue) {
        this.$modal.msgWarning("字典标签和键值不能为空");
        return;
      }
      
      if (row.isNew) {
        // 新增
        addData(row).then(response => {
          this.$modal.msgSuccess("新增成功");
          this.getDictDataList(this.form.dictId);
        });
      } else {
        // 修改
        updateData(row).then(response => {
          this.$modal.msgSuccess("修改成功");
          this.$set(row, 'editing', false);
          delete this.dictDataBackup[row.dictCode];
        });
      }
    },
    /** 取消编辑字典数据 */
    handleCancelData(row, index) {
      if (row.isNew) {
        // 新增的直接删除
        this.dictDataList.splice(index, 1);
      } else {
        // 恢复原始数据
        Object.assign(row, this.dictDataBackup[row.dictCode]);
        this.$set(row, 'editing', false);
        delete this.dictDataBackup[row.dictCode];
      }
    },
    /** 删除字典数据 */
    handleDeleteData(row, index) {
      this.$modal.confirm('是否确认删除字典标签为"' + row.dictLabel + '"的数据项？').then(() => {
        return delData(row.dictCode);
      }).then(() => {
        this.dictDataList.splice(index, 1);
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {});
    },
    /** 提交按钮 */
    submitForm: function() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          if (this.form.dictId != undefined) {
            updateType(this.form).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addType(this.form).then(response => {
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
      const dictIds = row.dictId || this.ids;
      this.$modal.confirm('是否确认删除字典编号为"' + dictIds + '"的数据项？').then(function() {
        return delType(dictIds);
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {});
    },
    /** 导出按钮操作 */
    handleExport() {
      this.download('system/dict/type/export', {
        ...this.queryParams
      }, `type_${new Date().getTime()}.xlsx`)
    },
    /** 刷新缓存按钮操作 */
    handleRefreshCache() {
      refreshCache().then(() => {
        this.$modal.msgSuccess("刷新成功");
        this.$store.dispatch('dict/cleanDict');
      });
    }
  }
};
</script>