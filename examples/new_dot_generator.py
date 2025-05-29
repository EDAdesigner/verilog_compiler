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
                # 对于门的输入，我们也应该通过 _process_expression_node 来处理，以支持连接到复杂的表达式输出
                input_node_name = self._process_expression_node(inp)
                # 使用通用端口名 A, B, C... 来连接门的输入
                input_port_name = chr(ord('A') + gate.inputs.index(inp))
                self._create_edge(input_node_name, f"{gate_node}:{input_port_name}")

                port_parts.append(f"<{input_port_name}> {inp}")

            input_ports = "{" + "|".join(port_parts) + "}"
            output_port_name = "out" # 门的输出端口通常称为 'out'
            output_port_label = f"<{output_port_name}> {gate.output}"

            # 三段式横向结构（加最外层大括号，左中右）
            gate_label = f"{{{input_ports}|{{{gate_id}\\n{gate_type}}}|{output_port_label}}}"

            # 创建门节点
            self.dot.node(gate_node, gate_label, shape='record',
                         style='filled', fillcolor=self.node_colors['gate'])

            self.created_nodes.add(gate_node)
            self.node_types['gate'].append(gate_node)


            # 连接门输出到 wire 或 output
            # gate.output 是输出连接到的信号名称
            output_target_name = gate.output
            if output_target_name in self.module.wires or output_target_name in self.module.outputs:
                self._create_edge(f"{gate_node}:{output_port_name}", output_target_name)
            else:
                 # 如果输出目标不是 wire 或 output，可能是错误或内部信号，暂时忽略连接
                 print(f"警告: 门 '{gate.name}' 的输出目标 '{output_target_name}' 不是 wire 或 output. 无法创建连接.")

        # 处理赋值语句
        for assign in getattr(self.module, 'assigns', []):
            # 赋值语句的左侧是目标（wire 或 output）
            target_node_name = assign.left

            # 处理赋值语句的右侧表达式，生成相应的节点和连接
            # _process_expression_node 返回的是表达式最终节点的输出端口名称
            output_from_expr = self._process_expression_node(assign.right)

            # 将表达式的输出连接到赋值语句的左侧目标
            # 确保 target_node_name 是一个合法的目标（在 module.wires 或 module.outputs 中）
            if target_node_name in self.module.wires or target_node_name in self.module.outputs:
                 self._create_edge(output_from_expr, target_node_name)
            else:
                 # 如果左侧不是 wire 或 output，可能是错误或者优化后的中间信号，需要进一步分析
                 print(f"警告: 赋值语句左侧目标 '{target_node_name}' 不是 wire 或 output. 无法创建连接.")

            # 不再为赋值语句本身创建独立节点，连接已经代表了赋值关系

    def _create_edge(self, src, dst):
        """创建边，处理重复检测"""
        edge_key = f"{src}->{dst}"
        # 确保源和目标节点/端口存在，避免创建无效边
        # 这里可以添加更严格的检查，例如检查端口是否存在于节点的定义中
        if src and dst and edge_key not in self.created_edges:
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
    
    def _process_expression_node(self, expr):
        """
        递归处理表达式节点并创建相应的DOT节点。
        返回生成节点的输出名称。
        """
        if isinstance(expr, str):
            # 标识符或常量
            if expr in self.module.inputs or expr in self.module.wires:
                return expr # 直接返回输入或线的名称
            else:
                # 可能是常量或未声明的wire/输入，创建常量节点
                return self._get_or_create_constant_node(expr)
        elif isinstance(expr, dict):
            # 操作符节点
            op = expr['op']
            op_label = self._get_operation_type_label(op)

            # 为操作节点生成唯一ID
            node_id = f"op_{op_label}_{self.node_counter:02d}"
            self.node_counter += 1

            # 构建标签和端口
            input_ports = []
            input_node_names = {} # 存储输入表达式生成的节点名称

            # 处理左操作数
            if 'left' in expr:
                left_expr = expr['left']
                # 递归处理左操作数
                left_node_name = self._process_expression_node(left_expr)
                input_ports.append(f"<A> {'left'}") # 使用通用端口名A
                input_node_names['A'] = left_node_name

            # 处理右操作数
            if 'right' in expr:
                right_expr = expr['right']
                # 递归处理右操作数
                right_node_name = self._process_expression_node(right_expr)
                 # 根据是否有 'left' 来决定使用端口A还是B
                port_name = 'B' if 'left' in expr else 'A'
                input_ports.append(f"<{port_name}> {'right'}") # 使用通用端口名B或A
                input_node_names[port_name] = right_node_name

             # 处理三元操作符的其他输入
            if op == '?:':
                if 'condition' in expr:
                     cond_expr = expr['condition']
                     cond_node_name = self._process_expression_node(cond_expr)
                     input_ports.append(f"<S> {'cond'}")
                     input_node_names['S'] = cond_node_name
                if 'if_true' in expr:
                    true_expr = expr['if_true']
                    true_node_name = self._process_expression_node(true_expr)
                    # Check if 'left' exists to decide port A or B
                    port_name = 'A' if 'left' in expr else 'A' # MUX true input is A
                    input_ports.append(f"<{port_name}> {'true'}")
                    input_node_names[port_name] = true_node_name
                if 'if_false' in expr:
                    false_expr = expr['if_false']
                    false_node_name = self._process_expression_node(false_expr)
                     # Check if 'right' exists to decide port B or A (for second input)
                    port_name = 'B' if 'right' in expr or 'left' in expr else 'A' # MUX false input is B
                    input_ports.append(f"<{port_name}> {'false'}")
                    input_node_names[port_name] = false_node_name


            input_ports_label = "{" + "|".join(input_ports) + "}" if input_ports else "{}"
            # 输出端口使用固定的 'out'
            output_port_label = f"<out> {op_label}_out" # 使用操作符名作为输出端口标签的一部分

            # 三段式横向结构
            op_label_full = f"{{{input_ports_label}|{{{self.node_counter-1:02d}\\n{op_label}}}|{output_port_label}}}"

            # 创建操作符节点
            self.dot.node(node_id, op_label_full, shape='record',
                         style='filled', fillcolor=self.node_colors['gate'])

            self.created_nodes.add(node_id)
            self.node_types['gate'].append(node_id) # 将操作节点视为gate类型

            # 连接输入
            for port_name, node_name in input_node_names.items():
                 self._create_edge(node_name, f"{node_id}:{port_name}")

            # 返回操作节点的输出名称
            return f"{node_id}:out" # 返回带端口的节点名称

        else:
            # 未知表达式类型
            print(f"警告: 未知的表达式类型 {type(expr)}")
            return "unknown_node" # 返回一个默认名称
    
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
        """设置是否显示内部细节"""
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