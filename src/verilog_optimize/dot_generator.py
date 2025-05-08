from graphviz import Digraph
import os

class DotGenerator:
    def __init__(self, module):
        self.module = module
        self.dot = Digraph(comment=module.name)
        self.dot.attr(rankdir='LR')
        self.node_counter = 0
        self.processed_nodes = set()
        self.created_nodes = set()

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
                if assign.right.get('type') == 'add' or assign.right.get('op') == '+':
                    # 处理加法
                    add_node = f"add_{self.node_counter}"
                    self.node_counter += 1
                    self.dot.node(add_node, "+", shape='box')
                    
                    # 连接输入到加法节点
                    left_id = assign.right.get('left')
                    right_id = assign.right.get('right')
                    
                    # 确保节点存在
                    if left_id and isinstance(left_id, str) and left_id.startswith('temp_wire_') and left_id not in self.created_nodes:
                        self.dot.node(left_id, "", shape='point')
                        self.created_nodes.add(left_id)
                    if right_id and isinstance(right_id, str) and right_id.startswith('temp_wire_') and right_id not in self.created_nodes:
                        self.dot.node(right_id, "", shape='point')
                        self.created_nodes.add(right_id)
                        
                    self.dot.edge(str(left_id), add_node)
                    self.dot.edge(str(right_id), add_node)
                    
                    # 连接加法节点到输出
                    self.dot.edge(add_node, assign.left)
                    
                elif assign.right.get('type') == 'and' or assign.right.get('op') == '&':
                    # 处理与运算
                    and_node = f"and_{self.node_counter}"
                    self.node_counter += 1
                    self.dot.node(and_node, "&", shape='box')
                    
                    # 连接输入到与运算节点
                    left_id = assign.right.get('left')
                    right_id = assign.right.get('right')
                    
                    # 确保节点存在
                    if left_id and isinstance(left_id, str) and left_id.startswith('temp_wire_') and left_id not in self.created_nodes:
                        self.dot.node(left_id, "", shape='point')
                        self.created_nodes.add(left_id)
                    if right_id and isinstance(right_id, str) and right_id.startswith('temp_wire_') and right_id not in self.created_nodes:
                        self.dot.node(right_id, "", shape='point')
                        self.created_nodes.add(right_id)
                        
                    self.dot.edge(str(left_id), and_node)
                    self.dot.edge(str(right_id), and_node)
                    
                    # 连接与运算节点到输出
                    self.dot.edge(and_node, assign.left)
            else:
                # 处理简单赋值
                source = str(assign.right)
                target = assign.left
                if source.startswith('temp_wire_') and source not in self.created_nodes:
                    self.dot.node(source, "", shape='point')
                    self.created_nodes.add(source)
                self.dot.edge(source, target)

        return self.dot

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