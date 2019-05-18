tokens = (
    'NAME', 'NUMBER',                                           # 변수, 상수
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',               # 연산자
    'LPAREN', 'RPAREN',                                         # (, )
    'INCLUDE', 'ANGLELPAREN', 'ANGLERPAREN', 'LIBRARY',         # #include 부분(#include, <, >. library)
    'TYPE',
)
# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

t_INCLUDE = r'[#][i][n][c][l][u][d][e]'
t_ANGLELPAREN = r'<'
t_ANGLERPAREN = r'>'
t_LIBRARY = r'[a-zA-Z0-9_]+[.][a-zA-Z0-9_]+'

t_TYPE = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}

# 타입 이름
types = {'int', 'double', 'float', 'long', }

# 라이브러리 이름
libraries = {}

def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]

def p_statement_expr(t):
    'statement : expression'
    print(t[1])

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

# 변수 선언 부분
def p_expression_variableDeclaration(t):
    'expression : TYPE NAME'
    if(t[1] in types == True):
        t[0] = names[t[2]]
        print("변수 선언 완료")
    else:
        p_error(t)

# 변수 초기화 부분
def p_statement_initVariable(t):
    'statement : TYPE NAME EQUALS expression'
    names[t[2]] = t[4]
    print("변수 초기화 완료")

# #include 부분(라이브러리)
def p_expression_library(t):
    'expression : LIBRARY'
    try:
        t[0] = libraries[t[1]]
    except LookupError:
        print("Undefined library '%s" % t[1])
        t[0] = 0
def p_statement_includeLibrary(t):
    'statement : INCLUDE ANGLELPAREN LIBRARY ANGLERPAREN'
    print("include 완료")
# #include 부분 끝

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')  # Use raw_input on Python 2
    except EOFError:
        break

    #실험
    lexer.input(s)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
    #실험

    parser.parse(s)