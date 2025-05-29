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
            else: # 'unknown' 或 'wire'
                self.wires.append(name)

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
        original_ports = p[4]

        # 在解析完所有 module_items 后，根据 ports 字典填充 inputs, outputs, wires 列表
        self.module.finalize_ports()

        p[0] = self.module
        
    def p_port_list(self, p):
        '''port_list : port_list_items'''
        p[0] = p[1] # port_list 的值就是 port_list_items 返回的列表
        
    def p_port_list_items(self, p):
        '''port_list_items : port_item
                         | port_list_items COMMA port_item'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + p[3]
        
    def p_port_item(self, p):
        '''port_item : ID
                     | WIRE ID'''
        if len(p) == 2:
            # 记录端口名，类型暂时未知
            self.module.ports[p[1]] = 'unknown'
            p[0] = [p[1]]
        else: # WIRE ID
            # 记录端口名，类型暂时未知
            self.module.ports[p[2]] = 'unknown'
            p[0] = [p[2]] # 忽略 WIRE 关键字，只返回 ID

    def p_module_items(self, p):
        '''module_items : module_item
                       | module_items module_item
                       | empty'''
        pass
        
    def p_module_item(self, p):
        '''module_item : input_declaration
                      | output_declaration
                      | wire_declaration
                      | assign_statement
                      | gate_instantiation'''
        pass
        
    def p_input_declaration(self, p):
        '''input_declaration : INPUT input_list SEMICOLON
                           | INPUT WIRE input_list SEMICOLON'''
        # input_list 的规则已经处理了端口类型的更新，这里只需 pass
        pass

    def p_input_list(self, p):
        '''input_list : ID
                     | input_list COMMA ID'''
        if len(p) == 2:
            # 记录输入端口名，并更新类型
            self.module.ports[p[1]] = 'input'
            p[0] = [p[1]]
        else:
            # 记录输入端口名，并更新类型
            self.module.ports[p[3]] = 'input'
            p[0] = p[1] + [p[3]]
            
    def p_output_declaration(self, p):
        '''output_declaration : OUTPUT output_list SEMICOLON
                              | OUTPUT WIRE output_list SEMICOLON'''
        # output_list 的规则已经处理了端口类型的更新，这里只需 pass
        pass

    def p_output_list(self, p):
        '''output_list : ID
                      | output_list COMMA ID'''
        if len(p) == 2:
            # 记录输出端口名，并更新类型
            self.module.ports[p[1]] = 'output'
            p[0] = [p[1]]
        else:
            # 记录输出端口名，并更新类型
            self.module.ports[p[3]] = 'output'
            p[0] = p[1] + [p[3]]
            
    def p_wire_declaration(self, p):
        '''wire_declaration : WIRE wire_list SEMICOLON'''
        pass
        
    def p_wire_list(self, p):
        '''wire_list : ID
                    | wire_list COMMA ID'''
        if len(p) == 2:
            self.module.wires.append(p[1])
        else:
            self.module.wires.append(p[3])
            
    def p_assign_statement(self, p):
        '''assign_statement : ASSIGN ID EQUALS expression SEMICOLON'''
        self.module.assigns.append(Assignment(p[2], p[4]))
        
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
                p[0] = {'op': 'AND', 'left': p[1], 'right': p[3]}
            elif p[2] == '|':
                p[0] = {'op': 'OR', 'left': p[1], 'right': p[3]}
            elif p[2] == '^':
                p[0] = {'op': 'XOR', 'left': p[1], 'right': p[3]}
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
            p[0] = {'op': 'NOT', 'right': p[2]}
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
        result = self.parser.parse(data, lexer=self.lexer)
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