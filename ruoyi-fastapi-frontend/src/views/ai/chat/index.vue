<template>
  <div class="app-container chat-container">
    <el-container style="height: 100%">
      <!-- 侧边栏：会话历史 -->
      <el-aside width="260px" class="session-sidebar">
        <div class="sidebar-header">
          <el-button
            type="primary"
            class="new-chat-btn"
            icon="el-icon-plus"
            @click="clearChat"
            >新建对话</el-button
          >
        </div>
        <div class="session-list" v-loading="sessionLoading">
          <div
            v-for="session in sessionList"
            :key="session.sessionId"
            :class="[
              'session-item',
              currentSessionId === session.sessionId ? 'active' : '',
            ]"
            @click="loadSession(session.sessionId)"
          >
            <div class="session-icon">
              <i class="el-icon-chat-dot-round"></i>
            </div>
            <div class="session-info">
              <div class="session-title">
                {{ session.sessionTitle || "新对话" }}
              </div>
              <div class="session-time">
                {{ formatTime(session.createdAt) }}
              </div>
            </div>
            <el-button
              class="delete-btn"
              type="text"
              icon="el-icon-delete"
              style="color: #f56c6c"
              @click.stop="handleDeleteSession(session.sessionId)"
            ></el-button>
          </div>
          <div
            v-if="sessionList.length === 0 && !sessionLoading"
            class="empty-session"
          >
            暂无历史对话
          </div>
        </div>
      </el-aside>

      <!-- 主区域：对话框 -->
      <el-main class="chat-main">
        <div class="chat-header">
          <div class="header-left">
            <span class="header-title">AI 智能助手</span>
          </div>
          <div class="header-right">
            <el-tooltip content="全局参数配置" placement="bottom">
              <el-button
                icon="el-icon-setting"
                circle
                style="margin-right: 10px"
                @click="openConfigDialog"
              ></el-button>
            </el-tooltip>
            <el-select
              v-model="currentModelId"
              placeholder="选择模型"
              size="large"
              style="width: 210px"
            >
              <el-option
                v-for="item in modelOptions"
                :key="item.modelId"
                :label="`${item.provider}/${item.modelCode}`"
                :value="item.modelId"
              />
            </el-select>
          </div>
        </div>

        <div class="chat-history" ref="chatHistoryRef" @scroll="handleScroll">
          <div
            class="chat-content"
            ref="chatContentRef"
            :class="{ 'is-empty': messageList.length === 0 }"
          >
            <div v-if="messageList.length === 0" class="welcome-screen">
              <div class="welcome-icon">
                <i class="el-icon-service" style="font-size: 60px"></i>
              </div>
              <h2>你好！我是你的 AI 助手</h2>
              <p>请在下方输入问题开始对话...</p>
            </div>

            <div
              v-for="(msg, index) in messageList"
              :key="index"
              :class="[
                'message-row',
                msg.role === 'user' ? 'message-user' : 'message-ai',
              ]"
            >
              <div class="message-avatar">
                <el-avatar
                  :icon="
                    msg.role === 'user'
                      ? 'el-icon-user-solid'
                      : 'el-icon-service'
                  "
                  :size="40"
                  :class="msg.role === 'user' ? 'avatar-user' : 'avatar-ai'"
                ></el-avatar>
              </div>
              <div class="message-content-wrapper">
                <div class="message-sender">
                  {{ msg.role === "user" ? "我" : "AI 助手" }}
                  <span class="message-time" v-if="msg.createdAt">{{
                    formatTime(msg.createdAt)
                  }}</span>
                </div>
                <div class="message-bubble">
                  <div v-if="msg.role === 'user'">
                    <div
                      v-if="msg.images && msg.images.length > 0"
                      class="user-images"
                    >
                      <el-image
                        v-for="(img, idx) in msg.images"
                        :key="idx"
                        :src="getImageUrl(img)"
                        :preview-src-list="msg.images.map(getImageUrl)"
                        fit="cover"
                        class="user-image-item"
                      />
                    </div>
                    <div class="user-text">{{ msg.content }}</div>
                  </div>
                  <AiMessage
                    v-else
                    :content="msg.content"
                    :reasoning-content="msg.reasoningContent"
                    :loading="loading && index === messageList.length - 1"
                    :is-typing="msg.isTyping"
                    :is-dark="isDark"
                  />
                </div>
                
                <!-- 工具调用显示 -->
                <div v-if="msg.role === 'assistant' && msg.toolCalls && msg.toolCalls.length > 0" class="tool-calls-container">
                  <div
                    v-for="(toolCall, tcIdx) in msg.toolCalls"
                    :key="tcIdx"
                    :class="['tool-call-item', `tool-call-${toolCall.status}`]"
                  >
                    <!-- 业务友好显示（优先） -->
                    <div v-if="toolCall.display" class="tool-call-display">
                      <pre class="tool-call-friendly">{{ toolCall.display }}</pre>
                    </div>
                    
                    <!-- 传统显示（兼容旧数据或作为备用） -->
                    <div v-else>
                      <div class="tool-call-header">
                        <span class="tool-call-icon">
                          <i v-if="toolCall.status === 'running'" class="el-icon-loading"></i>
                          <i v-else-if="toolCall.status === 'completed'" class="el-icon-success" style="color: #67c23a;"></i>
                          <i v-else-if="toolCall.status === 'error'" class="el-icon-error" style="color: #f56c6c;"></i>
                        </span>
                        <span class="tool-call-name">🔧 {{ toolCall.name }}</span>
                        <span v-if="toolCall.status === 'running'" class="tool-call-status">执行中...</span>
                        <span v-else-if="toolCall.status === 'completed'" class="tool-call-status" style="color: #67c23a;">✓ 完成</span>
                        <span v-else-if="toolCall.status === 'error'" class="tool-call-status" style="color: #f56c6c;">✗ 失败</span>
                      </div>
                    </div>
                    
                    <!-- 技术详情（可折叠） -->
                    <div v-if="toolCall.args && Object.keys(toolCall.args).length > 0" class="tool-call-args">
                      <el-collapse accordion>
                        <el-collapse-item title="查看技术详情" name="1">
                          <pre class="tool-call-code">{{ JSON.stringify(toolCall.args, null, 2) }}</pre>
                        </el-collapse-item>
                      </el-collapse>
                    </div>
                    <div v-if="toolCall.result && !toolCall.display" class="tool-call-result">
                      <el-collapse accordion>
                        <el-collapse-item title="查看结果" name="1">
                          <pre class="tool-call-code">{{ toolCall.result }}</pre>
                        </el-collapse-item>
                      </el-collapse>
                    </div>
                    <div v-if="toolCall.error && !toolCall.display" class="tool-call-error">
                      <span style="color: #f56c6c;">错误: {{ toolCall.error }}</span>
                    </div>
                  </div>
                </div>
                <div class="message-footer">
                  <div class="footer-actions">
                    <el-tooltip content="复制" placement="top">
                      <el-button
                        type="text"
                        icon="el-icon-document-copy"
                        size="small"
                        style="color: #606266"
                        @click="copyText(msg.content)"
                      ></el-button>
                    </el-tooltip>
                    <div
                      v-if="
                        userConfig.metricsDefaultVisible == '0' &&
                        hasMetrics(msg)
                      "
                      class="message-metrics"
                    >
                      <span
                        v-if="
                          msg.metrics &&
                          msg.metrics.duration !== null &&
                          msg.metrics.duration !== undefined
                        "
                        >耗时 {{ msg.metrics.duration.toFixed(3) }} s</span
                      >
                      <span
                        v-if="
                          msg.metrics &&
                          msg.metrics.inputTokens !== null &&
                          msg.metrics.inputTokens !== undefined
                        "
                        >输入 {{ msg.metrics.inputTokens }} tokens</span
                      >
                      <span
                        v-if="
                          msg.metrics &&
                          msg.metrics.outputTokens !== null &&
                          msg.metrics.outputTokens !== undefined
                        "
                        >输出 {{ msg.metrics.outputTokens }} tokens</span
                      >
                      <span
                        v-if="
                          msg.metrics &&
                          msg.metrics.totalTokens !== null &&
                          msg.metrics.totalTokens !== undefined
                        "
                        >总 {{ msg.metrics.totalTokens }} tokens</span
                      >
                      <span
                        v-if="
                          msg.metrics &&
                          msg.metrics.reasoningTokens !== null &&
                          msg.metrics.reasoningTokens !== undefined
                        "
                        >推理 {{ msg.metrics.reasoningTokens }} tokens</span
                      >
                    </div>
                  </div>
                  <div v-if="msg.role === 'assistant'" class="model-info">
                    <el-tag
                      size="small"
                      type="info"
                      effect="plain"
                      v-if="
                        currentSessionAgentData && currentSessionAgentData.model
                      "
                    >
                      {{ currentSessionAgentData.model.provider }} /
                      {{ currentSessionAgentData.model.id }}
                    </el-tag>
                    <el-tag
                      size="small"
                      type="info"
                      effect="plain"
                      v-else-if="currentModelInfo"
                    >
                      {{ currentModelInfo.provider }} /
                      {{ currentModelInfo.modelCode }}
                    </el-tag>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="chat-input-area">
          <div class="input-wrapper">
            <el-input
              v-model="inputMessage"
              type="textarea"
              :rows="3"
              resize="none"
              placeholder="请输入您的问题... (Enter 发送，Shift + Enter 换行)"
              @keydown.enter.native.exact.prevent="handleSend"
              :disabled="loading"
            />
            <div
              class="selected-images"
              v-if="userConfig.visionEnabled == '0' && inputImages.length"
            >
              <el-image
                v-for="(img, idx) in inputImages"
                :key="idx"
                :src="getImageUrl(img)"
                :preview-src-list="inputImages.map(getImageUrl)"
                fit="cover"
                class="selected-image-item"
              />
            </div>
            <div class="input-actions">
              <div class="left-actions">
                <el-tooltip
                  v-if="
                    currentModelInfo &&
                    currentModelInfo.supportImages === 'Y' &&
                    userConfig.visionEnabled == '0'
                  "
                  content="上传图片"
                  placement="top"
                >
                  <el-button
                    circle
                    type="text"
                    icon="el-icon-picture-outline"
                    style="color: #606266"
                    @click="triggerImageUpload"
                  />
                </el-tooltip>
                <el-button
                  v-if="
                    currentModelInfo &&
                    currentModelInfo.supportReasoning === 'Y'
                  "
                  class="toggle-chip"
                  size="mini"
                  icon="deepthink"
                  :type="chatConfig.isReasoning ? 'primary' : ''"
                  :plain="!chatConfig.isReasoning"
                  @click="chatConfig.isReasoning = !chatConfig.isReasoning"
                >
                  <svg-icon icon-class="deepthink" />
                  深度思考
                </el-button>
              </div>
              <el-button
                :type="loading ? 'danger' : 'primary'"
                :icon="loading ? 'el-icon-video-pause' : 'el-icon-s-promotion'"
                @click="handleMainAction"
                :disabled="
                  !loading && !inputMessage.trim() && !inputImages.length
                "
              >
                {{ loading ? "停止" : "发送" }}
              </el-button>
            </div>
          </div>
        </div>
      </el-main>
    </el-container>

    <!-- 全局配置弹窗 -->
    <el-dialog
      :visible.sync="showConfigDialog"
      title="用户全局配置"
      width="700px"
      append-to-body
      class="chat-config-dialog"
    >
      <el-form :model="editingUserConfig" label-width="150px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="默认温度">
              <el-input-number
                v-model="editingUserConfig.temperature"
                :min="0"
                :max="2"
                :step="0.1"
                :precision="1"
                placeholder="默认温度"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="附带历史消息">
              <el-switch
                active-value="0"
                inactive-value="1"
                v-model="editingUserConfig.addHistoryToContext"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="历史消息轮数"
              v-if="editingUserConfig.addHistoryToContext == '0'"
            >
              <el-input-number
                v-model="editingUserConfig.numHistoryRuns"
                :min="1"
                :max="20"
                placeholder="历史消息轮数"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="默认显示指标">
              <el-switch
                active-value="0"
                inactive-value="1"
                v-model="editingUserConfig.metricsDefaultVisible"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="开启视觉功能">
              <el-switch
                active-value="0"
                inactive-value="1"
                v-model="editingUserConfig.visionEnabled"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="图片最大大小"
              v-if="editingUserConfig.visionEnabled"
            >
              <el-input-number
                v-model="editingUserConfig.imageMaxSizeMb"
                :min="1"
                :max="50"
                placeholder="图片大小"
                style="width: 100%"
              >
                <template #suffix>
                  <span>MB</span>
                </template>
              </el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item label="系统提示词">
              <el-input
                v-model="editingUserConfig.systemPrompt"
                type="textarea"
                :rows="4"
                placeholder="设置全局系统提示词"
              />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showConfigDialog = false">取消</el-button>
          <el-button type="primary" @click="handleSaveConfig">保存</el-button>
        </span>
      </template>
    </el-dialog>
    <input
      v-if="userConfig.visionEnabled"
      ref="imageInputRef"
      type="file"
      accept="image/*"
      multiple
      class="chat-image-input"
      @change="handleImageInputChange"
    />
  </div>
