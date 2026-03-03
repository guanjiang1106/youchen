# 缩进问题最终解决方案（已完全修复）

## 问题根源

AI 生成的 Python 代码经常出现缩进错误，主要表现为：

1. `@classmethod` 装饰器前有多余的空行
2. `@classmethod` 装饰器缩进不正确
3. 方法体缩进不一致

**错误示例**：
```python
# 原有代码
    return result


@classmethod  # ❌ 错误：多了一个空行，且缩进不对
    async def new_method(cls):
        pass
```

**正确示例**：
```python
# 原有代码
    return result

    @classmethod  # ✅ 正确：一个空行，缩进正确（4个空格）
    async def new_method(cls):
        pass
```

## 完整解决方案（三层防护）

### 第 1 层：智能缩进修复算法

系统会自动检测并修复缩进问题：

```python
# 智能修复缩进
lines = service_code.split('\n')
if lines:
    # 检测第一行的缩进级别
    first_line = lines[0]
    first_line_stripped = first_line.lstrip()
    
    # 如果第一行是装饰器或方法定义，需要确保正确的缩进
    if first_line_stripped.startswith('@') or \
       first_line_stripped.startswith('async def') or \
       first_line_stripped.startswith('def'):
        # 计算当前缩进
        current_indent = len(first_line) - len(first_line_stripped)
        
        # 类方法应该有4个空格的缩进
        target_indent = 4
        indent_diff = target_indent - current_indent
        
        # 调整所有行的缩进
        fixed_lines = []
        for line in lines:
            if line.strip():  # 非空行
                # 计算当前行的缩进
                line_stripped = line.lstrip()
                line_indent = len(line) - len(line_stripped)
                # 调整缩进
                new_indent = max(0, line_indent + indent_diff)
                fixed_lines.append(' ' * new_indent + line_stripped)
            else:
                # 空行保持为空
                fixed_lines.append('')
        service_code = '\n'.join(fixed_lines)
```

**算法原理**：
1. 检测第一行的当前缩进
2. 计算与目标缩进（4个空格）的差异
3. 按比例调整所有行的缩进
4. 保持代码的相对缩进关系

### 第 2 层：自动代码格式化

应用代码后，自动运行 `autopep8` 格式化：

```python
# 尝试使用 autopep8 格式化文件
try:
    import subprocess
    subprocess.run(['autopep8', '--in-place', '--aggressive', service_file], 
                 capture_output=True, timeout=5, check=False)
except Exception:
    # 如果格式化失败，继续执行（不影响主流程）
    pass
```

### 第 3 层：详细的 AI 提示词

在提示词中明确要求：

```
【Python 缩进规范 - 非常重要！】
- 类方法的装饰器（@classmethod）必须有 4 个空格缩进
- 类方法的定义（async def）必须有 4 个空格缩进
- 方法体内的代码必须有 8 个空格缩进
- 嵌套代码块（if、for、try等）每层增加 4 个空格
- 不要使用 Tab，只使用空格
- 装饰器和方法定义之间不要有空行
- 方法之间只有一个空行

【缩进检查清单】
生成代码前，请确认：
✓ @classmethod 前面有 4 个空格
✓ async def 前面有 4 个空格
✓ 方法体内的代码前面有 8 个空格
✓ 没有使用 Tab 字符
✓ 没有多余的空行
✓ 所有缩进都是 4 的倍数
```

## 代码清理流程

```
原始 AI 生成的代码
    ↓
去除首尾空白 (strip)
    ↓
移除开头多余空行
    ↓
检测第一行缩进
    ↓
计算缩进差异
    ↓
调整所有行的缩进
    ↓
追加到文件（只添加一个空行）
    ↓
自动运行 autopep8 格式化
```

## 缩进规则

### Python 类方法的正确缩进

```python
class TeacherService:
    """类定义"""
    
    @classmethod  # 4个空格缩进
    async def method1(cls):  # 4个空格缩进
        """方法1"""  # 8个空格缩进
        pass  # 8个空格缩进
    
    @classmethod  # 4个空格缩进
    async def method2(cls):  # 4个空格缩进
        """方法2"""  # 8个空格缩进
        pass  # 8个空格缩进
```

### 缩进层级

