import ply.yacc as yacc
from verilog_lexer import get_lexer, VerilogLexer
import os
import sys
import io

class VerilogModule:
    def __init__(self, name):
        self.name = name
        self.ports = {} # 存储端口名和类型 {'port_name': 'type'}
        self.inputs = []
        self.outputs = []
        self.wires = []
        self.gates = []
        self.assigns = []
        
    def finalize_ports(self):
        """根据 ports 字典填充 inputs, outputs, wires 列表"""
        self.inputs = []
        self.outputs = []
        self.wires = []
        for name, type in self.ports.items():
            if type == 'input':
                self.inputs.append(name)
            elif type == 'output':
                self.outputs.append(name)
            elif type == 'wire':
                self.wires.append(name)
            else: # 'unknown'
                # 如果在端口列表中出现但没有input/output/wire声明，默认为wire
                if name not in self.wires:
                     self.wires.append(name)
                     
    def print_info(self):
        """在终端打印模块的详细信息"""
        print("\n" + "="*50)
        print(f"模块名称: {self.name}")
        print("="*50)
        
        print("\n输入端口:")
        for i, input_name in enumerate(self.inputs):
            print(f"  [{i+1}] {input_name}")
            
        print("\n输出端口:")
        for i, output_name in enumerate(self.outputs):
            print(f"  [{i+1}] {output_name}")
            
        print("\n内部连线:")
        for i, wire_name in enumerate(self.wires):
            print(f"  [{i+1}] {wire_name}")
        
        if self.gates:
            print("\n门级元件:")
            for i, gate in enumerate(self.gates):
                inputs_str = ", ".join(gate.inputs)
                print(f"  [{i+1}] {gate.gate_type} {gate.name}: 输入=({inputs_str}), 输出={gate.output}")
        
        if self.assigns:
            print("\n赋值语句:")
            for i, assign in enumerate(self.assigns):
                print(f"  [{i+1}] {assign.left} = ", end="")
                self._print_expression(assign.right)
                print()
        
        print("="*50 + "\n")
    
    def _print_expression(self, expr, level=0):
        """递归打印表达式"""
        indent = "  " * level
        
        # 如果表达式是简单的标识符或数字
        if isinstance(expr, str) or isinstance(expr, int):
            print(f"{expr}", end="")
            return
            
        # 一元操作（如~）
        if isinstance(expr, dict) and (expr.get('op') == 'NOT' or expr.get('op') == '~'):
            print("~(", end="")
            self._print_expression(expr['right'], level+1)
            print(")", end="")
            return
            
        # 二元操作
        if isinstance(expr, dict) and 'left' in expr and 'right' in expr:
            op = expr['op']
            # 使用原始操作符符号
            op_symbol = op
            
            print("(", end="")
            self._print_expression(expr['left'], level+1)
            print(f" {op_symbol} ", end="")
            self._print_expression(expr['right'], level+1)
            print(")", end="")
            return
            
        # 三元操作符
        if isinstance(expr, dict) and expr.get('op') == '?:':
            print("(", end="")
            self._print_expression(expr['condition'], level+1)
            print(" ? ", end="")
            self._print_expression(expr['if_true'], level+1)
            print(" : ", end="")
            self._print_expression(expr['if_false'], level+1)
            print(")", end="")
            return
            
        # 其他情况
        print(f"{expr}", end="")

class Gate:
    def __init__(self, gate_type, name, inputs, output):
        self.gate_type = gate_type
        self.name = name
        self.inputs = inputs
        self.output = output
        
