# 工具调用显示优化集成指南

## 问题描述

当前 AI 对话框显示的工具调用信息过于技术化，业务人员难以理解：

```
ToolExecution(tool_call_id='call_f8da41f7321a4092ab6ed045', 
              tool_name='execute_command', 
              tool_args={'command': 'curl -s "https://zh.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles=博威合金材料股份有限公司..."'})
```

## 解决方案

使用 `ToolDisplayFormatter` 将技术信息转换为业务友好的显示格式：

```
🔧 正在调用工具：命令执行
📝 执行命令：curl -s "https://zh.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles=博威合金材料股份有限...
⏱️  超时时间：15秒
⏳ 执行中...
```

## 集成步骤

### 1. 在 AI 聊天服务中集成格式化器

修改 `module_ai/service/ai_chat_service.py`：

```python
from module_ai.utils.tool_display_formatter import format_tool_call, format_tool_result

class AiChatService:
    
    @classmethod
    async def chat_with_ai(cls, ...):
        # ... 现有代码 ...
        
        # 在工具调用前格式化显示
        for tool_call in agent_response.tool_calls:
            friendly_display = format_tool_call(
                tool_call.tool_name, 
                tool_call.tool_args
            )
            # 发送友好显示到前端
            await cls._send_tool_call_display(friendly_display)
        
        # 在工具执行后格式化结果
        for tool_result in tool_results:
            result_display = format_tool_result(
                tool_result.tool_name,
                tool_result.result,
                success=tool_result.success
            )
            # 发送结果显示到前端
            await cls._send_tool_result_display(result_display)
```

### 2. 在 WebSocket 消息中使用格式化器

如果使用 WebSocket 实时推送：

```python
# 发送工具调用通知
await websocket.send_json({
    'type': 'tool_call',
    'display': format_tool_call(tool_name, tool_args),
    'raw': {  # 可选：保留原始数据供调试
        'tool_name': tool_name,
        'tool_args': tool_args
    }
})

# 发送工具执行结果
await websocket.send_json({
    'type': 'tool_result',
    'display': format_tool_result(tool_name, result, success),
    'raw': {  # 可选：保留原始数据供调试
        'result': result,
        'success': success
    }
})
```

### 3. 前端显示优化

在前端 Vue 组件中：

```vue
<template>
  <div class="ai-chat-message">
    <!-- 工具调用显示 -->
    <div v-if="message.type === 'tool_call'" class="tool-call-display">
      <pre>{{ message.display }}</pre>
      
      <!-- 可选：技术详情折叠面板 -->
      <el-collapse v-if="message.raw">
        <el-collapse-item title="查看技术详情">
          <pre>{{ JSON.stringify(message.raw, null, 2) }}</pre>
        </el-collapse-item>
      </el-collapse>
    </div>
    
    <!-- 工具结果显示 -->
    <div v-if="message.type === 'tool_result'" class="tool-result-display">
      <pre>{{ message.display }}</pre>
    </div>
  </div>
</template>

<style scoped>
.tool-call-display {
  background: #f5f7fa;
  border-left: 4px solid #409eff;
  padding: 12px;
  margin: 8px 0;
  border-radius: 4px;
}

.tool-result-display {
  background: #f0f9ff;
  border-left: 4px solid #67c23a;
  padding: 12px;
  margin: 8px 0;
  border-radius: 4px;
}

pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
}
</style>
```

## 支持的工具类型

当前格式化器支持以下工具类型：

| 工具名称 | 友好名称 | 显示内容 |
|---------|---------|---------|
| `execute_command` | 命令执行 | 命令、工作目录、超时时间 |
| `execute_python_code` | Python 代码执行 | 代码预览（前3行）、超时时间 |
| `web_search` | 网页搜索 | 搜索关键词 |
| `web_fetch` | 网页内容获取 | 目标网址 |
| 其他工具 | 原工具名 | 参数列表（最多3个） |

## 扩展新工具类型

如需支持新的工具类型，在 `tool_display_formatter.py` 中添加：

```python
class ToolDisplayFormatter:
    
    # 1. 添加工具名称映射
    TOOL_NAME_MAP = {
        # ... 现有映射 ...
        'your_new_tool': '你的新工具',
    }
    
    # 2. 添加格式化方法
    @classmethod
    def _format_your_new_tool(cls, friendly_name: str, tool_args: dict) -> str:
        """格式化你的新工具"""
        param1 = tool_args.get('param1', '')
        param2 = tool_args.get('param2', '')
        
        lines = [
            f'🔧 正在调用工具：{friendly_name}',
            f'📝 参数1：{param1}',
            f'📝 参数2：{param2}',
            '⏳ 执行中...',
        ]
        
        return '\n'.join(lines)
    
    # 3. 在 format_tool_call 中添加分支
    @classmethod
    def format_tool_call(cls, tool_name: str, tool_args: dict[str, Any]) -> str:
        # ... 现有代码 ...
        elif tool_name == 'your_new_tool':
            return cls._format_your_new_tool(friendly_name, tool_args)
        # ... 现有代码 ...
```

## 测试

运行测试查看效果：

```bash
cd ruoyi-fastapi-backend
python -m module_ai.utils.test_tool_display_formatter
```

## 效果对比

### 优化前（技术性）
```
ToolExecution(tool_call_id='call_xxx', tool_name='execute_command', 
tool_args={'command': 'curl -s "https://zh.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles=博威合金材料股份有限公司&exintro=&formatversion=2" | python3 -c "import json,sys; data=json.load(sys.stdin); pages=data.get(\'query\',{}).get(\'pages\',[{}]); print(pages[0].get(\'extract\',\'\')[:500] if pages else \'未找到信息\')"', 'timeout': 15})
```

### 优化后（业务友好）
```
🔧 正在调用工具：命令执行
📝 执行命令：curl -s "https://zh.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles=博威合金材料股份有限...
⏱️  超时时间：15秒
⏳ 执行中...

✅ 命令执行 - 执行成功
📄 结果：
博威合金材料股份有限公司成立于1993年，总部位于浙江省宁波市，是一家专业从事高性能合金材料研发、生产和销售的高新技术企业...
```

## 注意事项

1. **保留原始数据**：建议在前端保留原始的技术数据，供开发人员调试使用
2. **可折叠显示**：将技术详情放在可折叠的面板中，默认隐藏
3. **长文本截断**：对于过长的命令或结果，自动截断并显示"..."
4. **错误处理**：失败的工具调用使用红色图标（❌）和错误提示
5. **实时更新**：工具执行过程中显示"⏳ 执行中..."，完成后更新为结果

## 相关文件

- `module_ai/utils/tool_display_formatter.py` - 格式化器实现
- `module_ai/utils/test_tool_display_formatter.py` - 测试文件
- `module_ai/service/ai_chat_service.py` - AI 聊天服务（需要集成）