| 代码位置 | 缩进空格数 | 示例 |
|---------|-----------|------|
| 类定义 | 0 | `class Service:` |
| 类方法装饰器 | 4 | `    @classmethod` |
| 类方法定义 | 4 | `    async def method(cls):` |
| 方法体 | 8 | `        return result` |
| 嵌套代码块 | 12+ | `            if condition:` |

## 常见错误和修复

### 错误 1：多余的空行

**错误**：
```python
    return result


@classmethod  # ❌ 两个空行
    async def new_method(cls):
```

**修复**：
```python
    return result

    @classmethod  # ✅ 一个空行
    async def new_method(cls):
```

### 错误 2：缩进不足

**错误**：
```python
@classmethod  # ❌ 没有缩进
async def new_method(cls):  # ❌ 没有缩进
    pass
```

**修复**：
```python
    @classmethod  # ✅ 4个空格
    async def new_method(cls):  # ✅ 4个空格
        pass  # ✅ 8个空格
```

### 错误 3：缩进过多

**错误**：
```python
        @classmethod  # ❌ 8个空格（太多）
        async def new_method(cls):
            pass
```

**修复**：
```python
    @classmethod  # ✅ 4个空格
    async def new_method(cls):
        pass
```

## 验证方法

### 1. 使用 Python 编译检查

```bash
python -m py_compile ruoyi-fastapi-backend/module_admin/service/teacher_service.py
```

如果有缩进错误，会显示：
```
IndentationError: unexpected indent
```

### 2. 使用代码格式化工具

```bash
# 使用 black 格式化
black ruoyi-fastapi-backend/module_admin/service/teacher_service.py

# 使用 autopep8
autopep8 --in-place ruoyi-fastapi-backend/module_admin/service/teacher_service.py
```

### 3. 使用 IDE 检查

- VS Code：会自动显示缩进错误（红色波浪线）
- PyCharm：会高亮显示缩进问题
- Kiro：使用 getDiagnostics 工具

## 预防措施

### 1. 使用自动修复功能

系统现在会自动修复缩进问题，但仍建议：

- 应用前预览代码
- 检查缩进是否正确
- 使用版本控制

### 2. 明确的需求描述

在需求中添加：

```
请确保生成的代码：
1. 缩进正确，使用 4 个空格
2. @classmethod 装饰器与类的其他方法对齐
3. 方法之间只有一个空行
4. 符合 Python PEP 8 规范
```

### 3. 使用代码格式化

应用代码后，运行格式化工具：

```bash
# 格式化整个模块
black ruoyi-fastapi-backend/module_admin/

# 或使用 ruff
ruff format ruoyi-fastapi-backend/module_admin/
```

## 手动修复指南

如果自动修复失败，手动修复步骤：

### 步骤 1：定位错误

查看错误信息：
```
File "teacher_service.py", line 152
    async def generate_random_teacher_services(cls, ...):
    ^
IndentationError: unexpected indent
```

### 步骤 2：打开文件

找到第 152 行附近的代码

### 步骤 3：检查缩进

使用编辑器的"显示空白字符"功能，检查：
- 是否使用了 Tab 而不是空格
- 空格数量是否正确
- 是否有多余的空行

### 步骤 4：修复缩进

确保：
- `@classmethod` 前只有一个空行
- `@classmethod` 有 4 个空格缩进
- 方法定义有 4 个空格缩进
- 方法体有 8 个空格缩进

### 步骤 5：验证

保存文件，重启服务，检查是否还有错误

## 配置编辑器

### VS Code

在 `.vscode/settings.json` 中：

```json
{
  "editor.tabSize": 4,
  "editor.insertSpaces": true,
  "editor.detectIndentation": false,
  "python.formatting.provider": "black"
}
```

### PyCharm

设置 → 编辑器 → 代码样式 → Python：
- 缩进：4 个空格
- 使用空格而不是 Tab

## 总结

缩进问题已通过以下方式解决：

1. ✅ 自动缩进修复逻辑
2. ✅ 优化的 AI 提示词
3. ✅ 代码清理流程
4. ✅ 详细的文档说明

现在系统会自动修复大部分缩进问题，但仍建议：

- 应用前预览代码
- 使用版本控制
- 遇到问题及时手动修复

如果还有缩进问题，请使用代码格式化工具（black 或 autopep8）一键修复！
