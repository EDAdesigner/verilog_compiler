import ply.yacc as yacc
from verilog_lexer import get_lexer, VerilogLexer

class VerilogModule:
    def __init__(self, name):
        self.name = name
        self.inputs = []
        self.outputs = []
        self.wires = []
        self.gates = []
        self.assigns = []
        
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
        self.parser = yacc.yacc(module=self)
        self.module = None
        
    # 语法规则
    def p_module_definition(self, p):
        '''module_definition : MODULE ID LPAREN port_list RPAREN SEMICOLON declarations statements ENDMODULE'''
        p[0] = self.module
        
    def p_port_list(self, p):
        '''port_list : ID
                    | ID COMMA port_list'''
        # 只保存端口名，具体的输入/输出类型会在声明中处理
        pass
        
    def p_declarations(self, p):
        '''declarations : declaration
                       | declaration declarations
                       | empty'''
        pass
        
    def p_declaration(self, p):
        '''declaration : input_declaration
                      | output_declaration
                      | wire_declaration'''
        pass
        
    def p_input_declaration(self, p):
        '''input_declaration : INPUT ID SEMICOLON
                           | INPUT LBRACKET NUMBER COLON NUMBER RBRACKET ID SEMICOLON'''
        if len(p) == 4:
            self.module.inputs.append(p[2])
        else:
            # 处理总线
            width = p[3] - p[5] + 1
            self.module.inputs.append(f"{p[7]}[{p[5]}:{p[3]}]")
            
    def p_output_declaration(self, p):
        '''output_declaration : OUTPUT ID SEMICOLON
                             | OUTPUT LBRACKET NUMBER COLON NUMBER RBRACKET ID SEMICOLON'''
        if len(p) == 4:
            self.module.outputs.append(p[2])
        else:
            # 处理总线
            width = p[3] - p[5] + 1
            self.module.outputs.append(f"{p[7]}[{p[5]}:{p[3]}]")
            
    def p_wire_declaration(self, p):
        '''wire_declaration : WIRE ID SEMICOLON
                          | WIRE LBRACKET NUMBER COLON NUMBER RBRACKET ID SEMICOLON'''
        if len(p) == 4:
            self.module.wires.append(p[2])
        else:
            # 处理总线
            width = p[3] - p[5] + 1
            self.module.wires.append(f"{p[7]}[{p[5]}:{p[3]}]")
            
    def p_statements(self, p):
        '''statements : statement
                     | statement statements
                     | empty'''
        pass
        
    def p_statement(self, p):
        '''statement : gate_instantiation
                    | assign_statement'''
        pass
        
    def p_gate_instantiation(self, p):
        '''gate_instantiation : gate_type ID LPAREN signal_list RPAREN SEMICOLON'''
        gate_type = p[1]
        gate_name = p[2]
        signals = p[4]
        
        # 最后一个信号是输出
        output = signals[-1]
        inputs = signals[:-1]
        
        gate = Gate(gate_type, gate_name, inputs, output)
        self.module.gates.append(gate)
        
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
                      | ID COMMA signal_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]
            
    def p_assign_statement(self, p):
        '''assign_statement : ASSIGN ID EQUALS expression SEMICOLON
                          | ASSIGN ID LBRACKET NUMBER RBRACKET EQUALS expression SEMICOLON'''
        if len(p) == 6:
            left = p[2]
        else:
            left = f"{p[2]}[{p[4]}]"
            
        right = p[len(p)-2]
        
        assign = Assignment(left, right)
        self.module.assigns.append(assign)
        
    def p_expression(self, p):
        '''expression : term
                     | term PLUS expression
                     | term MINUS expression
                     | term AMPERSAND expression
                     | term BAR expression
                     | term CARET expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = {'op': p[2], 'left': p[1], 'right': p[3]}
            
    def p_term(self, p):
        '''term : factor
                | factor TIMES term
                | factor DIVIDE term'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = {'op': p[2], 'left': p[1], 'right': p[3]}
            
    def p_factor(self, p):
        '''factor : primary
                 | TILDE primary
                 | MINUS primary'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = {'op': p[1], 'operand': p[2]}
            
    def p_primary(self, p):
        '''primary : ID
                  | NUMBER
                  | LPAREN expression RPAREN'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]
            
    def p_empty(self, p):
        'empty :'
        pass
        
    def p_error(self, p):
        if p:
            print(f"语法错误: '{p.value}'，第 {p.lineno} 行")
        else:
            print("语法错误: 意外的文件结束")
            
    def parse(self, data, module_name=None):
        # 创建一个新的模块对象
        self.module = VerilogModule(module_name or "default_module")
        
        # 解析
        self.parser.parse(data, lexer=self.lexer)
        return self.module 