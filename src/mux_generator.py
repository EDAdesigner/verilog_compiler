from graphviz import Digraph
import os
from module_library import ModuleLibrary

class MuxGenerator:
    """用于生成多路选择器(Multiplexer)电路图的生成器"""
    
    def __init__(self, module_name="multiplexer"):
        """
        初始化多路选择器生成器
        
        参数:
            module_name: 模块名称
        """
        self.module_name = module_name
        self.dot = Digraph(name=module_name)
        self.dot.attr('graph', rankdir='LR', splines='ortho', nodesep='0.5')
        self.dot.attr('node', fontname='Arial', height='0.6', width='1.2')
        self.dot.attr('edge', arrowsize='0.7')
        
    def generate_2to1_mux(self, module_id="$26"):
        """
        生成2选1多路选择器的电路图
        
        参数:
            module_id: 模块ID
        """
        # 获取多路选择器定义
        mux_def = ModuleLibrary.create_multiplexer(module_id, select_size=1)
        
        # 创建输入端口组
        input_ports = []
        for port in mux_def['ports']['inputs']:
            input_ports.append(f"<{port}> {port}")
        
        # 添加选择信号端口
        for port in mux_def['ports']['selects']:
            input_ports.append(f"<{port}> {port}")
            
        # 创建输入端口组节点
        if input_ports:
            self.dot.node('inputs', '|'.join(input_ports), shape='record')
        
        # 创建输出端口组
        output_ports = []
        for port in mux_def['ports']['outputs']:
            output_ports.append(f"<{port}> {port}")
            
        # 创建输出端口组节点
        if output_ports:
            self.dot.node('outputs', '|'.join(output_ports), shape='record')
        
        # 创建多路选择器模块
        module_label = f"{{{mux_def['id']}|{mux_def['type']}}}"
        self.dot.node('module', module_label, shape='record', style='filled', fillcolor='lightgray')
        
        # 连接输入端口到模块
        for port in mux_def['ports']['inputs']:
            self.dot.edge(f"inputs:{port}", 'module')
            
        # 连接选择信号到模块
        for port in mux_def['ports']['selects']:
            self.dot.edge(f"inputs:{port}", 'module')
        
        # 连接模块到输出端口
        for port in mux_def['ports']['outputs']:
            self.dot.edge('module', f"outputs:{port}")
            
        return self.dot
    
    def generate_4to1_mux(self, module_id="$26"):
        """
        生成4选1多路选择器的电路图
        
        参数:
            module_id: 模块ID
        """
        # 获取多路选择器定义
        mux_def = ModuleLibrary.create_multiplexer(module_id, select_size=2)
        
        # 创建输入端口组
        input_ports = []
        for port in mux_def['ports']['inputs']:
            input_ports.append(f"<{port}> {port}")
        
        # 添加选择信号端口
        for port in mux_def['ports']['selects']:
            input_ports.append(f"<{port}> {port}")
            
        # 创建输入端口组节点
        if input_ports:
            self.dot.node('inputs', '|'.join(input_ports), shape='record')
        
        # 创建输出端口组
        output_ports = []
        for port in mux_def['ports']['outputs']:
            output_ports.append(f"<{port}> {port}")
            
        # 创建输出端口组节点
        if output_ports:
            self.dot.node('outputs', '|'.join(output_ports), shape='record')
        
        # 创建多路选择器模块
        module_label = f"{{{mux_def['id']}|{mux_def['type']}}}"
        self.dot.node('module', module_label, shape='record', style='filled', fillcolor='lightgray')
        
        # 连接输入端口到模块
        for port in mux_def['ports']['inputs']:
            self.dot.edge(f"inputs:{port}", 'module')
            
        # 连接选择信号到模块
        for port in mux_def['ports']['selects']:
            self.dot.edge(f"inputs:{port}", 'module')
        
        # 连接模块到输出端口
        for port in mux_def['ports']['outputs']:
            self.dot.edge('module', f"outputs:{port}")
            
        return self.dot
        
    def save(self, output_path=None):
        """保存DOT文件和图形图片"""
        if output_path is None:
            output_path = f"{self.module_name}"
            
        # 移除文件扩展名（如果有）
        base_path = os.path.splitext(output_path)[0]
        
        # 保存DOT文件
        dot_file = f"{base_path}.dot"
        self.dot.save(dot_file)
        
        # 渲染并保存图片
        png_file = f"{base_path}.png"
        self.dot.render(base_path, format='png', cleanup=True)
        
        return dot_file, png_file 