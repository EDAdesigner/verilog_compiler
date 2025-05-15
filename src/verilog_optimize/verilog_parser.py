import ply.yacc as yacc
from verilog_lexer import get_lexer, VerilogLexer
import sys
import io

class VerilogModule:
    def __init__(self, name):
        self.name = name
        self.inputs = []
        self.outputs = []
        self.wires = []
        self.gates = []
        self.assigns = []
        self.expressions = {}  # 用于存储表达式及其对应的wire
        
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
        self.type = 'assign'  # 添加类型标识

class VerilogParser:
    def __init__(self):
        self.lexer = get_lexer()
        self.tokens = VerilogLexer.tokens
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        self.parser = yacc.yacc(module=self)
        sys.stdout = old_stdout
        self.module = None
        self.temp_wire_count = 0
        
    # 语法规则
    def p_module_definition(self, p):
        '''module_definition : MODULE ID LPAREN port_list RPAREN SEMICOLON declarations statements ENDMODULE'''
        p[0] = self.module
        
    def p_port_list(self, p):
        '''port_list : port_item
                    | port_item COMMA port_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_port_item(self, p):
        '''port_item : ID'''
        p[0] = p[1]
        
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
        '''input_declaration : INPUT port_list SEMICOLON'''
        for port in p[2]:
            self.module.inputs.append(port)
            
    def p_output_declaration(self, p):
        '''output_declaration : OUTPUT port_list SEMICOLON'''
        for port in p[2]:
            self.module.outputs.append(port)
            
    def p_wire_declaration(self, p):
        '''wire_declaration : WIRE port_list SEMICOLON'''
        for port in p[2]:
            self.module.wires.append(port)
            
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
            
    def _get_expression_key(self, expr):
        """生成表达式的唯一标识符"""
        if isinstance(expr, dict):
            if expr['type'] == 'add':
                left_key = self._get_expression_key(expr['left'])
                right_key = self._get_expression_key(expr['right'])
                return f"({left_key}+{right_key})"
            elif expr['type'] == 'and':
                left_key = self._get_expression_key(expr['left'])
                right_key = self._get_expression_key(expr['right'])
                return f"({left_key}&{right_key})"
        return str(expr)

    def _process_expression(self, expr):
        """处理表达式，返回对应的wire名称"""
        if isinstance(expr, dict):
            expr_key = self._get_expression_key(expr)
            if expr_key in self.module.expressions:
                # 如果表达式已经存在，直接返回对应的wire
                return self.module.expressions[expr_key]
            else:
                # 如果是新表达式，创建新的wire
                if expr['type'] == 'add':
                    left_wire = self._process_expression(expr['left'])
                    right_wire = self._process_expression(expr['right'])
                    result_wire = expr.get('result', f'temp_wire_{self.temp_wire_count}')
                    self.temp_wire_count += 1
                    if result_wire not in self.module.wires:
                        self.module.wires.append(result_wire)
                    # 创建新的赋值语句
                    new_expr = {'type': 'add', 'left': left_wire, 'right': right_wire}
                    self.module.assigns.append(Assignment(result_wire, new_expr))
                    self.module.expressions[expr_key] = result_wire
                    return result_wire
                elif expr['type'] == 'and':
                    left_wire = self._process_expression(expr['left'])
                    right_wire = self._process_expression(expr['right'])
                    result_wire = f'temp_wire_{self.temp_wire_count}'
                    self.temp_wire_count += 1
                    self.module.wires.append(result_wire)
                    new_expr = {'type': 'and', 'left': left_wire, 'right': right_wire}
                    self.module.assigns.append(Assignment(result_wire, new_expr))
                    self.module.expressions[expr_key] = result_wire
                    return result_wire
        return expr

    def p_assign_statement(self, p):
        '''assign_statement : ASSIGN ID EQUALS expression SEMICOLON'''
        left = p[2]
        right = p[4]
        # 处理表达式，获取最终的wire名称
        result_wire = self._process_expression(right)
        # 判断是否为输出端口，且右侧为中间wire，直接连线不生成BUF
        if left in self.module.outputs and isinstance(result_wire, str) and result_wire.startswith('temp_wire_'):
            self.module.assigns.append(Assignment(left, result_wire))
        elif isinstance(right, dict):
            self.module.assigns.append(Assignment(left, result_wire))
        else:
            self.module.assigns.append(Assignment(left, right))
        
    def _balance_add_chain(self, add_list):
        """递归将加法链分组为平衡二叉树结构，返回表达式树结构，不生成wire和assign"""
        if len(add_list) == 1:
            return add_list[0]
        mid = len(add_list) // 2
        left = self._balance_add_chain(add_list[:mid])
        right = self._balance_add_chain(add_list[mid:])
        return {'type': 'add', 'left': left, 'right': right}

    def p_expression(self, p):
        '''expression : term
                     | expression PLUS term
                     | expression AMPERSAND term'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            if p[2] == '+':
                # 收集加法链
                def flatten_add(expr):
                    # 递归展开所有加法项，兼容不同结构
                    if isinstance(expr, dict) and (expr.get('type') == 'add' or expr.get('op') == '+'):
                        return flatten_add(expr['left']) + flatten_add(expr['right'])
                    else:
                        return [expr]
                left_terms = flatten_add(p[1])
                right_terms = flatten_add(p[3])
                all_terms = left_terms + right_terms
                # 树高平衡
                p[0] = self._balance_add_chain(all_terms)
            elif p[2] == '&':
                p[0] = {'type': 'and', 'left': p[1], 'right': p[3]}
            
    def p_term(self, p):
        '''term : ID
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