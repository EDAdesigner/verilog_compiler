import ply.lex as lex

# 词法分析器

class VerilogLexer:
    # 保留字
    reserved = {
        'module': 'MODULE',
        'endmodule': 'ENDMODULE',
        'input': 'INPUT',
        'output': 'OUTPUT',
        'wire': 'WIRE',
        'reg': 'REG',
        'and': 'AND',
        'or': 'OR',
        'not': 'NOT',
        'nand': 'NAND',
        'nor': 'NOR',
        'xor': 'XOR',
        'xnor': 'XNOR',
        'buf': 'BUF',
        'assign': 'ASSIGN',
    }

    # 所有令牌名称列表
    tokens = [
        'ID',
        'NUMBER',
        'LPAREN',
        'RPAREN',
        'LBRACKET',
        'RBRACKET',
        'LBRACE',
        'RBRACE',
        'SEMICOLON',
        'COLON',
        'COMMA',
        'DOT',
        'EQUALS',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'TILDE',
        'AMPERSAND',
        'BAR',
        'CARET',
        'QUESTION',
    ] + list(reserved.values())

    # 正则表达式规则
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_SEMICOLON = r';'
    t_COLON = r':'
    t_COMMA = r','
    t_DOT = r'\.'
    t_EQUALS = r'='
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_TILDE = r'~'
    t_AMPERSAND = r'&'
    t_BAR = r'\|'
    t_CARET = r'\^'
    t_QUESTION = r'\?'

    # 忽略这些字符
    t_ignore = ' \t'

    # 忽略注释
    t_ignore_COMMENT = r'//.*'

    # 标识符和关键字
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    # 数字
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # 新行
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # 处理错误
    def t_error(self, t):
        print(f"非法字符 '{t.value[0]}'")
        t.lexer.skip(1)

    # 构建词法分析器
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

    # 测试词法分析器
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)
            
# 创建和返回一个词法分析器
def get_lexer():
    return VerilogLexer().build() 