class Assignment:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class VerilogParser:
    def __init__(self):
        self.lexer = get_lexer()
        self.tokens = VerilogLexer.tokens
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        self.parser = yacc.yacc(module=self)
        sys.stdout = old_stdout
        self.module = None
        
    # 语法规则
    def p_module_definition(self, p):
        '''module_definition : MODULE ID LPAREN port_list RPAREN SEMICOLON module_items ENDMODULE'''
        self.module.name = p[2]
        # 获取原始端口列表 (p[4] 现在只包含名称列表)
        # original_ports = p[4] # 这一行不需要了，p[4]是port_list_items的结果，我们已经直接更新到self.module.ports

        # 在解析完所有 module_items 后，根据 ports 字典填充 inputs, outputs, wires 列表
        self.module.finalize_ports()

        p[0] = self.module
        
    def p_port_list(self, p):
        '''port_list : port_list_items'''
        # port_list_items 的动作已经更新了 self.module.ports，这里只需 pass
        pass
        
    def p_port_list_items(self, p):
        '''port_list_items : port_item
                         | port_list_items COMMA port_item'''
        # port_item 的动作已经更新了 self.module.ports，这里只需 pass
        pass
        
    def p_port_item(self, p):
        '''port_item : ID
                     | WIRE ID'''
        if len(p) == 2:
            # 记录端口名，类型暂时未知 (如果在端口列表出现但无声明，默认为 wire)
            if p[1] not in self.module.ports:
                self.module.ports[p[1]] = 'unknown' # 或者更明确一点，初始可以设置为 wire

        else: # WIRE ID - wire 声明应该在 module_items 中处理，这里是端口列表，不应该有 WIRE 关键字
             # 记录端口名，类型暂时未知
             if p[2] not in self.module.ports:
                 self.module.ports[p[2]] = 'unknown' # Initial type can be wire or unknown

        # p[0] = [p[1]] 或 [p[2]] - 这里不需要返回列表，信息已记录到 self.module.ports
        pass

    def p_module_items(self, p):
        '''module_items : module_item
                       | module_items module_item
                       | empty'''
        # 不需要返回值，所有信息都存储在module对象中
        pass
        
    def p_module_item(self, p):
        '''module_item : input_declaration
                      | output_declaration
                      | wire_declaration
                      | assign_statement
                      | gate_instantiation'''
        # 不需要返回值，所有信息都存储在module对象中
        pass
        
    def p_input_declaration(self, p):
        '''input_declaration : INPUT input_list SEMICOLON
                           | INPUT WIRE input_list SEMICOLON'''
        # input_list 的规则已经处理了端口类型的更新
        pass

    def p_input_list(self, p):
        '''input_list : ID
                     | input_list COMMA ID'''
        if len(p) == 2:
            # 记录输入端口名，并更新类型
            self.module.ports[p[1]] = 'input'
        else:
            # 记录输入端口名，并更新类型
            self.module.ports[p[3]] = 'input'
        pass
            
    def p_output_declaration(self, p):
        '''output_declaration : OUTPUT output_list SEMICOLON
                              | OUTPUT WIRE output_list SEMICOLON'''
        # output_list 的规则已经处理了端口类型的更新
        pass

    def p_output_list(self, p):
        '''output_list : ID
                      | output_list COMMA ID'''
        if len(p) == 2:
            # 记录输出端口名，并更新类型
            self.module.ports[p[1]] = 'output'
        else:
            # 记录输出端口名，并更新类型
            self.module.ports[p[3]] = 'output'
        pass
            
    def p_wire_declaration(self, p):
        '''wire_declaration : WIRE wire_list SEMICOLON'''
        # 确保wire_list中的所有标识符都被正确添加到wires列表中
        pass

    def p_wire_list(self, p):
        '''wire_list : ID
                    | wire_list COMMA ID'''
        if len(p) == 2:
            # 如果是单个ID
            wire_name = p[1]
            if wire_name not in self.module.wires:
                self.module.wires.append(wire_name)
                # 更新ports字典中的类型
                self.module.ports[wire_name] = 'wire'
        else:
            # 如果是wire_list COMMA ID
            wire_name = p[3]
            if wire_name not in self.module.wires:
                self.module.wires.append(wire_name)
                # 更新ports字典中的类型
                self.module.ports[wire_name] = 'wire'
        pass

    def p_assign_statement(self, p):
        '''assign_statement : ASSIGN ID EQUALS expression SEMICOLON'''
        left = p[2]
        # 检查左侧是否是已声明的wire或output
        if left not in self.module.wires and left not in self.module.outputs:
            # 如果左侧不是已声明的wire或output，自动将其添加为wire
            self.module.wires.append(left)
            self.module.ports[left] = 'wire'
        self.module.assigns.append(Assignment(left, p[4]))
        
    def p_expression(self, p):
        '''expression : term
                     | expression PLUS term
                     | expression MINUS term
                     | expression AMPERSAND term
                     | expression BAR term
                     | expression CARET term
                     | term QUESTION expression COLON expression'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            if p[2] == '+':
                p[0] = {'op': '+', 'left': p[1], 'right': p[3]}
            elif p[2] == '-':
                p[0] = {'op': '-', 'left': p[1], 'right': p[3]}
            elif p[2] == '&':
                p[0] = {'op': '&', 'left': p[1], 'right': p[3]}
            elif p[2] == '|':
                p[0] = {'op': '|', 'left': p[1], 'right': p[3]}
            elif p[2] == '^':
                p[0] = {'op': '^', 'left': p[1], 'right': p[3]}
        elif len(p) == 6:  # 三元操作符: condition ? if_true : if_false
            p[0] = {'op': '?:', 'condition': p[1], 'if_true': p[3], 'if_false': p[5]}
            
    def p_term(self, p):
        '''term : ID
               | NUMBER
               | LPAREN expression RPAREN
               | TILDE term'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3 and p[1] == '~':
            p[0] = {'op': '~', 'right': p[2]}
        else:
            p[0] = p[2]
            
    def p_empty(self, p):
        '''empty :'''
        pass
        
    def p_gate_instantiation(self, p):
        '''gate_instantiation : gate_type ID LPAREN signal_list RPAREN SEMICOLON'''
        gate_type = p[1]
        gate_name = p[2]
        signals = p[4]
        output = signals[-1]
        inputs = signals[:-1]
        self.module.gates.append(Gate(gate_type, gate_name, inputs, output))

    def p_gate_type(self, p):
        '''gate_type : AND
                    | OR
                    | NOT
                    | NAND
                    | NOR
                    | XOR
                    | XNOR
                    | BUF'''
        p[0] = p[1]

    def p_signal_list(self, p):
        '''signal_list : ID
                      | signal_list COMMA ID'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
        
    def p_error(self, p):
        if p:
            print(f"语法错误: '{p.value}'，第 {p.lineno} 行")
        else:
            print("语法错误: 意外的文件结束")
            
    def parse(self, data, module_name=None):
        self.module = VerilogModule(module_name or "default_module")
        # 在解析之前清空 ports 字典
        self.module.ports = {}
        result = self.parser.parse(data, lexer=self.lexer)
        # finalize_ports 现在在 p_module_definition 中调用
        return self.module

def process_verilog(input_file, optimize=True):
    """处理Verilog文件的主函数"""
    try:
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            verilog_code = f.read()
    except Exception as e:
        print(f"错误: 无法读取文件 '{input_file}': {e}")
        return False

    # 解析阶段
    print("1. 开始解析Verilog代码...")
    parser = VerilogParser()
    module = parser.parse(verilog_code)
    
    if module is None:
        print("解析失败，请检查Verilog代码语法")
        return False
    
    print("   解析完成")
    
    # 在终端显示解析后的模块信息
    print("\n正在显示解析后的模块信息...")
    module.print_info()

    # 优化阶段
    if optimize:
        try:
            print("2. 开始进行共享子表达式优化...")
            optimizer = CSEOptimizer()
            module = optimizer.optimize_module(module)
            print("   优化完成")
        except Exception as e:
            print(f"优化过程中出错: {e}")
            return False

    # 生成图形
    try:
        print("3. 开始生成图形...")
        dot_generator = DotGenerator(module)
        dot = dot_generator.generate_dot()
        
        output_base = os.path.splitext(input_file)[0]
        if optimize:
            output_base += "_optimized"
            
        dot_file, png_file = dot_generator.save(output_base)
        
        print(f"   成功生成 DOT 文件: {dot_file}")
        print(f"   成功生成图像文件: {png_file}")
        
    except Exception as e:
        print(f"生成图形时出错: {e}")
        return False

    return True