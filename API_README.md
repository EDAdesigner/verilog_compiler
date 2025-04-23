# Verilog编译器 API 使用说明

本文档详细介绍如何使用 Verilog 编译器的 API 服务。

## API 服务概述

Verilog 编译器 API 服务提供了一个简单的 HTTP 接口，用于将 Verilog 代码转换为图像表示。服务接收 Verilog 代码文本，并返回生成的 DOT 文件和 PNG 图像的路径及可访问的URL。

## 启动服务

要启动 API 服务，请执行以下命令：

```bash
python server.py
```

服务默认在 `http://localhost:8000` 上运行。

## API 端点

### POST /verilog

此端点用于提交 Verilog 代码并获取生成的图像。

#### 请求格式

```json
{
  "code": "您的Verilog代码"
}
```

#### 响应格式

成功时：

```json
{
  "success": true,
  "module_name": "verilog_uuid",
  "dot_file": "./result/verilog_uuid.dot",
  "png_file": "./result/verilog_uuid.png",
  "dot_url": "http://localhost:8000/result/verilog_uuid.dot",
  "png_url": "http://localhost:8000/result/verilog_uuid.png"
}
```

失败时：

```json
{
  "error": "错误信息"
}
```

## 使用示例

### 使用 curl

```bash
curl -X POST "http://localhost:8000/verilog" \
     -H "Content-Type: application/json" \
     -d '{"code":"module test(a, b, c); input a, b; output c; assign c = a & b; endmodule"}'
```

### 使用 Python requests

```python
import requests

url = "http://localhost:8000/verilog"
payload = {
    "code": "module test(a, b, c); input a, b; output c; assign c = a & b; endmodule"
}

response = requests.post(url, json=payload)
data = response.json()
print(data)

# 直接访问生成的图像
if "png_url" in data:
    image_url = data["png_url"]
    print(f"图像链接: {image_url}")
```

### 使用 JavaScript fetch

```javascript
fetch('http://localhost:8000/verilog', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    code: 'module test(a, b, c); input a, b; output c; assign c = a & b; endmodule'
  }),
})
.then(response => response.json())
.then(data => {
  console.log(data);
  // 显示生成的图像
  if (data.png_url) {
    const img = document.createElement('img');
    img.src = data.png_url;
    document.body.appendChild(img);
  }
});
```

## 访问生成的文件

服务提供静态文件服务，您可以直接通过返回的URL访问生成的DOT文件和PNG图像：

- DOT文件: `http://localhost:8000/result/verilog_uuid.dot`
- PNG图像: `http://localhost:8000/result/verilog_uuid.png`

文件也存储在服务器的 `./result` 目录中。

## API 文档

访问 `http://localhost:8000/docs` 查看完整的 API 文档（由 FastAPI 自动生成）。

## 故障排除

如果遇到问题，请检查以下几点：

1. 确保 Verilog 代码语法正确
2. 确保服务器有权限写入 `./result` 目录
3. 确保已安装所有依赖（`pip install -r requirements.txt`）
4. 查看服务器日志以获取详细错误信息 