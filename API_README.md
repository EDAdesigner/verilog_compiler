# Verilog编译器 API 使用说明

本文档详细介绍如何使用 Verilog 编译器的 API 服务。

## API 服务概述

Verilog 编译器 API 服务提供了一个简单的 HTTP 接口，用于将 Verilog 代码转换为图像表示。服务接收 Verilog 代码文本，并返回生成的图像的base64编码。

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
  "status": "success",
  "module_name": "verilog_uuid",
  "base64_image": "base64编码的图像数据"
}
```

失败时：

```json
{
  "status": "error",
  "message": "错误信息"
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
import base64
from io import BytesIO
from PIL import Image

url = "http://localhost:8000/verilog"
payload = {
    "code": "module test(a, b, c); input a, b; output c; assign c = a & b; endmodule"
}

response = requests.post(url, json=payload)
data = response.json()

if data["status"] == "success":
    # 从base64字符串获取图像
    image_data = base64.b64decode(data["base64_image"])
    image = Image.open(BytesIO(image_data))
    
    # 显示或保存图像
    image.show()  # 显示图像
    # 或保存图像
    # image.save("verilog_graph.png")
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
  if (data.status === 'success') {
    // 显示base64编码的图像
    const img = document.createElement('img');
    img.src = 'data:image/png;base64,' + data.base64_image;
    document.body.appendChild(img);
  } else {
    console.error(data.message);
  }
});
```

## API 文档

访问 `http://localhost:8000/docs` 查看完整的 API 文档（由 FastAPI 自动生成）。

## 故障排除

如果遇到问题，请检查以下几点：

1. 确保 Verilog 代码语法正确
2. 确保服务器有权限写入 `./result` 目录
3. 确保已安装所有依赖（`pip install -r requirements.txt`）
4. 查看服务器日志以获取详细错误信息 