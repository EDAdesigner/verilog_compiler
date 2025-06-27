import ply.yacc as yacc
from .verilog_lexer import get_lexer, VerilogLexer
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
        
    def print_info(self):
        print("\n==================================================")
        print(f"模块名称: {self.name}")
        print("==================================================\n")
        print("输入端口:")
        for idx, port in enumerate(self.inputs, 1):
            print(f"  [{idx}] {port}")
        print("\n输出端口:")
        for idx, port in enumerate(self.outputs, 1):
            print(f"  [{idx}] {port}")
        print("\n内部连线:")
        for idx, wire in enumerate(self.wires, 1):
            print(f"  [{idx}] {wire}")
        print("\n赋值语句:")
        for idx, assign in enumerate(self.assigns, 1):
            left = assign.left
            right = assign.right
            print(f"  [{idx}] {left} = {self._expr_to_str(right)}")
        print("==================================================\n")

    def _expr_to_str(self, expr):
        if isinstance(expr, dict):
            op = expr.get('op')
            if op in ['+', '-', '&', '|', '^']:
                return f"({self._expr_to_str(expr['left'])} {op} {self._expr_to_str(expr['right'])})"
            elif op == '~':
                return f"~({self._expr_to_str(expr['right'])})"
            elif op == '?:':
                return f"({self._expr_to_str(expr['condition'])} ? {self._expr_to_str(expr['if_true'])} : {self._expr_to_str(expr['if_false'])})"
            else:
                return str(expr)
        else:
            return str(expr)

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
        '''declarations : declarations declaration
                       | declaration
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
        '''statements : statements statement
                     | statement
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
            
    def _process_expression(self, expr):
        """处理表达式，返回对应的wire名称"""
        if not isinstance(expr, dict):
            # 如果是变量名或常量，直接返回
            return expr
        expr_key = self._get_expression_key(expr)
        if expr_key in self.module.expressions:
            return self.module.expressions[expr_key]
        # Use 'op' key consistently
        op = expr.get('op')
        if op == '+':
            left_wire = self._process_expression(expr['left'])
            right_wire = self._process_expression(expr['right'])
            result_wire = expr.get('result', f'temp_wire_{self.temp_wire_count}')
            self.temp_wire_count += 1
            if result_wire not in self.module.wires:
                self.module.wires.append(result_wire)
            new_expr = {'op': '+', 'left': left_wire, 'right': right_wire}
            self.module.assigns.append(Assignment(result_wire, new_expr))
            self.module.expressions[expr_key] = result_wire
            return result_wire
        elif op == '&':
            left_wire = self._process_expression(expr['left'])
            right_wire = self._process_expression(expr['right'])
            result_wire = f'temp_wire_{self.temp_wire_count}'
            self.temp_wire_count += 1
            self.module.wires.append(result_wire)
            new_expr = {'op': '&', 'left': left_wire, 'right': right_wire}
            self.module.assigns.append(Assignment(result_wire, new_expr))
            self.module.expressions[expr_key] = result_wire
            return result_wire
        elif op == '|':
            left_wire = self._process_expression(expr['left'])
            right_wire = self._process_expression(expr['right'])
            result_wire = f'temp_wire_{self.temp_wire_count}'
            self.temp_wire_count += 1
            self.module.wires.append(result_wire)
            new_expr = {'op': '|', 'left': left_wire, 'right': right_wire}
            self.module.assigns.append(Assignment(result_wire, new_expr))
            self.module.expressions[expr_key] = result_wire
            return result_wire
        elif op == '^':
            left_wire = self._process_expression(expr['left'])
            right_wire = self._process_expression(expr['right'])
            result_wire = f'temp_wire_{self.temp_wire_count}'
            self.temp_wire_count += 1
            self.module.wires.append(result_wire)
            new_expr = {'op': '^', 'left': left_wire, 'right': right_wire}
            self.module.assigns.append(Assignment(result_wire, new_expr))
            self.module.expressions[expr_key] = result_wire
            return result_wire
        elif op == '~':
            right_wire = self._process_expression(expr['right'])
            result_wire = f'temp_wire_{self.temp_wire_count}'
            self.temp_wire_count += 1
            self.module.wires.append(result_wire)
            new_expr = {'op': '~', 'right': right_wire}
            self.module.assigns.append(Assignment(result_wire, new_expr))
            self.module.expressions[expr_key] = result_wire
            return result_wire
        elif op == '?:':
            cond_wire = self._process_expression(expr['condition'])
            true_wire = self._process_expression(expr['if_true'])
            false_wire = self._process_expression(expr['if_false'])
            result_wire = f'temp_wire_{self.temp_wire_count}'
            self.temp_wire_count += 1
            self.module.wires.append(result_wire)
            new_expr = {'op': '?:', 'condition': cond_wire, 'if_true': true_wire, 'if_false': false_wire}
            self.module.assigns.append(Assignment(result_wire, new_expr))
            self.module.expressions[expr_key] = result_wire
            return result_wire
        else:
            print(f"Warning: Unhandled expression type in _process_expression: {expr}")
            return expr

    def _get_expression_key(self, expr):
        """生成表达式的唯一标识符"""
        if not isinstance(expr, dict):
            return str(expr)
        # Use 'op' key consistently
        if expr.get('op') == '+':
            left_key = self._get_expression_key(expr['left'])
            right_key = self._get_expression_key(expr['right'])
            return f"({left_key}+{right_key})"
        elif expr.get('op') == '&':
            left_key = self._get_expression_key(expr['left'])
            right_key = self._get_expression_key(expr['right'])
            return f"({left_key}&{right_key})"
        elif expr.get('op') == '|':
            left_key = self._get_expression_key(expr['left'])
            right_key = self._get_expression_key(expr['right'])
            return f"({left_key}|{right_key})"
        elif expr.get('op') == '^':
            left_key = self._get_expression_key(expr['left'])
            right_key = self._get_expression_key(expr['right'])
            return f"({left_key}^{right_key})"
        elif expr.get('op') == '~':
            right_key = self._get_expression_key(expr['right'])
            return f"(~{right_key})"
        elif expr.get('op') == '?:':
            cond_key = self._get_expression_key(expr['condition'])
            true_key = self._get_expression_key(expr['if_true'])
            false_key = self._get_expression_key(expr['if_false'])
            return f"({cond_key}?{true_key}:{false_key})"
        # Handle other simple operations if needed
        elif 'op' in expr:
            operands = []
            if 'left' in expr:
                operands.append(self._get_expression_key(expr['left']))
            if 'right' in expr:
                operands.append(self._get_expression_key(expr['right']))
            return f"({' '.join(operands)}{expr['op']})"
        return str(expr)

    def p_assign_statement(self, p):
        '''assign_statement : ASSIGN ID EQUALS expression SEMICOLON'''
        left = p[2]
        right = p[4]
        # 处理表达式，获取最终的wire名称
        result_wire = self._process_expression(right)
        # assign 右侧始终为 wire 名称
        self.module.assigns.append(Assignment(left, result_wire))

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
                     | expression AMPERSAND term
                     | expression OR_OP term
                     | expression XOR_OP term
                     | TILDE term''' # Add rule for unary NOT
        if len(p) == 2:
            p[0] = p[1]
        else:
            # Use 'op' key consistently
            if p[1] == '~': # Check if the first token is TILDE
                p[0] = {'op': '~', 'right': p[2]} # Create expression for unary NOT
            elif p[2] == '+':
                # 收集加法链
                def flatten_add(expr):
                    # Recursively flatten all addition terms, accommodating different structures
                    if isinstance(expr, dict) and (expr.get('type') == 'add' or expr.get('op') == '+'): # Check for both 'type' and 'op' during flattening for compatibility
                        return flatten_add(expr.get('left')) + flatten_add(expr.get('right'))
                    else:
                        return [expr]
                left_terms = flatten_add(p[1])
                right_terms = flatten_add(p[3])
                all_terms = left_terms + right_terms
                # 树高平衡
                # Create the expression structure using 'op'
                p[0] = self._balance_add_chain_with_op(all_terms)
            elif p[2] == '&':
                p[0] = {'op': '&', 'left': p[1], 'right': p[3]}
            elif p[2] == '|': # Handle OR_OP
                p[0] = {'op': '|', 'left': p[1], 'right': p[3]}
            elif p[2] == '^': # Handle XOR_OP
                p[0] = {'op': '^', 'left': p[1], 'right': p[3]}

    # Helper function to balance add chain and use 'op' key
    def _balance_add_chain_with_op(self, add_list):
        """递归将加法链分组为平衡二叉树结构，返回使用'op'键的表达式树结构"""
        if len(add_list) == 1:
            return add_list[0]
        mid = len(add_list) // 2
        left = self._balance_add_chain_with_op(add_list[:mid])
        right = self._balance_add_chain_with_op(add_list[mid:])
        return {'op': '+', 'left': left, 'right': right}

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

        # --- Add Dead Code Removal Logic Here ---
        self._remove_dead_code() # Call the new method
        # --- End Dead Code Removal Logic ---

        return self.module

    def _add_inputs_to_live_signals(self, expression, live_signals_set):
        """递归地将表达式中的输入信号添加到活跃信号集合"""
        if isinstance(expression, str):
            # If it's a simple signal name and not already processed
            live_signals_set.add(expression)
        elif isinstance(expression, dict):
            # Recursively process sub-expressions
            if 'left' in expression:
                self._add_inputs_to_live_signals(expression['left'], live_signals_set)
            if 'right' in expression:
                self._add_inputs_to_live_signals(expression['right'], live_signals_set)
            if 'condition' in expression:
                 self._add_inputs_to_live_signals(expression['condition'], live_signals_set)
            if 'if_true' in expression:
                 self._add_inputs_to_live_signals(expression['if_true'], live_signals_set)
            if 'if_false' in expression:
                 self._add_inputs_to_live_signals(expression['if_false'], live_signals_set)

    def _remove_dead_code(self):
        """移除模块中的死代码"""
        live_signals = set(self.module.outputs) # Start with outputs
        live_assigns = []
        live_gates = []

        # Keep track of changes to iterate until stable
        changed = True
        while changed:
            changed = False
            newly_live_signals = set()

            # Check assignments
            for assign in self.module.assigns:
                # Check if the assignment's output is a live signal
                if assign.left in live_signals and assign not in live_assigns:
                    live_assigns.append(assign)
                    changed = True
                    # Add inputs of this assignment's expression to newly live signals
                    self._add_inputs_to_live_signals(assign.right, newly_live_signals)

            # Check gates
            for gate in self.module.gates:
                 # Check if the gate's output is a live signal
                 if gate.output in live_signals and gate not in live_gates:
                     live_gates.append(gate)
                     changed = True
                     # Add inputs of this gate to newly live signals
                     for inp in gate.inputs:
                         newly_live_signals.add(inp)

            # Add newly found live signals to the main set
            for signal in newly_live_signals:
                if signal not in live_signals:
                    live_signals.add(signal)
                    changed = True # Continue iterating if new signals are added

        # Filter wires, gates, and assigns based on live signals/objects
        self.module.wires = [wire for wire in self.module.wires if wire in live_signals]
        self.module.gates = live_gates
        self.module.assigns = live_assigns

        # Remove expressions related to dead wires (optional, but good for cleanup)
        # This part might be tricky depending on how expressions are structured and used
        # For now, we'll keep it simple and just filter wires/assigns/gates

        # Also filter inputs that are not part of any live logic
        # This requires checking if input signals are in the final 'live_signals' set
        self.module.inputs = [inp for inp in self.module.inputs if inp in live_signals or inp in self.module.outputs] # Outputs are always live 