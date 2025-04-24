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
- 支持共享子表达式优化

## 使用方法

### 命令行使用

```
python main.py <input_file.v>
```

这将生成一个同名的.dot文件和图形文件(.png)。

### API服务器使用

启动API服务器：

```
start_server.bat
```

或者：

```
python server.py
```

服务器将在 http://localhost:8000 上运行。

#### API端点

1. `/verilog` - 解析Verilog代码并生成图形
   - 方法：POST
   - 参数：verilog_code (表单字段)
   - 返回：包含状态和生成文件路径的JSON

2. `/optimize` - 解析并优化Verilog代码，然后生成图形
   - 方法：POST
   - 参数：verilog_code (表单字段)
   - 返回：包含状态和生成文件路径的JSON

#### 测试API

```
python test_api.py
```

## 环境要求

- Python 3.x
- Graphviz (用于生成图形)
- FastAPI (用于API服务)
- Uvicorn (用于运行服务器)
- PLY (用于词法和语法分析)

## 安装依赖

```
pip install -r requirements.txt
```

## 输出文件

所有通过API生成的文件都保存在`output`目录中，使用UUID作为文件名以确保唯一性。API返回的响应中包含生成文件的路径信息。 