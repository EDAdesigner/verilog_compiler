# 半加器实验总结

## 实现方法

在本实验中，我们使用两种不同的方式实现了半加器：

1. **门级描述法（Gate-level Description）**:
   ```verilog
   xor xor1(a, b, sum);    // 异或门产生和
   and and1(a, b, carry);  // 与门产生进位
   ```

2. **数据流描述法（Dataflow Description）**:
   ```verilog
   assign sum = a ^ b;     // 异或操作产生和
   assign carry = a & b;   // 与操作产生进位
   ```

## 电路结构分析

通过我们的Verilog编译器分析，半加器的结构如下：

### 组件
- 输入端口: a, b
- 输出端口: sum, carry
- 逻辑门: 一个异或门，一个与门

### 连接关系
- 异或门（XOR）: 输入a和b，输出连接到sum
- 与门（AND）: 输入a和b，输出连接到carry

## DOT文件分析

我们的编译器成功生成了描述半加器结构的DOT文件：

1. **门级描述生成的DOT**:
   ```
   digraph half_adder {
      graph [rankdir=LR]
      a [color=blue shape=triangle]
      b [color=blue shape=triangle]
      sum [color=red shape=triangle]
      carry [color=red shape=triangle]
      xor1 [label=xor shape=box]
      a -> xor1
      b -> xor1
      xor1 -> sum
      and1 [label=and shape=box]
      a -> and1
      b -> and1
      and1 -> carry
   }
   ```

2. **数据流描述生成的DOT**:
   ```
   digraph half_adder_assign {
      graph [rankdir=LR]
      a [color=blue shape=triangle]
      b [color=blue shape=triangle]
      sum [color=red shape=triangle]
      carry [color=red shape=triangle]
      "^_0" [label="^" shape=box]
      a -> "^_0"
      b -> "^_0"
      "^_0" -> sum
      "&_1" [label="&" shape=box]
      a -> "&_1"
      b -> "&_1"
      "&_1" -> carry
   }
   ```

可以看出，无论是使用门级描述还是数据流描述，生成的电路结构本质上是相同的。

## 总结

半加器是数字电路中最基本的组件之一，用于实现单比特的加法操作。它通过组合异或门和与门实现了二进制加法的基本功能，为构建更复杂的数字电路（如全加器、多位加法器）奠定了基础。

我们的Verilog编译器成功地提取了半加器的结构信息，并生成了便于可视化的DOT表示。 