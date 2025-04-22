from graphviz import Digraph
import os

class DotGenerator:
    def __init__(self, module):
        self.module = module
        self.dot = Digraph(comment=module.name)
        self.dot.attr(rankdir='LR')
        self.node_counter = 0
        self.processed_nodes = set()

    def generate_dot(self):
        # 创建输入节点
        for input_name in self.module.inputs:
            self.dot.node(input_name, input_name, shape='triangle', color='blue')
            
        # 创建输出节点
        for output_name in self.module.outputs:
            self.dot.node(output_name, output_name, shape='triangle', color='red')
            
        # 创建wire节点
        for wire_name in self.module.wires:
            if not wire_name.startswith('temp_wire_'):
                self.dot.node(wire_name, wire_name, shape='point')

        # 处理赋值语句
        for assign in self.module.assigns:
            if isinstance(assign.right, dict):
                if assign.right['type'] == 'add':
                    # 处理加法
                    add_node = f"add_{self.node_counter}"
                    self.node_counter += 1
                    self.dot.node(add_node, "+", shape='box')
                    
                    # 连接输入到加法节点
                    left_id = self._process_operand(assign.right['left'])
                    right_id = self._process_operand(assign.right['right'])
                    self.dot.edge(left_id, add_node)
                    self.dot.edge(right_id, add_node)
                    
                    # 连接加法节点到输出
                    self.dot.edge(add_node, assign.left)
                elif assign.right['type'] == 'and':
                    # 处理与运算
                    and_node = f"and_{self.node_counter}"
                    self.node_counter += 1
                    self.dot.node(and_node, "&", shape='box')
                    
                    # 连接输入到与运算节点
                    left_id = self._process_operand(assign.right['left'])
                    right_id = self._process_operand(assign.right['right'])
                    self.dot.edge(left_id, and_node)
                    self.dot.edge(right_id, and_node)
                    
                    # 连接与运算节点到输出
                    self.dot.edge(and_node, assign.left)
            else:
                # 处理简单赋值
                self.dot.edge(str(assign.right), assign.left)

        return self.dot

    def _process_operand(self, operand):
        if isinstance(operand, dict):
            if operand['type'] == 'add':
                add_node = f"add_{self.node_counter}"
                self.node_counter += 1
                self.dot.node(add_node, "+", shape='box')
                
                left_id = self._process_operand(operand['left'])
                right_id = self._process_operand(operand['right'])
                self.dot.edge(left_id, add_node)
                self.dot.edge(right_id, add_node)
                
                return operand['result']
            elif operand['type'] == 'and':
                and_node = f"and_{self.node_counter}"
                self.node_counter += 1
                self.dot.node(and_node, "&", shape='box')
                
                left_id = self._process_operand(operand['left'])
                right_id = self._process_operand(operand['right'])
                self.dot.edge(left_id, and_node)
                self.dot.edge(right_id, and_node)
                
                return and_node
        return str(operand)

    def save(self, output_path=None):
        if output_path is None:
            output_path = self.module.name
            
        base_path = os.path.splitext(output_path)[0]
        
        # 保存DOT文件
        dot_file = f"{base_path}.dot"
        self.dot.save(dot_file)
        
        # 渲染并保存图片
        png_file = f"{base_path}.png"
        self.dot.render(base_path, format='png', cleanup=True)
        
        return dot_file, png_file 