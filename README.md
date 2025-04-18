# Verilog编译器

这是一个简易的Verilog编译器，可以将Verilog文件(.v)解析并生成DOT格式的图形表示。

## 功能特点

- 支持Verilog端口、门级信息提取
- 支持多元表达式解析
- 支持一元运算
- 考虑运算符优先级
- 支持括号表达式
- 自动生成图形文件

## 使用方法

```
python main.py <input_file.v>
```

这将生成一个同名的.dot文件和图形文件(.png)。

## 环境要求

- Python 3.x
- Graphviz (用于生成图形)
- 必须在Windows 11操作系统上运行

## 安装依赖

```
pip install -r requirements.txt
``` 