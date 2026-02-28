<template>
  <!-- 创建表 -->
  <el-dialog title="AI智能创建表" :visible.sync="visible" width="900px" top="5vh" append-to-body>
    <!-- 第一步：输入需求 -->
    <div v-if="step === 1">
      <el-form :model="form" label-width="100px">
        <el-form-item label="选择模型" required>
          <el-select
            v-model="form.modelId"
            placeholder="请选择AI模型"
            style="width: 100%"
            @change="handleModelChange"
          >
            <el-option
              v-for="model in modelList"
              :key="model.modelId"
              :label="model.modelName + ' (' + model.modelCode + ')'"
              :value="model.modelId"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="表需求描述" required>
          <el-input
            type="textarea"
            :rows="8"
            placeholder="请描述您想要创建的表，例如：&#10;创建一个用户积分表，包含用户ID、积分数量、获取时间、积分来源等字段"
            v-model="form.requirement"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="handleGenerateSQL" :loading="generating">
          {{ generating ? '生成中...' : '生成SQL' }}
        </el-button>
        <el-button @click="visible = false">取 消</el-button>
      </div>
    </div>

    <!-- 第二步：确认SQL -->
    <div v-if="step === 2">
      <el-alert
        title="AI已生成建表语句，请检查并修改后确认执行"
        type="success"
        :closable="false"
        style="margin-bottom: 15px"
      ></el-alert>
      <span>创建表语句(支持多个建表语句)：</span>
      <el-input
        type="textarea"
        :rows="15"
        placeholder="请输入文本"
        v-model="content"
        style="margin-top: 10px"
      ></el-input>
      <div slot="footer" class="dialog-footer" style="margin-top: 15px">
        <el-button @click="step = 1">上一步</el-button>
        <el-button type="primary" @click="handleCreateTable">确认执行</el-button>
        <el-button @click="visible = false">取 消</el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script>
import { createTable, generateTableSQL } from "@/api/tool/gen";
import { listModelAll } from "@/api/ai/model";

export default {
  data() {
    return {
      // 遮罩层
      visible: false,
      // 当前步骤
      step: 1,
      // 生成中
      generating: false,
      // 模型列表
      modelList: [],
      // 表单数据
      form: {
        modelId: undefined,
        requirement: "",
      },
      // SQL文本内容
      content: "",
    };
  },
  methods: {
    // 显示弹框
    show() {
      this.visible = true;
      this.step = 1;
      this.form = {
        modelId: undefined,
        requirement: "",
      };
      this.content = "";
      this.loadModelList();
    },
    // 加载模型列表
    loadModelList() {
      listModelAll().then((response) => {
        this.modelList = response.data || [];
        // 默认选择第一个模型
        if (this.modelList.length > 0) {
          this.form.modelId = this.modelList[0].modelId;
        }
      });
    },
    // 模型变化
    handleModelChange(modelId) {
      // 可以在这里添加模型切换的逻辑
    },
    // 生成SQL
    handleGenerateSQL() {
      if (!this.form.modelId) {
        this.$modal.msgError("请选择AI模型");
        return;
      }
      if (!this.form.requirement || this.form.requirement.trim() === "") {
        this.$modal.msgError("请输入表需求描述");
        return;
      }

      this.generating = true;
      generateTableSQL({
        modelId: this.form.modelId,
        requirement: this.form.requirement,
      })
        .then((res) => {
          if (res.code === 200) {
            this.content = res.data;
            this.step = 2;
            this.$modal.msgSuccess("SQL生成成功，请检查后确认执行");
          }
        })
        .catch((error) => {
          this.$modal.msgError("生成失败：" + (error.msg || "未知错误"));
        })
        .finally(() => {
          this.generating = false;
        });
    },
    /** 创建按钮操作 */
    handleCreateTable() {
      if (this.content === "") {
        this.$modal.msgError("请输入建表语句");
        return;
      }
      createTable({ sql: this.content })
        .then((res) => {
          this.$modal.msgSuccess(res.msg);
          if (res.code === 200) {
            this.visible = false;
            this.$emit("ok");
          }
        })
        .catch((error) => {
          this.$modal.msgError("创建失败：" + (error.msg || "未知错误"));
        });
    },
  },
};
</script>

<style scoped>
.dialog-footer {
  text-align: right;
}
</style>