</template>

<script>
import { listModelAll } from "@/api/ai/model";
import {
  listChatSession,
  delChatSession,
  getChatSession,
  getUserChatConfig,
  saveUserChatConfig,
  cancelChatRun,
} from "@/api/ai/chat";
import { getToken } from "@/utils/auth";
import AiMessage from "./components/AiMessage";
import { v4 as uuidv4 } from "uuid";

export default {
  name: "AiChat",
  components: { AiMessage },
  data() {
    return {
      modelOptions: [],
      currentModelId: undefined,
      messageList: [],
      inputMessage: "",
      inputImages: [],
      loading: false,
      currentSessionId: null,
      showConfigDialog: false,
      sessionList: [],
      sessionLoading: false,
      abortController: null,
      currentRunId: null,
      isAutoScroll: true,
      currentSessionAgentData: null,
      isProgrammaticScroll: false,
      scrollTimeout: null,
      chatConfig: {
        temperature: undefined,
        isReasoning: true,
      },
      userConfig: {
        chatConfigId: undefined,
        userId: undefined,
        temperature: undefined,
        addHistoryToContext: "0",
        numHistoryRuns: 3,
        systemPrompt: "",
        metricsDefaultVisible: "1",
        visionEnabled: "0",
        imageMaxSizeMb: 5,
        createTime: undefined,
        updateTime: undefined,
      },
      editingUserConfig: {
        chatConfigId: undefined,
        userId: undefined,
        temperature: undefined,
        addHistoryToContext: "0",
        numHistoryRuns: 3,
        systemPrompt: "",
        metricsDefaultVisible: "1",
        visionEnabled: "0",
        imageMaxSizeMb: 5,
        createTime: undefined,
        updateTime: undefined,
      },
      isDark: false, // Default to light
    };
  },
  computed: {
    currentModelInfo() {
      if (!this.currentModelId) return null;
      return this.modelOptions.find((m) => m.modelId === this.currentModelId);
    },
  },
  watch: {
    currentModelId(newVal) {
      const model = this.modelOptions.find((m) => m.modelId === newVal);
      if (model) {
        this.chatConfig.temperature = model.temperature;
      }
    },
  },
  mounted() {
    this.getModels();
    this.getSessions();
    this.loadUserConfig();
    // Initialize ResizeObserver for auto-scroll if supported
    if (window.ResizeObserver && this.$refs.chatContentRef) {
      this.resizeObserver = new ResizeObserver(() => {
        if (this.isAutoScroll) {
          this.scrollToBottom();
        }
      });
      this.resizeObserver.observe(this.$refs.chatContentRef);
    }
  },
  beforeDestroy() {
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
    }
    if (this.abortController) {
      this.abortController.abort();
    }
  },
  methods: {
    generateSessionId() {
      return uuidv4();
    },
    loadUserConfig() {
      getUserChatConfig().then((res) => {
        if (res.data) {
          if (res.data.temperature === null) {
            res.data.temperature = undefined;
          }
          if (res.data.numHistoryRuns === null) {
            res.data.numHistoryRuns = undefined;
          }
          if (res.data.imageMaxSizeMb === null) {
            res.data.imageMaxSizeMb = undefined;
          }
          Object.assign(this.userConfig, res.data);
          Object.assign(this.editingUserConfig, res.data);
        }
      });
    },
    openConfigDialog() {
      Object.assign(this.editingUserConfig, this.userConfig);
      this.showConfigDialog = true;
    },
    handleSaveConfig() {
      const payload = { ...this.editingUserConfig };
      saveUserChatConfig(payload).then(() => {
        this.$modal.msgSuccess("配置保存成功");
        this.showConfigDialog = false;
        this.loadUserConfig();
      });
    },
    hasMetrics(msg) {
      const m = msg && msg.metrics;
      if (!m) return false;
      return (
        (m.inputTokens !== null && m.inputTokens !== undefined) ||
        (m.outputTokens !== null && m.outputTokens !== undefined) ||
        (m.totalTokens !== null && m.totalTokens !== undefined) ||
        (m.reasoningTokens !== null && m.reasoningTokens !== undefined) ||
        (m.duration !== null && m.duration !== undefined)
      );
    },
    getImageUrl(url) {
      if (!url) return "";
      if (
        url.startsWith("http") ||
        url.startsWith("https") ||
        url.startsWith("blob:")
      ) {
        return url;
      }
      return process.env.VUE_APP_BASE_API + url;
    },
    formatTime(timeStr) {
      if (!timeStr) return "";
      try {
        const date = new Date(timeStr);
        return date.toLocaleString();
      } catch (e) {
        return timeStr;
      }
    },
    getModels() {
      listModelAll().then((res) => {
        this.modelOptions = res.data;
        if (this.modelOptions.length > 0) {
          this.currentModelId = this.modelOptions[0].modelId;
          const model = this.modelOptions[0];
          this.chatConfig.temperature = model.temperature;
        }
      });
    },
    getSessions() {
      this.sessionLoading = true;
      listChatSession().then((res) => {
        this.sessionList = res.data;
        if (this.sessionList && this.sessionList.length > 0) {
          this.sessionList.sort((a, b) => {
            const dateA = new Date(a.createdAt).getTime();
            const dateB = new Date(b.createdAt).getTime();
            return dateB - dateA;
          });
        }
        this.sessionLoading = false;
      });
    },
    loadSession(sessionId) {
      if (this.currentSessionId === sessionId) return;
      this.currentSessionId = sessionId;
      this.messageList = [];
      this.loading = true;
      getChatSession(sessionId).then((res) => {
        this.messageList = res.data.messages;
        this.currentSessionAgentData = res.data.agentData;
        this.loading = false;
        this.isAutoScroll = true;
        this.scrollToBottom();
      });
    },
    handleDeleteSession(sessionId) {
      this.$modal
        .confirm("是否确认删除该会话？")
        .then(() => {
          return delChatSession(sessionId);
        })
        .then(() => {
          this.getSessions();
          if (this.currentSessionId === sessionId) {
            this.clearChat();
          }
          this.$modal.msgSuccess("删除成功");
        })
        .catch(() => {});
    },
    async sendRequest(text, images) {
      if (!this.currentModelId) {
        this.$modal.msgError("请先选择模型");
        return;
      }

      this.loading = true;
      const imageList = images ? images.slice() : [];

      this.messageList.push({
        role: "assistant",
        content: "",
        reasoningContent: "",
        toolCalls: [], // 工具调用记录
      });
      const aiMsgIndex = this.messageList.length - 1;

      this.scrollToBottom();
      this.isAutoScroll = true;

      this.abortController = new AbortController();

      try {
        const response = await fetch(
          process.env.VUE_APP_BASE_API + "/ai/chat/send",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: "Bearer " + getToken(),
            },
            signal: this.abortController.signal,
            body: JSON.stringify({
              modelId: this.currentModelId,
              message: text,
              images: imageList,
              sessionId: this.currentSessionId,
              stream: true,
              temperature: this.chatConfig.temperature,
              isReasoning: this.chatConfig.isReasoning,
            }),
          }
        );

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let aiContent = "";
        let aiReasoning = "";
        let buffer = "";
        let needRefreshSessions = false;

        while (true) {
          if (!this.abortController) break;
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split("\n");
          buffer = lines.pop();

          for (const line of lines) {
            if (!line.trim()) continue;
            try {
              const data = JSON.parse(line);
              if (data.type === "content") {
                // 流式打字机效果：逐字符添加
                const newContent = data.content;
                aiContent += newContent;
                
                // 使用 Vue.set 确保响应式更新
                this.$set(this.messageList[aiMsgIndex], "content", aiContent);
                this.$set(this.messageList[aiMsgIndex], "isTyping", true);
                
                // 平滑滚动到底部
                this.$nextTick(() => {
                  if (this.isAutoScroll) {
                    this.scrollToBottom();
                  }
                });
              } else if (data.type === "reasoning") {
                aiReasoning += data.content;
                this.$set(
                  this.messageList[aiMsgIndex],
                  "reasoningContent",
                  aiReasoning
                );
                this.$nextTick(() => {
                  if (this.isAutoScroll) {
                    this.scrollToBottom();
                  }
                });
              } else if (data.type === "tool_call_started") {
                // 工具调用开始
                console.log('🔧 Tool call started:', data);
                const toolCall = {
                  id: data.tool_call_id || Date.now(),
                  name: data.tool_name,
                  args: data.tool_args,
                  display: data.display,  // 业务友好显示
                  status: 'running',
                  startTime: new Date().toISOString(),
                };
                if (!this.messageList[aiMsgIndex].toolCalls) {
                  this.$set(this.messageList[aiMsgIndex], 'toolCalls', []);
                }
                this.messageList[aiMsgIndex].toolCalls.push(toolCall);
                console.log('🔧 Tool calls array:', this.messageList[aiMsgIndex].toolCalls);
              } else if (data.type === "tool_call_completed") {
                // 工具调用完成
                console.log('✅ Tool call completed:', data);
                const toolCalls = this.messageList[aiMsgIndex].toolCalls || [];
                const toolCall = toolCalls.find(t => t.name === data.tool_name && t.status === 'running');
                console.log('✅ Found tool call:', toolCall);
                if (toolCall) {
                  toolCall.status = 'completed';
                  toolCall.result = data.result;
                  toolCall.display = data.display;  // 业务友好显示
                  toolCall.endTime = new Date().toISOString();
                  console.log('✅ Updated tool call:', toolCall);
                }
              } else if (data.type === "tool_call_error") {
                // 工具调用失败
                console.log('❌ Tool call error:', data);
                const toolCalls = this.messageList[aiMsgIndex].toolCalls || [];
                const toolCall = toolCalls.find(t => t.name === data.tool_name && t.status === 'running');
                if (toolCall) {
                  toolCall.status = 'error';
                  toolCall.error = data.error;
                  toolCall.display = data.display;  // 业务友好显示
                  toolCall.endTime = new Date().toISOString();
                }
              } else if (data.type === "meta") {
                this.currentSessionId = data.session_id;
                if (
                  !this.sessionList.find((s) => s.sessionId === data.session_id)
                ) {
                  needRefreshSessions = true;
                }
              } else if (data.type === "run_info") {
                this.currentRunId = data.run_id;
              } else if (data.type === "metrics") {
                this.$set(
                  this.messageList[aiMsgIndex],
                  "metrics",
                  data.metrics
                );
              } else if (data.type === "error") {
                this.$modal.msgError(data.error);
              }
            } catch (e) {
              console.error("Parse error", e);
            }
          }
        }

        if (needRefreshSessions) {
          this.getSessions();
        }
        
        // 标记打字完成
        if (this.messageList[aiMsgIndex]) {
          this.$set(this.messageList[aiMsgIndex], "isTyping", false);
        }
      } catch (err) {
        if (err.name === "AbortError") {
          // User aborted
        } else {
          this.$modal.msgError("请求失败: " + err.message);
        }
      } finally {
        this.loading = false;
        this.abortController = null;
      }
    },
    clearChat() {
      this.messageList = [];
      this.currentSessionId = this.generateSessionId();
      this.currentSessionAgentData = null;
    },
    copyText(text) {
      if (!text) {
        this.$modal.msgWarning("内容为空，无法复制");
        return;
      }
      navigator.clipboard
        .writeText(text)
        .then(() => {
          this.$modal.msgSuccess("复制成功");
        })
        .catch(() => {
          this.$modal.msgError("复制失败");
        });
    },
    triggerImageUpload() {
      if (!this.userConfig.visionEnabled || this.loading) return;
      const input = this.$refs.imageInputRef;
      if (input) {
        input.value = "";
        input.click();
      }
    },
    async handleImageInputChange(event) {
      const files = Array.from(event.target.files || []);
      if (!files.length) return;
      if (files.length + this.inputImages.length > 10) {
        this.$modal.msgError("最多只能上传 10 张图片");
        return;
      }
      const maxSize = (this.userConfig.imageMaxSizeMb || 5) * 1024 * 1024;
      for (const file of files) {
        if (file.size > maxSize) {
          this.$modal.msgError(
            `单张图片大小不能超过 ${this.userConfig.imageMaxSizeMb} MB`
          );
          return;
        }
      }
      try {
        this.$modal.loading("正在上传图片，请稍候...");
        for (const file of files) {
          const form = new FormData();
          form.append("file", file);
          const resp = await fetch(
            process.env.VUE_APP_BASE_API + "/common/upload",
            {
              method: "POST",
              headers: {
                Authorization: "Bearer " + getToken(),
              },
              body: form,
            }
          );
          const data = await resp.json();
          if (data.code === 200 && data.fileName) {
            this.inputImages.push(data.fileName);
          } else {
            this.$modal.msgError(data.msg || "上传图片失败");
          }
        }
      } catch (e) {
        this.$modal.msgError("上传图片失败");
      } finally {
        this.$modal.closeLoading();
      }
    },
    async handleSend() {
      const text = this.inputMessage.trim();
      const images = this.inputImages;
      if (!text && !images.length) return;
      if (!this.currentModelId) {
        this.$modal.msgError("请先选择模型");
        return;
      }

      const imageList = images.slice();
      this.messageList.push({
        role: "user",
        content: text,
        images: imageList,
      });
      this.inputMessage = "";
      this.inputImages = [];
      this.currentRunId = null;

      await this.sendRequest(text, imageList);
    },
    stopGeneration() {
      if (this.abortController) {
        const controller = this.abortController;
        this.abortController = null;
        this.loading = false;

        if (this.currentRunId) {
          cancelChatRun(this.currentRunId)
            .then(() => {})
            .catch((err) => {
              console.error("Failed to cancel run:", err);
            })
            .finally(() => {
              controller.abort();
            });
        } else {
          controller.abort();
        }
      }
    },
    handleScroll(e) {
      if (this.isProgrammaticScroll) return;

      const { scrollTop, scrollHeight, clientHeight } = e.target;
      const distanceToBottom = scrollHeight - scrollTop - clientHeight;

      if (distanceToBottom > 100) {
        this.isAutoScroll = false;
      } else if (distanceToBottom < 20) {
        this.isAutoScroll = true;
      }
    },
    scrollToBottom() {
      if (this.isAutoScroll && this.$refs.chatHistoryRef) {
        this.isProgrammaticScroll = true;

        // 使用 smooth 滚动实现更流畅的效果
        this.$refs.chatHistoryRef.scrollTo({
          top: this.$refs.chatHistoryRef.scrollHeight,
          behavior: 'smooth'
        });

        this.$nextTick(() => {
          if (this.$refs.chatHistoryRef && this.isAutoScroll) {
            this.$refs.chatHistoryRef.scrollTop =
              this.$refs.chatHistoryRef.scrollHeight;
          }
        });

        if (this.scrollTimeout) clearTimeout(this.scrollTimeout);

        this.scrollTimeout = setTimeout(() => {
          this.isProgrammaticScroll = false;
          this.scrollTimeout = null;
        }, 150);
      }
    },
    handleMainAction() {
      if (this.loading) {
        this.stopGeneration();
      } else {
        this.handleSend();
      }
    },
  },
};
</script>

