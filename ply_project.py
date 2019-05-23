count_test = 0

reserved = (
    'VOID', 'CHAR', 'SHORT', 'INT', 'LONG', 'FLOAT', 'DOUBLE',
    'IF', 'ELSE', 'WHILE', 'SWITCH', 'CASE', 'FOR', 'CONTINUE', 'BREAK',
    'DEFAULT', 'RETURN',
)
tokens = reserved + (
    'ID', 'TYPEID',                                                             # 식별자
    'NNUM', 'FNUM',                                                             # 자연수, 양의 실수, 문자와 문자열이 필요할 수도?
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',                                  # +, - , *, /, %
    'OR', 'AND', 'NOT',                                                         # |, &, ~
    'LOR', 'LAND', 'LNOT',                                                      # ||, &&, !
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',                                         # <, <=, >, >=, ==, !=
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE',             # (, ), [, ], {, }
    'COMMA', 'PERIOD', 'SEMI', 'COLON',                                         # ',', '.', ';', ':'
    'EQUALS', 'PLUSEQUAL', 'MINUSEQUAL', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL',  # =, +=, -=, *=, /=, %=
    'PLUSPLUS', 'MINUSMINUS',                                                   # ++, --
    'INCLUDE',                                                                  # #include
)
# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'

t_OR = r'\|'
t_AND = r'&'
t_NOT = r'~'

t_LOR = r'\|\|'
t_LAND = r'&&'
t_LNOT = r'!'

t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_PERIOD = r'\.'
t_SEMI = r';'
t_COLON = r':'

t_EQUALS = r'='
t_TIMESEQUAL = r'\*='
t_DIVEQUAL = r'/='
t_MODEQUAL = r'%='
t_PLUSEQUAL = r'\+='
t_MINUSEQUAL = r'-='
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'--'

def t_FNUM(t):
    r'[\d+][\.][\d+]'
    return t
def t_NNUM(t):
    r'\d+'
    return t


# 예약어와 식별자
reserved_dictionary = {}
for r in reserved:
    reserved_dictionary[r.lower()] = r
def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_dictionary.get(t.value, "ID")
    return t

t_INCLUDE = r'[#][i][n][c][l][u][d][e]'

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

# 시작
def p_start_syntex(t):
    '''start : include_statement start
             | variable_statement
             | parameter_list
             | function_statement
    '''

# #include 부분(라이브러리)
def p_include_statement(t):
    'include_statement : INCLUDE LT ID PERIOD ID GT'
    print("include 완료")

# 변수 선언
def p_variable_statement(t):
    '''variable_statement : type_specifier ID SEMI
                          | type_specifier ID LBRACKET NNUM RBRACKET SEMI
    '''
    print("변수 선언 완료")

# 매개변수(ex: int a, int b, ..., int z)
def p_empty(t):
    'empty : '

def p_parameter_list(t):
    '''parameter_list : type_specifier ID
                      | empty
                      | type_specifier ID COMMA parameter_list
    '''
    # print("매개변수 완료")
    # global count_test
    # count_test += 1
    # print(count_test)

# 인자(ex: (a, b, c)
def p_factor_list(t):
    '''factor_list : ID
                   | factor_list COMMA ID
    '''


# 자료형
def p_type_specifier(t):
    '''type_specifier : VOID
                      | CHAR
                      | SHORT
                      | INT
                      | LONG
                      | FLOAT
                      | DOUBLE
                      | TYPEID
                      '''

# 여러 문법들
def p_statement(t):
    '''statement : body_statement

    '''

# 함수 내부 구현
def p_body_statement(t):
    '''body_statement : variable_statement
    '''

# 함수 선언
def p_function_statement(t):
    '''function_statement : type_specifier ID LPAREN parameter_list RPAREN LBRACE body_statement RBRACE
                          | type_specifier ID LPAREN parameter_list RPAREN LBRACE RBRACE SEMI
    '''
    print("함수 완료")



def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

'''
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
'''

# 파일 읽기
try:
    f = open('test.txt', 'r')
    s = f.read()
except EOFError:
    print("error")

lexer.input(s)
while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
parser.parse(s)
