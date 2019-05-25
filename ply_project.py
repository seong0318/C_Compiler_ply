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
    'OR', 'AND', 'XOR','NOT',                                                   # |, &, ^, ~
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
t_XOR = r'\^'
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
             | function_statement
             | assign_expression
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
                      | NNUM
                      | FNUM
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



# expression
def p_expression_list(t):
    '''expression : assign_expression
                  | expression COMMA assign_expression
    '''

# 변수에 값 할당하는 부분
def p_assign_expression(t):
    '''assign_expression : logic_expression
                         | prefix_expression assign_operator assign_expression
    '''
    print("값 할당 완료")
def p_assign_operator(t):
    '''assign_operator : EQUALS
                       | PLUSEQUAL
                       | MINUSEQUAL
                       | TIMESEQUAL
                       | DIVEQUAL
                       | MODEQUAL
    '''

# -------logic_expression 관련-------
# prefix
def p_prefix_expression(t):
    '''prefix_expression : postfix_expression
                         | PLUSPLUS prefix_expression
                         | MINUSMINUS prefix_expression
    '''
    print("prefix 완료")
# 변수와 상수
def p_target_expression(t):
    '''target : ID
              | NNUM
              | FNUM
    '''
# postfix 배열 다시 볼 것
def p_postfix_expression(t):
    '''postfix_expression : target
                          | target LBRACKET expression RBRACKET
                          | target LPAREN RPAREN
                          | target LPAREN factor_list RPAREN
                          | target PLUSPLUS
                          | target MINUSMINUS
    '''
# 산술 표현식
def p_arithmetic_expression(t):
    '''arithmetic_expression : prefix_expression
                             | arithmetic_expression PLUS prefix_expression
                             | arithmetic_expression MINUS prefix_expression
                             | arithmetic_expression TIMES prefix_expression
                             | arithmetic_expression DIVIDE prefix_expression
                             | arithmetic_expression MOD prefix_expression
    '''
# 대소 비교
def p_logic_compare_expression(t):
    '''logic_compare_expression : arithmetic_expression
                                | logic_compare_expression EQ arithmetic_expression
                                | logic_compare_expression NE arithmetic_expression
                                | logic_compare_expression LT arithmetic_expression
                                | logic_compare_expression LE arithmetic_expression
                                | logic_compare_expression GT arithmetic_expression
                                | logic_compare_expression GE arithmetic_expression
    '''
# 비트 연산
def p_bit_or_expression(t):
    '''bit_or_expression : bit_xor_expression
                         | bit_or_expression OR bit_xor_expression
    '''
def p_bit_xor_expression(t):
    '''bit_xor_expression : bit_and_expression
                          | bit_xor_expression XOR bit_and_expression
    '''
def p_bit_and_expression(t):
    '''bit_and_expression : logic_compare_expression
                          | bit_and_expression AND logic_compare_expression
    '''
# 논리 연산
def p_logic_or_expression(t):
    '''logic_or_expression : logic_and_expression
                           | logic_or_expression LOR logic_and_expression
    '''
def p_logic_and_expression(t):
    '''logic_and_expression : bit_or_expression
                            | logic_and_expression LAND bit_or_expression
    '''
# 논리 표현
def p_logic_expression(t):
    'logic_expression : logic_or_expression'
    print("논리 표현 완료")




# 여러 문법들
def p_statement(t):
    '''statement : body_statement

    '''

# 함수 내부 구현
def p_body_statement(t):
    '''body_statement : LBRACE variable_statement RBRACE
                      | LBRACE RBRACE
    '''

# 함수 선언
def p_function_statement(t):
    '''function_statement : type_specifier ID LPAREN parameter_list RPAREN body_statement

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
