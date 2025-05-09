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

基本用法（使用增强型电路图生成器）：
```
python main.py <your_verilog_file.v>
```

使用传统样式（原始电路图生成器）：
```
python main.py <your_verilog_file.v> --classic
```
或
```
python main.py <your_verilog_file.v> -c
```

启用优化选项：
```
python main.py <your_verilog_file.v> --optimize
```
或
```
python main.py <your_verilog_file.v> -o
```

同时使用多个选项：
```
python main.py <your_verilog_file.v> --optimize --classic
```

例如：
```
python main.py examples/half_adder.v
python main.py examples/multiplexer.v --classic
python main.py examples/test_circuit.v --optimize
```

### 特殊电路图生成

生成多路选择器图形：
```
python src/generate_mux.py
```

生成与参考图像一致的多路选择器：
```
python src/generate_spmux.py
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

## 电路图样式

编译器支持多种不同的电路图表示样式：

1. **增强样式（默认）** - 根据电路类型自动选择合适的表示方式
   ```
   python main.py examples/half_adder.v
   ```

2. **传统样式** - 使用简单的节点和箭头表示
   ```
   python main.py examples/half_adder.v --classic
   ```

3. **模块框样式** - 使用矩形框和端口组表示的样式，更接近电路原理图
   ```
   python src/generate_mux.py
   ```

4. **精确样式** - 与参考图像完全一致的样式，包括符号编号
   ```
   python src/generate_spmux.py
   ```

### 增强型电路图生成器

增强型电路图生成器可以自动识别电路类型并应用合适的图形样式：

1. **多路选择器(Multiplexer)** - 当检测到模块名称包含"mux"或"select"时
   - 自动识别数据输入和选择信号输入
   - 使用$nn格式的符号编号
   - 使用"Spmux"作为模块类型名称

2. **加法器(Adder)** - 当检测到模块名称包含"adder"时
   - 自动识别a、b、cin输入和sum、cout输出
   - 根据名称是否包含"half"或"full"确定加法器类型
   - 使用标准模块表示

3. **默认样式** - 对于其他类型的电路
   - 使用统一的模块框样式
   - 采用$nn格式的符号编号
   - 保持模块原始名称

### 符号编号格式

符号编号采用以下格式：
- 格式：`$nn`，其中nn为两位数字
- 示例：`$26`表示26号模块
- 符号编号显示在模块的左上角

### 特殊模块类型

目前支持的特殊模块类型包括：

1. **Spmux** - 多路选择器
   - 输入：A, B, S
   - 输出：Y
   - 功能：根据S的值选择A或B作为输出

2. **Decoder** - 解码器
   - 输入：I0, I1, ...
   - 输出：Y0, Y1, ...
   - 功能：将二进制输入解码为单热码输出

3. **Register** - 寄存器
   - 输入：D0-Dn, CLK, RST, LD
   - 输出：Q0-Qn
   - 功能：时序存储数据位

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