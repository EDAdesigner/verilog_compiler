import ply.lex as lex

class VerilogLexer:
    # 保留字
    reserved = {
        'module': 'MODULE',
        'endmodule': 'ENDMODULE',
        'input': 'INPUT',
        'output': 'OUTPUT',
        'wire': 'WIRE',
        'assign': 'ASSIGN',
        'and': 'AND',
        'or': 'OR',
        'not': 'NOT',
        'nand': 'NAND',
        'nor': 'NOR',
        'xor': 'XOR',
        'xnor': 'XNOR',
        'buf': 'BUF'
    }

    # 所有的token名称
    tokens = [
        'ID',          # 标识符
        'NUMBER',      # 数字
        'PLUS',       # +
        'MINUS',      # -
        'AMPERSAND',  # &
        'EQUALS',     # =
        'LPAREN',     # (
        'RPAREN',     # )
        'SEMICOLON',  # ;
        'COMMA',      # ,
        'TILDE',
        'OR_OP',      # |
        'XOR_OP'      # ^
    ] + list(reserved.values())

    # 简单的token规则
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_AMPERSAND = r'&'
    t_EQUALS = r'='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_SEMICOLON = r';'
    t_COMMA = r','
    t_TILDE = r'~'
    t_OR_OP = r'\|'
    t_XOR_OP = r'\^'

    # 标识符规则
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    # 数字规则
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # 忽略空白字符
    t_ignore = ' \t'

    # 新行
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # 错误处理
    def t_error(self, t):
        print(f"非法字符 '{t.value[0]}'")
        t.lexer.skip(1)

    def __init__(self):
        self.lexer = None

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()

def get_lexer():
    lexer = VerilogLexer()
    lexer.build()
    return lexer.lexer 