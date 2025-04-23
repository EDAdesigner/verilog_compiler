# Verilog编译器

这是一个简易的Verilog编译器，可以将Verilog文件(.v)解析并生成DOT格式的图形表示。

## 功能特点

- 支持Verilog端口、门级信息提取
- 支持多元表达式解析
- 支持一元运算
- 考虑运算符优先级
- 支持括号表达式
- 自动生成图形文件
- 提供API服务接口

## 使用方法

### 命令行使用

```
python main.py <input_file.v>
```

这将生成一个同名的.dot文件和图形文件(.png)。

### API服务器使用

启动API服务器：

```
python server.py
```

服务器将在 `http://localhost:8000` 上运行。您可以通过以下方式使用API：

- POST `/verilog` - 提交Verilog代码并获取生成的图像

请求示例：

```json
{
  "code": "module test(a, b, c); input a, b; output c; assign c = a & b; endmodule"
}
```

响应示例：

```json
{
  "status": "success",
  "module_name": "verilog_1234abcd",
  "base64_image": "base64编码的图像数据"
}
```

### API文档

访问 `http://localhost:8000/docs` 获取API文档。

## 环境要求

- Python 3.x
- Graphviz (用于生成图形)
- FastAPI (用于API服务)
- Uvicorn (用于运行服务器)
- PIL/Pillow (用于图像处理)

## 安装依赖

```
pip install -r requirements.txt
```

## 测试API

```
python examples/test_api.py
``` 