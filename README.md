# Verilog编译器

这是一个简易的Verilog编译器，可以将Verilog文件(.v)解析并生成DOT格式的图形表示。

## 项目结构

```
verilog_compiler/
├── src/                    # 源代码目录
│   ├── main.py            # 主程序
│   ├── verilog_parser.py  # Verilog解析器
│   ├── dot_generator.py   # DOT图形生成器
│   ├── verilog_lexer.py   # 词法分析器
│   ├── server.py          # API服务器
│   ├── generate_mux.py    # 多路选择器生成器
│   ├── generate_spmux.py  # 精确样式多路选择器生成器
│   ├── module_library.py  # 常用模块库
│   └── verilog_optimize/  # 优化相关代码
├── script/                 # 脚本文件目录
│   ├── compile_verilog.bat # 编译脚本
│   └── start_server.bat   # 启动服务器脚本
├── input/                  # 输入文件目录
│   └── *.v                # Verilog源文件
├── output/                 # 输出文件目录
│   ├── *.dot              # 生成的DOT文件
│   └── *.png              # 生成的图形文件
└── tests/                  # 测试文件目录
```

## 功能特点

- 支持Verilog端口、门级信息提取
- 支持多元表达式解析
- 支持一元运算
- 考虑运算符优先级
- 支持括号表达式
- 自动生成图形文件
- 提供API服务接口
- 支持共享子表达式优化
- 支持特殊电路图样式与符号编号
- **新增**: 增强型电路图生成，自动识别电路类型并应用适当样式

## 使用方法

### 命令行使用

基本用法（使用增强型电路图生成器）：
```
python src/main.py input/example.v
```

使用传统样式（原始电路图生成器）：
```
python src/main.py input/example.v --classic
```

启用优化选项：
```
python src/main.py input/example.v --optimize
```

或者使用批处理文件：

```
script/compile_verilog.bat input/example.v
```

这将生成一个同名的.dot文件和图形文件(.png)在output目录中。

### 特殊电路图生成

生成多路选择器图形：

```
python src/generate_mux.py
```

生成精确样式的多路选择器图形：

```
python src/generate_spmux.py
```

### API服务器使用

启动API服务器：

```
script/start_server.bat
```

或者：

```
python src/server.py
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
python tests/test_api.py
```

## 电路图样式

本编译器支持生成多种样式的电路图：

1. **标准样式** - 传统的箭头连接的节点图
2. **模块框样式** - 类似原理图的矩形框表示
3. **精确样式** - 与指定参考图完全一致的样式，包括符号编号

电路图样式示例:

```
+-------+
|   A   |
|   B   | $26  |   Y   |
|   S   | Spmux|       |
+-------+
```

## 环境要求

- Python 3.x
- Graphviz (用于生成图形)
- FastAPI (用于API服务)
- Uvicorn (用于运行服务器)
- PLY (用于词法和语法分析)

## 安装依赖

```
pip install -r src/requirements.txt
```

## 输出文件

所有生成的文件都保存在`output`目录中。对于API调用，使用UUID作为文件名以确保唯一性。API返回的响应中包含生成文件的路径信息。

# Verilog/BLIF 调度与可视化工具

## 简介
本工具支持对 BLIF 文件进行 ML-RCS 调度，并输出调度结果与门级甘特图。适用于数字电路综合、优化与可视化分析。

## 依赖环境
- Python 3.7+
- matplotlib

安装依赖：
```bash
pip install matplotlib
```

## 使用方法

### 1. 命令行调度与输出

基本用法：
```bash
python src/schedule.py <输入BLIF文件> <输出TXT文件>
```

例如：
```bash
python src/schedule.py examples/sample.blif output/sample.txt
```

### 2. 生成并保存甘特图

在命令后加 `--plot` 参数：
```bash
python src/schedule.py examples/sample.blif output/sample.txt --plot
```
- 程序会自动弹出甘特图窗口
- 并将图片保存为 `output/gantt.png`

### 3. 输出文件说明
- 输出TXT文件包含：
  - 输入输出信号列表
  - 总调度周期数
  - 每周期调度门列表
  - 每个门的开始时间、结束时间
- 输出图片为门级调度甘特图，横坐标为时间，纵坐标为门名，颜色区分门类型（浅色系）。

## 结果示例
```
Input :a, b, c, d, e, f  Output :o, p, q
Total 8 Cycles
Cycle 0:{h, g, i}
Cycle 1:{p}
Cycle 2:{}
Cycle 3:{j}
Cycle 4:{l, m}
Cycle 5:{}
Cycle 6:{n, k}
Cycle 7:{o, q}
Minimize Cycle: 8
h: Start Time: 0, End Time: 0
...
```

## 其他说明
- 支持自定义BLIF文件输入
- 支持自定义输出路径
- 支持自动保存甘特图

如有问题或需定制功能，请联系开发者。