<style scoped lang="scss">
.chat-container {
  height: calc(100vh - 84px);
  padding: 0;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
  overflow: hidden;
}

.session-sidebar {
  border-right: 1px solid #dcdfe6;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.02);
  z-index: 10;
  margin-bottom: 0;
  overflow: hidden;

  .sidebar-header {
    padding: 20px;
    border-bottom: 1px solid #dcdfe6;

    .new-chat-btn {
      width: 100%;
      border-radius: 8px;
      height: 40px;
      font-size: 14px;
    }
  }

  .session-list {
    flex: 1;
    overflow-y: auto;
    padding: 10px;

    &::-webkit-scrollbar {
      width: 6px;
    }
    &::-webkit-scrollbar-thumb {
      background: #c0c4cc;
      border-radius: 3px;
      
      &:hover {
        background: #909399;
      }
    }

    .session-item {
      display: flex;
      align-items: center;
      padding: 14px 12px;
      margin-bottom: 8px;
      background-color: transparent;
      border-radius: 10px;
      cursor: pointer;
      transition: all 0.3s ease;
      position: relative;
      border: 1px solid transparent;

      &:hover {
        background-color: #f5f7fa;
        transform: translateX(4px);
      }

      &.active {
        background: linear-gradient(135deg, #ecf5ff 0%, #e6f7ff 100%);
        border-color: #b3d8ff;
        box-shadow: 0 2px 8px rgba(64, 158, 255, 0.15);

        .session-icon {
          color: #409eff;
        }

        .session-title {
          color: #409eff;
          font-weight: 600;
        }
      }

      .session-icon {
        margin-right: 12px;
        color: #909399;
        display: flex;
        align-items: center;
        font-size: 18px;
      }

      .session-info {
        flex: 1;
        overflow: hidden;

        .session-title {
          font-size: 14px;
          color: #303133;
          margin-bottom: 4px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          transition: all 0.2s;
        }

        .session-time {
          font-size: 12px;
          color: #909399;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
      }

      .delete-btn {
        opacity: 0;
        transition: all 0.2s;
        padding: 4px;
      }

      &:hover .delete-btn {
        opacity: 1;
      }
    }

    .empty-session {
      text-align: center;
      color: #909399;
      font-size: 13px;
      margin-top: 40px;
    }
  }
}

.chat-main {
  padding: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f0f2f5;
  position: relative;
  overflow: hidden;

  .chat-header {
    height: 64px;
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border-bottom: 1px solid #e4e7ed;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 24px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);

    .header-title {
      font-size: 18px;
      font-weight: 600;
      color: #303133;
      display: flex;
      align-items: center;
      gap: 8px;
      
      &::before {
        content: '🤖';
        font-size: 24px;
      }
    }
  }

  .chat-history {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    scroll-behavior: smooth;

    &::-webkit-scrollbar {
      width: 8px;
    }
    
    &::-webkit-scrollbar-track {
      background: transparent;
    }
    
    &::-webkit-scrollbar-thumb {
      background: rgba(0, 0, 0, 0.2);
      border-radius: 4px;
      
      &:hover {
        background: rgba(0, 0, 0, 0.3);
      }
    }

    .chat-content {
      min-height: 100%;
      padding-bottom: 20px;

      &.is-empty {
        display: flex;
        flex-direction: column;
        height: 100%;
      }
    }

    .welcome-screen {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      color: #909399;
      opacity: 0.8;

      .welcome-icon {
        border-radius: 50%;
        padding: 30px;
        margin-bottom: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
        animation: pulse 2s ease-in-out infinite;
      }
      
      @keyframes pulse {
        0%, 100% {
          transform: scale(1);
        }
        50% {
          transform: scale(1.05);
        }
      }

      h2 {
        margin-bottom: 12px;
        font-weight: 600;
        color: #303133;
        font-size: 24px;
      }

      p {
        margin-top: 0;
        color: #909399;
        font-size: 15px;
      }
    }

    .message-row {
      display: flex;
      max-width: 900px;
      margin-bottom: 28px;
      margin-left: auto;
      margin-right: auto;
      animation: messageSlideIn 0.3s ease-out;

      @keyframes messageSlideIn {
        from {
          opacity: 0;
          transform: translateY(10px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      .message-avatar {
        flex-shrink: 0;
        margin-right: 14px;
        margin-top: 2px;

        .avatar-user {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }

        .avatar-ai {
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
          box-shadow: 0 2px 8px rgba(240, 147, 251, 0.3);
        }
      }

      .message-content-wrapper {
        flex: 1;
        display: flex;
        flex-direction: column;
        max-width: calc(100% - 54px);

        .message-sender {
          font-size: 13px;
          font-weight: 500;
          color: #606266;
          margin-bottom: 6px;
          display: flex;
          align-items: center;
          gap: 10px;
        }

        .message-time {
          font-size: 11px;
          opacity: 0.7;
          font-weight: 400;
        }

        .message-bubble {
          padding: 14px 18px;
          border-radius: 16px;
          font-size: 15px;
          line-height: 1.7;
          max-width: 100%;
          min-width: 60px;
          background-color: #fff;
          position: relative;
          transition: all 0.2s ease;
          
          &:hover {
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
          }
        }

        .message-footer {
          margin-top: 8px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          width: 100%;
          opacity: 0.7;
          transition: opacity 0.2s;

          &:hover {
            opacity: 1;
          }

          .message-metrics {
            font-size: 12px;
            color: #909399;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            
            span {
              padding: 2px 8px;
              background-color: #f5f7fa;
              border-radius: 4px;
            }
          }

          .footer-actions {
            display: flex;
            align-items: center;
            gap: 10px;
          }

          .model-info {
            margin-left: auto;
          }
        }
      }

      &.message-user {
        flex-direction: row-reverse;
        padding-left: 54px;

        .message-avatar {
          margin-left: 14px;
          margin-right: 0;
        }

        .message-content-wrapper {
          align-items: flex-end;

          .message-sender {
            flex-direction: row-reverse;
          }

          .message-footer {
            flex-direction: row-reverse;
          }

          .message-bubble {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            border-top-right-radius: 4px;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);
            
            &:hover {
              box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35);
            }
          }
        }
      }

      &.message-ai {
        padding-right: 54px;

        .message-bubble {
          background-color: #ffffff;
          color: #303133;
          border-top-left-radius: 4px;
          box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
          border: 1px solid #f0f0f0;
        }
      }
    }
  }
}

.chat-input-area {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.8) 0%, #ffffff 100%);
  border-top: 1px solid #e4e7ed;
  padding: 20px;
  backdrop-filter: blur(10px);

  .input-wrapper {
    max-width: 900px;
    margin: 0 auto;
    position: relative;
    border: 2px solid #e4e7ed;
    border-radius: 16px;
    padding: 12px;
    transition: all 0.3s ease;
    background-color: #ffffff;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);

    &:focus-within {
      border-color: #667eea;
      box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15);
      transform: translateY(-2px);
    }

    ::v-deep .el-textarea__inner {
      border: none;
      box-shadow: none;
      padding: 4px 0;
      resize: none;
      background: transparent;
      font-size: 15px;
      line-height: 1.6;

      &:focus {
        box-shadow: none;
      }
      
      &::placeholder {
        color: #c0c4cc;
      }
    }

    .selected-images {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 10px;
      padding-top: 10px;
      border-top: 1px dashed #dcdfe6;

      .selected-image-item {
        width: 60px;
        height: 60px;
        border-radius: 8px;
        border: 2px solid #e4e7ed;
        transition: all 0.2s;
        
        &:hover {
          border-color: #667eea;
          transform: scale(1.05);
        }
      }
    }

    .input-actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 10px;
      padding-top: 10px;
      border-top: 1px solid #f0f0f0;

      .left-actions {
        display: flex;
        gap: 8px;
        align-items: center;

        .toggle-chip {
          border-radius: 999px;
          margin-left: 0;
          transition: all 0.2s;
          
          &:hover {
            transform: translateY(-1px);
          }
        }
      }
      
      ::v-deep .el-button--primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 500;
        transition: all 0.3s ease;
        
        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        &:active {
          transform: translateY(0);
        }
      }
      
      ::v-deep .el-button--danger {
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 500;
      }
    }
  }
}

