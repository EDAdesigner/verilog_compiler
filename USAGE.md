# Verilog编译器使用说明

## 环境准备

### 安装依赖

1. 确保您的系统已安装Python 3.x版本
2. 运行安装脚本以准备环境：
   ```
   python setup.py
   ```
   这将自动安装所需的依赖项并创建示例文件。

### 安装Graphviz（必须）

本编译器使用Graphviz生成图形，因此需要在系统中安装Graphviz：

1. 访问 [Graphviz官方下载页面](https://graphviz.org/download/)
2. 下载并安装Windows版本
3. 确保将Graphviz的bin目录添加到系统PATH环境变量中

## 使用方法

### 命令行方式

```
python main.py <your_verilog_file.v>
```

例如：
```
python main.py examples/full_adder.v
```

### 使用批处理脚本

```
compile_verilog.bat <your_verilog_file.v>
```

例如：
```
compile_verilog.bat examples/full_adder.v
```

## 输出文件

编译器会生成两个文件：

1. `.dot` - DOT格式的图形描述文件
2. `.png` - 由DOT文件渲染生成的图形文件

这两个文件会与输入的Verilog文件位于同一目录，并使用相同的文件名（但扩展名不同）。

## 示例文件

本项目包含两个示例Verilog文件：

1. `examples/full_adder.v` - 一个全加器的实现
2. `examples/expression_test.v` - 测试表达式解析和运算符优先级

## 支持的Verilog特性

- 模块声明
- 输入/输出端口
- 线网声明
- 门实例化（and, or, not, nand, nor, xor, xnor, buf）
- assign语句
- 表达式（支持一元和二元运算符，及优先级）
- 括号表达式

## 故障排除

### 常见问题

1. **错误："找不到graphviz"**
   - 确保已正确安装Graphviz并将其bin目录添加到PATH

2. **警告："Token 'X' defined, but not used"**
   - 这是PLY库的警告，不影响程序功能

3. **无法生成图形文件**
   - 检查Graphviz安装
   - 确保输入的Verilog文件语法正确

### 日志

编译器运行时会在控制台输出详细的进度信息和错误消息，可以帮助诊断问题。 