"""
模块库 - 包含常用数字电路模块的定义
"""

class ModuleLibrary:
    @staticmethod
    def create_multiplexer(module_id, select_size=1):
        """
        创建一个多路选择器(multiplexer)的DOT表示
        
        参数:
            module_id: 模块ID编号
            select_size: 选择信号的位数
        
        返回:
            module_def: 模块定义字典
        """
        # 计算输入端口数量 (2^select_size) + select_size
        data_inputs = 2 ** select_size
        
        # 构建模块定义
        module_def = {
            'id': module_id,  # 模块ID，形如 $26
            'type': 'Spmux',  # 模块类型
            'ports': {
                'inputs': [],  # 输入端口列表
                'selects': [], # 选择信号列表
                'outputs': ['Y']  # 输出端口列表
            }
        }
        
        # 添加数据输入端口
        port_names = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in range(min(data_inputs, len(port_names))):
            module_def['ports']['inputs'].append(port_names[i])
        
        # 添加选择信号
        for i in range(select_size):
            module_def['ports']['selects'].append(f"S{i}")
        
        return module_def

    @staticmethod
    def create_decoder(module_id, input_size=2):
        """
        创建一个解码器(decoder)的DOT表示
        
        参数:
            module_id: 模块ID编号
            input_size: 输入信号的位数
        
        返回:
            module_def: 模块定义字典
        """
        # 计算输出端口数量 (2^input_size)
        outputs = 2 ** input_size
        
        # 构建模块定义
        module_def = {
            'id': module_id,  # 模块ID，形如 $26
            'type': 'Decoder',  # 模块类型
            'ports': {
                'inputs': [],  # 输入端口列表
                'outputs': []  # 输出端口列表
            }
        }
        
        # 添加输入端口
        for i in range(input_size):
            module_def['ports']['inputs'].append(f"I{i}")
        
        # 添加输出端口
        for i in range(outputs):
            module_def['ports']['outputs'].append(f"Y{i}")
        
        return module_def

    @staticmethod
    def create_register(module_id, size=8):
        """
        创建一个寄存器(register)的DOT表示
        
        参数:
            module_id: 模块ID编号
            size: 寄存器位数
        
        返回:
            module_def: 模块定义字典
        """
        # 构建模块定义
        module_def = {
            'id': module_id,  # 模块ID，形如 $26
            'type': 'Register',  # 模块类型
            'ports': {
                'inputs': [],    # 数据输入端口列表
                'clock': 'CLK',  # 时钟信号
                'reset': 'RST',  # 复位信号
                'load': 'LD',    # 加载信号
                'outputs': []    # 数据输出端口列表
            }
        }
        
        # 添加数据输入端口
        for i in range(size):
            module_def['ports']['inputs'].append(f"D{i}")
        
        # 添加数据输出端口
        for i in range(size):
            module_def['ports']['outputs'].append(f"Q{i}")
        
        return module_def 