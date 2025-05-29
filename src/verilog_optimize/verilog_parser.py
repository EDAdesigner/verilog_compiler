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
            
    def _get_expression_key(self, expr):
        """生成表达式的唯一标识符"""
        if isinstance(expr, dict):
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
            elif expr.get('op') == '?:': # Handle ternary operator
                 cond_key = self._get_expression_key(expr['condition'])
                 true_key = self._get_expression_key(expr['if_true'])
                 false_key = self._get_expression_key(expr['if_false'])
                 return f"({cond_key}?{true_key}:{false_key})"
            # Handle other simple operations if needed
            elif 'op' in expr: # Generic handling for other ops
                operands = []
                if 'left' in expr:
                    operands.append(self._get_expression_key(expr['left']))
                if 'right' in expr:
                    operands.append(self._get_expression_key(expr['right']))
                return f"({' '.join(operands)}{expr['op']})" # Simple representation

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
                # Use 'op' key consistently
                op = expr.get('op')
                if op == '+':
                    left_wire = self._process_expression(expr['left'])
                    right_wire = self._process_expression(expr['right'])
                    result_wire = expr.get('result', f'temp_wire_{self.temp_wire_count}')
                    self.temp_wire_count += 1
                    if result_wire not in self.module.wires:
                        self.module.wires.append(result_wire)
                    # 创建新的赋值语句，使用 'op'
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
                    # 创建新的赋值语句，使用 'op'
                    new_expr = {'op': '&', 'left': left_wire, 'right': right_wire}
                    self.module.assigns.append(Assignment(result_wire, new_expr))
                    self.module.expressions[expr_key] = result_wire
                    return result_wire
                elif op == '|': # Handle OR_OP
                    left_wire = self._process_expression(expr['left'])
                    right_wire = self._process_expression(expr['right'])
                    result_wire = f'temp_wire_{self.temp_wire_count}'
                    self.temp_wire_count += 1
                    self.module.wires.append(result_wire)
                    # 创建新的赋值语句，使用 'op'
                    new_expr = {'op': '|', 'left': left_wire, 'right': right_wire}
                    self.module.assigns.append(Assignment(result_wire, new_expr))
                    self.module.expressions[expr_key] = result_wire
                    return result_wire
                elif op == '^': # Handle XOR_OP
                    left_wire = self._process_expression(expr['left'])
                    right_wire = self._process_expression(expr['right'])
                    result_wire = f'temp_wire_{self.temp_wire_count}'
                    self.temp_wire_count += 1
                    self.module.wires.append(result_wire)
                    # 创建新的赋值语句，使用 'op'
                    new_expr = {'op': '^', 'left': left_wire, 'right': right_wire}
                    self.module.assigns.append(Assignment(result_wire, new_expr))
                    self.module.expressions[expr_key] = result_wire
                    return result_wire
                elif op == '~': # Handle unary NOT
                    right_wire = self._process_expression(expr['right'])
                    result_wire = f'temp_wire_{self.temp_wire_count}'
                    self.temp_wire_count += 1
                    self.module.wires.append(result_wire)
                    # 创建新的赋值语句，使用 'op'
                    new_expr = {'op': '~', 'right': right_wire}
                    self.module.assigns.append(Assignment(result_wire, new_expr))
                    self.module.expressions[expr_key] = result_wire
                    return result_wire
                # Add handling for other operation types if needed
                elif op == '?:': # Handle ternary operator
                     cond_wire = self._process_expression(expr['condition'])
                     true_wire = self._process_expression(expr['if_true'])
                     false_wire = self._process_expression(expr['if_false'])
                     result_wire = f'temp_wire_{self.temp_wire_count}'
                     self.temp_wire_count += 1
                     self.module.wires.append(result_wire)
                     # 创建新的赋值语句，使用 'op'
                     new_expr = {'op': '?:', 'condition': cond_wire, 'if_true': true_wire, 'if_false': false_wire}
                     self.module.assigns.append(Assignment(result_wire, new_expr))
                     self.module.expressions[expr_key] = result_wire
                     return result_wire
                else:
                    # Fallback for unhandled dictionary structures
                    print(f"Warning: Unhandled expression type in _process_expression: {expr}")
                    return expr # Return original expression if unhandled

        return expr # Return original expression if not a dictionary

    def p_assign_statement(self, p):
        '''assign_statement : ASSIGN ID EQUALS expression SEMICOLON'''
        left = p[2]
        right = p[4]
        # 处理表达式，获取最终的wire名称
        result_wire = self._process_expression(right)
        # 判断是否为输出端口，且右侧为中间wire，直接连线不生成BUF
        if left in self.module.outputs and isinstance(result_wire, str) and result_wire.startswith('temp_wire_'):
            # When directly assigning to output from a temp_wire, check if the temp_wire is from a complex expression
            # If result_wire corresponds to an expression, assign the expression structure, otherwise just the wire name
            expr_structure = None
            for expr_key, wire_name in self.module.expressions.items():
                 if wire_name == result_wire:
                      # Found the expression key for this temp_wire. Need to reconstruct the expression structure.
                      # This is a simplified approach. A more robust parser would link wires back to their generating expressions.
                      # For now, we'll just check if the expression_key looks like a complex operation.
                      # A better approach would involve storing the expression structure with the temp_wire.
                      if any(op in expr_key for op in ['+', '&', '|', '^', '~', '?:']):
                           # Try to find the original expression dict from the assigns list
                           original_assign = next((a for a in self.module.assigns if isinstance(a.left, str) and a.left == result_wire), None)
                           if original_assign and isinstance(original_assign.right, dict):
                                expr_structure = original_assign.right
                                break # Found it

            if expr_structure:
                # Append the assignment with the expression structure if it came from a complex op
                self.module.assigns.append(Assignment(left, expr_structure))
            else:
                # Otherwise, append the simple wire assignment
                self.module.assigns.append(Assignment(left, result_wire))

        elif isinstance(right, dict):
            # If the right side was an expression dictionary from p_expression, use result_wire
            # result_wire already points to the temp_wire created for this expression by _process_expression
             self.module.assigns.append(Assignment(left, result_wire))
        else:
            # Simple assignment (e.g., assign w1 = a;)
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