.chat-config-dialog {
  ::v-deep .el-dialog__body {
    padding-top: 10px;
    padding-bottom: 10px;
  }
}

.chat-image-input {
  display: none;
}

.user-images {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 8px;

  .user-image-item {
    width: 100px;
    height: 100px;
    border-radius: 8px;
    cursor: pointer;
    border: 1px solid rgba(255, 255, 255, 0.2);
  }
}

.user-text {
  white-space: pre-wrap;
  word-break: break-word;
}

// 工具调用样式
.tool-calls-container {
  margin-top: 12px;
  
  .tool-call-item {
    background-color: #f5f7fa;
    border: 1px solid #e4e7ed;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 8px;
    transition: all 0.3s;
    
    &.tool-call-running {
      border-color: #409eff;
      background-color: #ecf5ff;
    }
    
    &.tool-call-completed {
      border-color: #67c23a;
      background-color: #f0f9ff;
    }
    
    &.tool-call-error {
      border-color: #f56c6c;
      background-color: #fef0f0;
    }
    
    // 业务友好显示样式
    .tool-call-display {
      .tool-call-friendly {
        background-color: transparent;
        color: #303133;
        padding: 0;
        margin: 0;
        font-size: 14px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
        line-height: 1.8;
        white-space: pre-wrap;
        word-break: break-word;
        border: none;
      }
    }
    
    .tool-call-header {
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 500;
      margin-bottom: 8px;
      
      .tool-call-icon {
        font-size: 16px;
      }
      
      .tool-call-name {
        flex: 1;
        font-size: 14px;
      }
      
      .tool-call-status {
        font-size: 12px;
        color: #909399;
      }
    }
    
    .tool-call-args,
    .tool-call-result {
      margin-top: 8px;
      
      ::v-deep .el-collapse {
        border: none;
        
        .el-collapse-item__header {
          background-color: transparent;
          border: none;
          font-size: 12px;
          color: #606266;
          padding-left: 0;
        }
        
        .el-collapse-item__wrap {
          border: none;
          background-color: transparent;
        }
        
        .el-collapse-item__content {
          padding: 8px 0 0 0;
        }
      }
      
      .tool-call-code {
        background-color: #282c34;
        color: #abb2bf;
        padding: 12px;
        border-radius: 4px;
        font-size: 12px;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        overflow-x: auto;
        margin: 0;
        max-height: 200px;
        overflow-y: auto;
        
        &::-webkit-scrollbar {
          width: 6px;
          height: 6px;
        }
        
        &::-webkit-scrollbar-thumb {
          background: #4a4a4a;
          border-radius: 3px;
        }
      }
    }
    
    .tool-call-error {
      margin-top: 8px;
      font-size: 13px;
      padding: 8px;
      background-color: #fef0f0;
      border-radius: 4px;
    }
  }
}
</style>
