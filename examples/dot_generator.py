from graphviz import Digraph
import os
import re

class DotGenerator:
    def __init__(self, module):
        self.module = module
        self.dot = Digraph(name=module.name)
        # 修改图表方向从上到下
        self.dot.attr('graph', rankdir='LB', splines='ortho', nodesep='0.5')
    
        # 设置节点默认样式
        self.dot.attr('node', shape='record', style='filled', fillcolor='white', 
                    fontname='Arial', height='0.6', width='1.2')
        # 设置边默认样式
        self.dot.attr('edge', arrowsize='0.7')
        
        # 节点计数器（用于表达式中生成的临时节点）
        self.node_counter = 0
        
    def generate_dot(self):
        # 创建输入节点组
        for i, input_name in enumerate(self.module.inputs):
            self.dot.node(input_name, input_name, shape='ellipse', fillcolor='lightblue', style='filled')
        
        # 创建输出节点组
        for i, output_name in enumerate(self.module.outputs):
            self.dot.node(output_name, output_name, shape='ellipse', fillcolor='lightgreen', style='filled')
        
        # 创建主模块框
        
        # 处理内部门级逻辑（仅在调试模式下显示）
        if hasattr(self, 'debug_mode') and self.debug_mode:
            # 创建wire节点
            for wire_name in self.module.wires:
                self.dot.node(wire_name, wire_name, shape='point')
                
            # 处理门级实例化
            for gate in getattr(self.module, 'gates', []):
                gate_id = f"${self.node_counter:02d}"
                self.node_counter += 1
                gate_node = f"{gate.gate_type}_{gate.name}"
                self.dot.node(gate_node, f"{{{gate_id}|{gate.gate_type}}}", shape='record')
                # 输入连到门
                for inp in gate.inputs:
                    self.dot.edge(inp, gate_node)
                # 门连到输出
                self.dot.edge(gate_node, gate.output)
            
        # 处理赋值语句
        for assign in getattr(self.module, 'assigns', []):
            # 递归处理整个表达式树，并连接最终结果到左侧
            result_node = self._process_expression(assign.right)
            # 将表达式的最终结果节点连接到赋值语句的左侧（输出端口）
            self.dot.edge(result_node, assign.left)
        
        return self.dot
        
    def _process_expression(self, expr):
        # 如果表达式是简单的标识符或数字
        if isinstance(expr, str) or isinstance(expr, int):
            if isinstance(expr, int):
                gate_id = f"${self.node_counter:02d}"
                self.node_counter += 1
                node_id = f"const_{expr}_{self.node_counter}"
                self.dot.node(node_id, f"{{{gate_id}|{str(expr)}}}", shape='record')
                return node_id
            return expr
        # 一元操作（如~）
        if isinstance(expr, dict) and expr.get('op') == '~':
            gate_id = f"${self.node_counter:02d}"
            self.node_counter += 1
            node_id = f"~_{self.node_counter}"
            self.dot.node(node_id, f"{{{gate_id}|NOT}}", shape='record')
            right_id = self._process_expression(expr['right'])
            self.dot.edge(right_id, node_id)
            return node_id
        # 二元操作
        if isinstance(expr, dict) and 'left' in expr and 'right' in expr:
            op = expr['op']
            gate_id = f"${self.node_counter:02d}"
            self.node_counter += 1
            # 转换操作符到门名称
            gate_name = op
            if op == '&': gate_name = 'AND'
            elif op == '|': gate_name = 'OR'
            elif op == '^': gate_name = 'XOR'
            elif op == '+': gate_name = 'ADD'
            elif op == '-': gate_name = 'SUB'

            # 修改节点标签，包含输入端口（例如：<in1> | <in2>）
            node_label = "{ {<in1>}|{<in2>} } | {{" + gate_id + "}|{" + gate_name + "}}"
            node_id = f"{op}_{self.node_counter}"
            self.dot.node(node_id, node_label, shape='record')

            # 递归处理子表达式并连接
            left_node = self._process_expression(expr['left'])
            right_node = self._process_expression(expr['right'])

            # 连接子表达式的输出到当前操作符的输入端口
            self.dot.edge(left_node, f"{node_id}:in1")
            self.dot.edge(right_node, f"{node_id}:in2")

            # 返回当前操作符节点的输出端口
            return node_id
        # 三元操作符 (condition ? if_true : if_false)
        if isinstance(expr, dict) and expr.get('op') == '?:':
            gate_id = f"${self.node_counter:02d}"
            self.node_counter += 1
            node_id = f"mux_{self.node_counter}"
            self.dot.node(node_id, f"{{{gate_id}|MUX}}", shape='record')

            condition_node = self._process_expression(expr['condition'])
            if_true_node = self._process_expression(expr['if_true'])
            if_false_node = self._process_expression(expr['if_false'])

            self.dot.edge(condition_node, node_id)
            # 需要为多路选择器节点定义输入端口
            # 暂时简化处理，直接连接到节点，后续考虑添加端口
            self.dot.edge(if_true_node, node_id)
            self.dot.edge(if_false_node, node_id)

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
    
    def set_debug_mode(self, debug=False):
        """设置是否显示内部门级逻辑的调试模式"""
        self.debug_mode = debug 