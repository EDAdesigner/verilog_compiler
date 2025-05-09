from graphviz import Digraph
import os
import re

class EnhancedDotGenerator:
    """增强型DOT图形生成器，生成标准易读的电路图"""
    
    def __init__(self, module):
        """
        初始化DOT图形生成器
        
        参数:
            module: Verilog模块对象
        """
        self.module = module
        self.dot = Digraph(name=module.name, engine='dot', format='png')
        
        # 图形基本属性设置
        self.dot.attr('graph', 
                      rankdir='LR',                # 从左到右的布局
                      splines='polyline',          # 使用折线连接，避免直线重叠的同时确保清晰结构
                      nodesep='0.5',               # 节点间距
                      ranksep='0.8',               # 层级间距
                      concentrate='false',         # 不合并边线
                      ordering='out',              # 输出排序
                      dpi='300')                   # 高分辨率

        # 节点属性 - 使用record类型以支持端口
        self.dot.attr('node', 
                      shape='record',              # 支持端口的记录类型
                      style='filled',              # 填充样式
                      fillcolor='white',           # 默认填充色
                      fontname='Arial',            # 字体
                      fontsize='12',               # 字体大小
                      height='0.4',                # 节点高度
                      width='0.6',                 # 节点宽度
                      margin='0.1',                # 边距
                      penwidth='1.0')              # 边框宽度

        # 边属性 - 确保箭头明确指向边框而不是进入内部
        self.dot.attr('edge', 
                      arrowsize='0.6',             # 箭头大小
                      penwidth='1.0',              # 线条宽度
                      arrowhead='normal',          # 箭头样式
                      fontname='Arial',            # 字体
                      fontsize='10')               # 字体大小
        
        # 节点计数器
        self.node_counter = 0
        
        # 当前使用的样式
        self.style = 'default'
        
        # 是否显示内部细节
        self.show_internal = True
        
        # 跟踪已创建的节点和边，避免重复
        self.created_nodes = set()
        self.created_edges = set()
        
        # 常量节点映射
        self.constant_map = {}
        
        # 记录节点的类型分类
        self.node_types = {
            'input': [],
            'output': [],
            'wire': [],
            'gate': [],
            'assign': [],
            'constant': []
        }
        
        # 存储节点的连接点信息
        self.node_ports = {}
        
        # 节点颜色配置
        self.node_colors = {
            'input': 'lightblue',
            'output': 'lightgreen',
            'wire': 'lightyellow',
            'gate': 'lightpink',
            'assign': 'lavender',
            'constant': 'lightgrey'
        }
    
    def set_style(self, style):
        """设置电路图样式"""
        valid_styles = ['default', 'mux', 'adder', 'decoder', 'register']
        if style in valid_styles:
            self.style = style
        else:
            print(f"警告: 未知样式 '{style}'，使用默认样式")
            self.style = 'default'
    
    def generate_dot(self):
        """生成DOT图形"""
        # 创建输入端口节点
        for input_name in self.module.inputs:
            self.dot.node(input_name, input_name, shape='ellipse', 
                         style='filled', fillcolor=self.node_colors['input'])
            self.node_types['input'].append(input_name)
            # 注册输入端口
            self.node_ports[input_name] = {'out': input_name}
        
        # 创建输出端口节点
        for output_name in self.module.outputs:
            self.dot.node(output_name, output_name, shape='ellipse', 
                         style='filled', fillcolor=self.node_colors['output'])
            self.node_types['output'].append(output_name)
            # 注册输出端口
            self.node_ports[output_name] = {'in': output_name}
        
        # 创建wire节点
        for wire_name in self.module.wires:
            node_id = f"${self.node_counter:02d}"
            self.node_counter += 1
            
            self.dot.node(wire_name, wire_name, 
                         shape='box', style='filled', 
                         fillcolor=self.node_colors['wire'])
            
            self.created_nodes.add(wire_name)
            self.node_types['wire'].append(wire_name)
            # 注册wire端口
            self.node_ports[wire_name] = {'in': wire_name, 'out': wire_name}
        
        # 添加门和赋值逻辑
        self._add_gates_and_assignments()
        
        # 创建子图，改善布局
        self._create_subgraphs()
            
        return self.dot
    
    def _add_gates_and_assignments(self):
        """添加门和赋值语句节点及连接"""
        # 处理门实例
        for gate in getattr(self.module, 'gates', []):
            gate_node = f"{gate.gate_type}_{gate.name}"
            if gate_node in self.created_nodes:
                continue
            
            # 创建门标签和端口
            gate_type = self._get_gate_type_label(gate.gate_type)
            gate_id = f"${self.node_counter:02d}"
            self.node_counter += 1
            
            # 构建标签，包含输入和输出端口
            port_parts = []
            for inp in gate.inputs:
                port_parts.append(f"<{inp}> {inp}")
            input_ports = "{" + "|".join(port_parts) + "}"
            output_port = f"<{gate.output}> {gate.output}"
            # 三段式横向结构（加最外层大括号，左中右）
            gate_label = f"{{{input_ports}|{{{gate_id}\\n{gate_type}}}|{output_port}}}"
            
            # 创建门节点
            self.dot.node(gate_node, gate_label, shape='record', 
                         style='filled', fillcolor=self.node_colors['gate'])
            
            self.created_nodes.add(gate_node)
            self.node_types['gate'].append(gate_node)
            
            # 连接输入到门
            for inp in gate.inputs:
                if inp in self.module.inputs:
                    self._create_edge(inp, f"{gate_node}:{inp}")
                elif inp in self.module.wires:
                    self._create_edge(inp, f"{gate_node}:{inp}")
                else:
                    # 处理常量
                    const_node = self._get_or_create_constant_node(inp)
                    self._create_edge(const_node, f"{gate_node}:{inp}")
            
            # 连接门输出
            if gate.output in self.module.wires:
                self._create_edge(f"{gate_node}:{gate.output}", gate.output)
            elif gate.output in self.module.outputs:
                self._create_edge(f"{gate_node}:{gate.output}", gate.output)
        
        # 处理赋值语句
        for assign in getattr(self.module, 'assigns', []):
            assign_node = f"assign_{assign.left}"
            if assign_node in self.created_nodes:
                continue
            
            assign_id = f"${self.node_counter:02d}"
            self.node_counter += 1
            
            # 根据表达式类型创建不同的节点
            if isinstance(assign.right, dict) and 'op' in assign.right:
                op = assign.right['op']
                
                if op == '?:':  # 三元操作符
                    self._create_mux_node(assign_node, assign_id, assign.right, assign.left)
                else:  # 二元操作符
                    self._create_op_node(assign_node, assign_id, assign.right, assign.left)
            else:  # 简单赋值
                self._create_buf_node(assign_node, assign_id, assign.right, assign.left)
                
            self.created_nodes.add(assign_node)
            self.node_types['assign'].append(assign_node)
    
    def _create_edge(self, src, dst):
        """创建边，处理重复检测"""
        edge_key = f"{src}->{dst}"
        if edge_key not in self.created_edges:
            # 添加边，箭头连接到边框，但不指定端口方向
            self.dot.edge(src, dst)
            self.created_edges.add(edge_key)
    
    def _get_or_create_constant_node(self, value):
        """获取或创建常量节点"""
        if value in self.constant_map:
            return self.constant_map[value]
        
        const_node = f"const_{value}"
        self.dot.node(const_node, str(value), shape='plaintext', 
                     style='filled', fillcolor=self.node_colors['constant'])
        
        self.created_nodes.add(const_node)
        self.constant_map[value] = const_node
        self.node_types['constant'].append(const_node)
        
        return const_node
    
    def _create_mux_node(self, node_id, sym_id, expr, output_name):
        """创建多路选择器节点（三元操作符）"""
        # 创建端口
        if_true_port = f"<A> {expr['if_true']}" if isinstance(expr['if_true'], str) else "<A> if true"
        if_false_port = f"<B> {expr['if_false']}" if isinstance(expr['if_false'], str) else "<B> if false"
        cond_port = f"<S> {expr['condition']}" if isinstance(expr['condition'], str) else "<S> select"
        output_port = f"<{output_name}> {output_name}"
        
        # 创建标签
        label = f"{{{{{if_true_port}|{if_false_port}|{cond_port}}}|{{{sym_id}\\nMUX}}|{output_port}}}"
        
        # 创建节点
        self.dot.node(node_id, label, shape='record', 
                     style='filled', fillcolor=self.node_colors['assign'])
        
        # 处理条件输入
        if isinstance(expr['condition'], str):
            if expr['condition'] in self.module.inputs or expr['condition'] in self.module.wires:
                self._create_edge(expr['condition'], f"{node_id}:S")
            else:
                cond_node = self._get_or_create_constant_node(expr['condition'])
                self._create_edge(cond_node, f"{node_id}:S")
        
        # 处理真值输入
        if isinstance(expr['if_true'], str):
            if expr['if_true'] in self.module.inputs or expr['if_true'] in self.module.wires:
                self._create_edge(expr['if_true'], f"{node_id}:A")
            else:
                true_node = self._get_or_create_constant_node(expr['if_true'])
                self._create_edge(true_node, f"{node_id}:A")
        
        # 处理假值输入
        if isinstance(expr['if_false'], str):
            if expr['if_false'] in self.module.inputs or expr['if_false'] in self.module.wires:
                self._create_edge(expr['if_false'], f"{node_id}:B")
            else:
                false_node = self._get_or_create_constant_node(expr['if_false'])
                self._create_edge(false_node, f"{node_id}:B")
        
        # 处理输出连接
        if output_name in self.module.wires or output_name in self.module.outputs:
            self._create_edge(f"{node_id}:{output_name}", output_name)
    
    def _create_op_node(self, node_id, sym_id, expr, output_name):
        """创建操作符节点（二元操作符）"""
        op_label = self._get_operation_type_label(expr['op'])
        
        # 创建端口
        left_port = f"<A> {expr['left']}" if isinstance(expr['left'], str) else "<A> A"
        right_port = f"<B> {expr['right']}" if isinstance(expr['right'], str) else "<B> B"
        output_port = f"<{output_name}> {output_name}"
        
        # 创建标签
        label = f"{{{{{left_port}|{right_port}}}|{{{sym_id}\\n{op_label}}}|{output_port}}}"
        
        # 创建节点
        self.dot.node(node_id, label, shape='record', 
                     style='filled', fillcolor=self.node_colors['assign'])
        
        # 处理左操作数
        if isinstance(expr['left'], str):
            if expr['left'] in self.module.inputs or expr['left'] in self.module.wires:
                self._create_edge(expr['left'], f"{node_id}:A")
            else:
                left_node = self._get_or_create_constant_node(expr['left'])
                self._create_edge(left_node, f"{node_id}:A")
        
        # 处理右操作数
        if isinstance(expr['right'], str):
            if expr['right'] in self.module.inputs or expr['right'] in self.module.wires:
                self._create_edge(expr['right'], f"{node_id}:B")
            else:
                right_node = self._get_or_create_constant_node(expr['right'])
                self._create_edge(right_node, f"{node_id}:B")
        
        # 处理输出连接
        if output_name in self.module.wires or output_name in self.module.outputs:
            self._create_edge(f"{node_id}:{output_name}", output_name)
    
    def _create_buf_node(self, node_id, sym_id, input_value, output_name):
        """创建BUF节点（简单赋值）"""
        # 创建端口
        input_port = f"<A> {input_value}" if isinstance(input_value, str) else "<A> in"
        output_port = f"<{output_name}> {output_name}"
        
        # 创建标签
        label = f"{{{input_port}|{{{sym_id}\\nBUF}}|{output_port}}}"
        
        # 创建节点
        self.dot.node(node_id, label, shape='record', 
                     style='filled', fillcolor=self.node_colors['assign'])
        
        # 处理输入
        if isinstance(input_value, str):
            if input_value in self.module.inputs or input_value in self.module.wires:
                self._create_edge(input_value, f"{node_id}:A")
            else:
                in_node = self._get_or_create_constant_node(input_value)
                self._create_edge(in_node, f"{node_id}:A")
        
        # 处理输出连接
        if output_name in self.module.wires or output_name in self.module.outputs:
            self._create_edge(f"{node_id}:{output_name}", output_name)
    
    def _is_input_used_in_expression(self, input_name, expression):
        """检查输入在表达式中是否被使用"""
        if isinstance(expression, str):
            return expression == input_name
        elif isinstance(expression, dict):
            result = False
            if 'left' in expression and 'right' in expression:
                result = result or self._is_input_used_in_expression(input_name, expression['left'])
                result = result or self._is_input_used_in_expression(input_name, expression['right'])
            elif 'right' in expression:  # 一元操作符
                result = result or self._is_input_used_in_expression(input_name, expression['right'])
            elif 'condition' in expression:  # 三元操作符
                result = result or self._is_input_used_in_expression(input_name, expression['condition'])
                result = result or self._is_input_used_in_expression(input_name, expression['if_true'])
                result = result or self._is_input_used_in_expression(input_name, expression['if_false'])
            return result
        return False
    
    def _create_subgraphs(self):
        """创建改善布局的子图"""
        # 输入子图
        if self.node_types['input']:
            with self.dot.subgraph(name='cluster_inputs') as s:
                s.attr(rank='source', style='filled', color='lightblue', label='Inputs')
                for node in self.node_types['input']:
                    s.node(node)
        
        # 输出子图
        if self.node_types['output']:
            with self.dot.subgraph(name='cluster_outputs') as s:
                s.attr(rank='sink', style='filled', color='lightgreen', label='Outputs')
                for node in self.node_types['output']:
                    s.node(node)
        
        # 常量子图
        if self.node_types['constant']:
            with self.dot.subgraph(name='cluster_constants') as s:
                s.attr(rank='min', style='filled', color='lightgrey', label='Constants')
                for node in self.node_types['constant']:
                    s.node(node)
    
    def _get_gate_type_label(self, gate_type):
        """获取门类型的标准标签"""
        gate_labels = {
            'and': 'AND',
            'or': 'OR',
            'xor': 'XOR',
            'not': 'NOT',
            'nand': 'NAND',
            'nor': 'NOR',
            'xnor': 'XNOR',
            'buf': 'BUF'
        }
        return gate_labels.get(gate_type.lower(), gate_type.upper())
    
    def _get_operation_type_label(self, op):
        """获取操作符类型的标准标签"""
        op_labels = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIV',
            '&': 'AND',
            '|': 'OR',
            '^': 'XOR',
            '~': 'NOT',
            '?:': 'MUX'
        }
        return op_labels.get(op, op.upper())
    
    def set_show_internal(self, show):
        """设置是否显示内部电路细节"""
        self.show_internal = show
    
    def save(self, output_path=None):
        """保存DOT图形为图形文件"""
        if output_path is None:
            output_path = f"{self.module.name}"
        
        # 移除文件扩展名（如果有）
        base_path = os.path.splitext(output_path)[0]
        
        # 确保输出目录存在
        output_dir = os.path.dirname(base_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 保存DOT文件
        dot_file = f"{base_path}.dot"
        self.dot.save(dot_file)
        
        # 渲染并保存图片
        png_file = f"{base_path}.png"
        self.dot.render(base_path, format='png', cleanup=True)
        
        return dot_file, png_file 