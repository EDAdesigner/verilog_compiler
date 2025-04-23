# Verilog编译器使用说明

## 环境准备

### 安装依赖

1. 确保您的系统已安装Python 3.x版本
2. 安装所需的Python包：
   ```
   pip install ply graphviz
   ```

### 安装Graphviz（必须）

本编译器使用Graphviz生成图形，因此需要在系统中安装Graphviz：

1. 访问 [Graphviz官方下载页面](https://graphviz.org/download/)
2. 下载并安装Windows版本
3. 确保将Graphviz的bin目录添加到系统PATH环境变量中

## 使用方法

### 命令行方式

基本用法：
```
python main.py <your_verilog_file.v>
```

启用优化选项：
```
python main.py <your_verilog_file.v> --optimize
```
或
```
python main.py <your_verilog_file.v> -o
```

例如：
```
python main.py examples/full_adder.v
python main.py examples/full_adder.v --optimize
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
如果使用了优化选项，输出文件名会包含"_optimized"后缀。

## 示例文件

本项目包含两个示例Verilog文件：

1. `examples/full_adder.v` - 一个全加器的实现
2. `examples/expression_test.v` - 测试表达式解析和运算符优先级

## 支持的Verilog特性

- 模块声明
- 输入/输出端口
- wire声明
- 基本门实例化：
  - and
  - or
  - not
  - nand
  - nor
  - xor
  - xnor
  - buf
- assign语句
- 表达式：
  - 加法运算 (+)
  - 与运算 (&)
  - 括号表达式

## 优化功能

编译器支持以下优化：

1. 共享子表达式优化
   - 自动检测并重用相同的子表达式
   - 通过临时wire变量存储中间结果
   - 减少电路中重复的逻辑门

使用 `--optimize` 或 `-o` 选项启用优化功能。

## 故障排除

### 常见问题

1. **错误："找不到graphviz"**
   - 确保已正确安装Graphviz并将其bin目录添加到PATH

2. **错误："无法导入优化模块"**
   - 确保所有Python文件都在正确的目录结构中
   - 检查是否正确安装了所有依赖包

3. **无法生成图形文件**
   - 检查Graphviz安装
   - 确保输入的Verilog文件语法正确
   - 检查文件写入权限

### 错误信息

编译器会在控制台输出详细的错误信息：

- 语法错误：显示错误发生的行号和具体内容
- 文件操作错误：显示具体的文件访问问题
- 优化相关错误：显示优化过程中遇到的问题

如果遇到问题，请查看控制台输出的完整错误信息以进行诊断。 