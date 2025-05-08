from graphviz import Digraph
import os
import re

class DotGenerator:
    def __init__(self, module):
        self.module = module
        self.dot = Digraph(name=module.name)
        self.dot.attr('graph', rankdir='LR')  # 从左到右的布局
        
        # 节点计数器（用于表达式中生成的临时节点）
        self.node_counter = 0
        
    def generate_dot(self):
        # 创建输入节点
        for input_name in self.module.inputs:
            self.dot.node(input_name, input_name, shape='triangle', color='blue')
            
        # 创建输出节点
        for output_name in self.module.outputs:
            self.dot.node(output_name, output_name, shape='triangle', color='red')
            
        # 创建wire节点
        for wire_name in self.module.wires:
            self.dot.node(wire_name, wire_name, shape='point')
            
        # 处理门级实例化
        for gate in getattr(self.module, 'gates', []):
            gate_node = f"{gate.gate_type}_{gate.name}"
            self.dot.node(gate_node, label=gate.gate_type, shape='box')
            # 输入连到门
            for inp in gate.inputs:
                self.dot.edge(inp, gate_node)
            # 门连到输出
            self.dot.edge(gate_node, gate.output)
            
        # 处理赋值语句
        for assign in getattr(self.module, 'assigns', []):
            output_node = self._process_expression(assign.right)
            self.dot.edge(output_node, assign.left)
            
        return self.dot
        
    def _process_expression(self, expr):
        # 如果表达式是简单的标识符或数字
        if isinstance(expr, str) or isinstance(expr, int):
            if isinstance(expr, int):
                node_id = f"const_{expr}_{self.node_counter}"
                self.node_counter += 1
                self.dot.node(node_id, label=str(expr), shape='box', style='filled', fillcolor='lightgrey')
                return node_id
            return expr
        # 一元操作（如~）
        if isinstance(expr, dict) and expr.get('op') == '~':
            node_id = f"~_{self.node_counter}"
            self.node_counter += 1
            self.dot.node(node_id, label='~', shape='box')
            right_id = self._process_expression(expr['right'])
            self.dot.edge(right_id, node_id)
            return node_id
        # 二元操作
        if isinstance(expr, dict) and 'left' in expr and 'right' in expr:
            op = expr['op']
            node_id = f"{op}_{self.node_counter}"
            self.node_counter += 1
            self.dot.node(node_id, label=op, shape='box')
            left_id = self._process_expression(expr['left'])
            right_id = self._process_expression(expr['right'])
            self.dot.edge(left_id, node_id)
            self.dot.edge(right_id, node_id)
            return node_id
        return str(expr)
        
    def save(self, output_path=None):
        """保存DOT文件和图形图片"""
        if output_path is None:
            output_path = f"{self.module.name}"
            
        # 移除文件扩展名（如果有）
        base_path = os.path.splitext(output_path)[0]
        
        # 保存DOT文件
        dot_file = f"{base_path}.dot"
        self.dot.save(dot_file)
        
        # 渲染并保存图片
        png_file = f"{base_path}.png"
        self.dot.render(base_path, format='png', cleanup=True)
        
        return dot_file, png_file 