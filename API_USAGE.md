# Verilog编译器API使用说明

## 概述

这是一个基于FastAPI的Verilog编译器API服务，提供两个主要端点：
- `/verilog` - 编译Verilog代码并生成电路图
- `/optimize` - 使用优化版本编译Verilog代码并生成电路图

## 启动服务器

### 方法1: 使用启动脚本
```bash
./start_server.sh
```

### 方法2: 直接运行
```bash
cd src
python3 server.py
```

服务器将在 `http://localhost:8000` 上运行。

## API端点

### 1. 根路径
- **URL**: `GET /`
- **描述**: 获取API服务信息
- **响应示例**:
```json
{
  "message": "Verilog编译器API服务",
  "version": "1.0.0",
  "endpoints": {
    "/verilog": "编译Verilog代码（POST）",
    "/optimize": "优化编译Verilog代码（POST）"
  },
  "optimization_available": true
}
```

### 2. 健康检查
- **URL**: `GET /health`
- **描述**: 检查服务状态
- **响应示例**:
```json
{
  "status": "healthy",
  "optimization_available": true
}
```

### 3. Verilog编译
- **URL**: `POST /verilog`
- **描述**: 编译Verilog代码并生成电路图
- **参数**:
  - `verilog_code` (string, 必需): Verilog源代码
  - `enhanced_style` (boolean, 可选): 是否使用增强样式，默认true
- **响应示例**:
```json
{
  "status": "success",
  "message": "Verilog代码编译成功",
  "files": {
    "dot_file": "output/uuid.dot",
    "png_file": "output/uuid.png"
  },
  "module_info": {
    "name": "module_uuid",
    "inputs": ["a", "b", "sel"],
    "outputs": ["out"],
    "wires": ["w1", "w2"],
    "gates_count": 0,
    "assigns_count": 3
  }
}
```

### 4. 优化编译
- **URL**: `POST /optimize`
- **描述**: 使用优化版本编译Verilog代码并生成电路图
- **参数**:
  - `verilog_code` (string, 必需): Verilog源代码
  - `enhanced_style` (boolean, 可选): 是否使用增强样式，默认true
- **响应**: 与 `/verilog` 相同

## 使用示例

### 使用curl

#### 编译Verilog代码
```bash
curl -X POST "http://localhost:8000/verilog" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "verilog_code=module test(input a, input b, output out); assign out = a & b; endmodule" \
  -d "enhanced_style=true"
```

#### 优化编译
```bash
curl -X POST "http://localhost:8000/optimize" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "verilog_code=module test(input a, input b, output out); assign out = a & b; endmodule" \
  -d "enhanced_style=true"
```

### 使用Python requests

```python
import requests

# Verilog代码
verilog_code = """
module test_module(
    input a,
    input b,
    input sel,
    output out
);
    wire w1, w2;
    
    assign w1 = a & b;
    assign w2 = a | b;
    assign out = sel ? w1 : w2;
    
endmodule
"""

# 编译请求
data = {
    "verilog_code": verilog_code,
    "enhanced_style": True
}

# 发送请求
response = requests.post("http://localhost:8000/verilog", data=data)

if response.status_code == 200:
    result = response.json()
    print("编译成功!")
    print(f"DOT文件: {result['files']['dot_file']}")
    print(f"PNG文件: {result['files']['png_file']}")
    print(f"模块信息: {result['module_info']}")
else:
    print(f"错误: {response.text}")
```

### 使用JavaScript fetch

```javascript
const verilogCode = `
module test_module(
    input a,
    input b,
    input sel,
    output out
);
    wire w1, w2;
    
    assign w1 = a & b;
    assign w2 = a | b;
    assign out = sel ? w1 : w2;
    
endmodule
`;

const formData = new FormData();
formData.append('verilog_code', verilogCode);
formData.append('enhanced_style', 'true');

fetch('http://localhost:8000/verilog', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.status === 'success') {
        console.log('编译成功!');
        console.log('DOT文件:', data.files.dot_file);
        console.log('PNG文件:', data.files.png_file);
        console.log('模块信息:', data.module_info);
    } else {
        console.error('编译失败:', data);
    }
})
.catch(error => console.error('请求错误:', error));
```

## 测试API

运行测试脚本：
```bash
python3 test_server.py
```

## 输出文件

所有生成的文件都保存在 `output/` 目录中，使用UUID作为文件名以确保唯一性：
- `.dot` 文件：DOT格式的图形描述文件
- `.png` 文件：生成的电路图图片

## 错误处理

常见错误码：
- `400`: 请求参数错误
- `500`: 服务器内部错误（通常是编译失败）
- `503`: 优化模块不可用

## 注意事项

1. 确保服务器正在运行
2. 检查依赖是否正确安装
3. 优化模块需要 `verilog_optimize` 包正确配置
4. 生成的图片文件需要Graphviz支持
5. 所有文件路径都是相对于项目根目录的

## API文档

启动服务器后，可以在浏览器中访问以下地址查看交互式API文档：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc` 