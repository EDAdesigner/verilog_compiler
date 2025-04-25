import hashlib
from typing import Dict, List, Set, Tuple

class Expression:
    def __init__(self, op=None, operands=None, value=None):
        self.op = op  # 操作符
        self.operands = operands if operands else []  # 操作数列表
        self.value = value  # 如果是常量或变量，存储其值
        self._hash = None

    def __hash__(self):
        if self._hash is None:
            # 为了确保相同的表达式有相同的哈希值，我们需要标准化
            if self.op is None:
                self._hash = hash(str(self.value))
            else:
                # 对操作数排序以确保 a+b 和 b+a 有相同的哈希值
                sorted_operands = sorted(str(hash(op)) for op in self.operands)
                hash_str = f"{self.op}{''.join(sorted_operands)}"
                self._hash = hash(hash_str)
        return self._hash

    def __eq__(self, other):
        if not isinstance(other, Expression):
            return False
        if self.op != other.op:
            return False
        if self.value != other.value:
            return False
        if len(self.operands) != len(other.operands):
            return False
        # 对于操作数，我们需要考虑顺序无关性
        if self.op in {'+', '*', '&', '|', '^', 'xnor'}:
            return set(self.operands) == set(other.operands)
        return self.operands == other.operands

class CSEOptimizer:
    def __init__(self):
        self.expressions = {}  # 存储表达式及其对应的wire
        self.temp_wire_count = 0

    def _get_expression_key(self, expr):
        """生成表达式的唯一标识符"""
        if isinstance(expr, dict):
            if 'op' in expr:
                if expr['op'] == '+':
                    left_key = self._get_expression_key(expr['left'])
                    right_key = self._get_expression_key(expr['right'])
                    return f"({left_key}+{right_key})"
                elif expr['op'] == '&':
                    left_key = self._get_expression_key(expr['left'])
                    right_key = self._get_expression_key(expr['right'])
                    return f"({left_key}&{right_key})"
        return str(expr)

    def _process_expression(self, expr, module):
        """处理表达式，返回对应的wire名称"""
        if isinstance(expr, dict):
            expr_key = self._get_expression_key(expr)
            if expr_key in self.expressions:
                # 如果表达式已经存在，直接返回对应的wire
                return self.expressions[expr_key]
            else:
                # 如果是新表达式，创建新的wire
                if expr['op'] == '+' or expr['op'] == '&':
                    left_wire = self._process_expression(expr['left'], module)
                    right_wire = self._process_expression(expr['right'], module)
                    result_wire = f'temp_wire_{self.temp_wire_count}'
                    self.temp_wire_count += 1
                    
                    if result_wire not in module.wires:
                        module.wires.append(result_wire)
                    
                    # 创建新的赋值语句
                    new_expr = {'op': expr['op'], 'left': left_wire, 'right': right_wire}
                    from verilog_parser import Assignment
                    module.assigns.append(Assignment(result_wire, new_expr))
                    self.expressions[expr_key] = result_wire
                    return result_wire
        return expr

    def optimize_module(self, module):
        """优化整个模块的共享子表达式"""
        # 重置状态
        self.expressions = {}
        self.temp_wire_count = 0
        
        # 处理所有赋值语句
        optimized_assigns = []
        for assign in module.assigns:
            if isinstance(assign.right, dict):
                # 处理复杂表达式
                result_wire = self._process_expression(assign.right, module)
                # 创建一个新的简单赋值
                optimized_assigns.append(Assignment(assign.left, result_wire))
            else:
                # 保持简单赋值不变
                optimized_assigns.append(assign)
        
        # 更新模块的赋值语句
        module.assigns = optimized_assigns
        return module

class Assignment:
    def __init__(self, left, right):
        self.left = left
        self.right = right 