"""
工具显示格式化器测试

演示如何使用格式化器将技术性的工具调用转换为业务友好的显示
"""
from module_ai.utils.tool_display_formatter import format_tool_call, format_tool_result


def test_execute_command():
    """测试命令执行工具的格式化"""
    print('=' * 80)
    print('测试 1: 命令执行工具')
    print('=' * 80)
    
    # 原始工具调用（技术性）
    tool_name = 'execute_command'
    tool_args = {
        'command': 'curl -s "https://zh.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles=博威合金材料股份有限公司&exintro=&formatversion=2" | python3 -c "import json,sys; data=json.load(sys.stdin); pages=data.get(\'query\',{}).get(\'pages\',[{}]); print(pages[0].get(\'extract\',\'\')[:500] if pages else \'未找到信息\')"',
        'timeout': 15,
    }
    
    print('\n【原始显示】（业务人员看不懂）')
    print(f'ToolExecution(tool_call_id="call_f8da41f7321a4092ab6ed045", tool_name="{tool_name}", tool_args={tool_args})')
    
    print('\n【友好显示】（业务人员能看懂）')
    friendly_display = format_tool_call(tool_name, tool_args)
    print(friendly_display)
    
    # 模拟执行结果
    print('\n【执行结果】')
    result = '博威合金材料股份有限公司成立于1993年，总部位于浙江省宁波市，是一家专业从事高性能合金材料研发、生产和销售的高新技术企业...'
    result_display = format_tool_result(tool_name, result, success=True)
    print(result_display)


def test_execute_python():
    """测试 Python 代码执行工具的格式化"""
    print('\n' + '=' * 80)
    print('测试 2: Python 代码执行工具')
    print('=' * 80)
    
    tool_name = 'execute_python_code'
    tool_args = {
        'code': '''import json
bowei_info = {
    "company_name": "宁波博威合金材料股份有限公司",
    "english_name": "Ningbo Boway Alloy Material Co., Ltd.",
    "stock_code": "601137.SH",
    "founded": "1993年",
    "headquarters": "浙江省宁波市",
    "main_business": "高性能合金材料的研发、生产和销售",
    "products": ["高端铜合金板材", "精密合金材料", "新能源材料"],
    "key_features": ["国家高新技术企业", "中国有色金属行业龙头企业", "拥有多项核心技术专利"]
}
print(json.dumps(bowei_info, ensure_ascii=False, indent=2))''',
        'timeout': 10,
    }
    
    print('\n【原始显示】（技术细节太多）')
    print(f'ToolExecution(tool_name="{tool_name}", tool_args={{"code": "...(省略)", "timeout": 10}})')
    
    print('\n【友好显示】（清晰明了）')
    friendly_display = format_tool_call(tool_name, tool_args)
    print(friendly_display)
    
    print('\n【执行结果】')
    result = '''{"company_name": "宁波博威合金材料股份有限公司", "english_name": "Ningbo Boway Alloy Material Co., Ltd.", ...}'''
    result_display = format_tool_result(tool_name, result, success=True)
    print(result_display)


def test_web_search():
    """测试网页搜索工具的格式化"""
    print('\n' + '=' * 80)
    print('测试 3: 网页搜索工具')
    print('=' * 80)
    
    tool_name = 'web_search'
    tool_args = {
        'query': '博威合金材料股份有限公司 最新财报',
    }
    
    print('\n【友好显示】')
    friendly_display = format_tool_call(tool_name, tool_args)
    print(friendly_display)
    
    print('\n【执行结果】')
    result = '找到 5 条相关结果：\n1. 博威合金2024年第三季度财报...\n2. 博威合金发布年度业绩预告...'
    result_display = format_tool_result(tool_name, result, success=True)
    print(result_display)


def test_error_case():
    """测试错误情况的格式化"""
    print('\n' + '=' * 80)
    print('测试 4: 错误情况')
    print('=' * 80)
    
    tool_name = 'execute_command'
    tool_args = {
        'command': 'invalid_command_that_does_not_exist',
        'timeout': 5,
    }
    
    print('\n【友好显示】')
    friendly_display = format_tool_call(tool_name, tool_args)
    print(friendly_display)
    
    print('\n【执行结果】（失败）')
    result = 'Error: Command not found: invalid_command_that_does_not_exist'
    result_display = format_tool_result(tool_name, result, success=False)
    print(result_display)


if __name__ == '__main__':
    print('🎨 工具显示格式化器测试\n')
    
    test_execute_command()
    test_execute_python()
    test_web_search()
    test_error_case()
    
    print('\n' + '=' * 80)
    print('✅ 所有测试完成')
    print('=' * 80)
    print('\n💡 使用建议：')
    print('1. 在前端 AI 对话框中使用格式化器显示工具调用')
    print('2. 将原始的技术细节隐藏在"查看详情"按钮后面')
    print('3. 默认显示业务友好的格式化信息')
    print('4. 可以根据需要扩展更多工具类型的格式化')
