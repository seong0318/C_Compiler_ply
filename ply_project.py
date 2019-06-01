includeNum = 0
declaredFunctionNum = 0
declaredVariableNum = 0
conditionalNum = 0
loopNum = 0
calledFunctionNum = 0

reserved = (
    'VOID', 'CHAR', 'SHORT', 'INT', 'LONG', 'FLOAT', 'DOUBLE',
    'IF', 'ELSE', 'WHILE', 'FOR', 'CONTINUE', 'BREAK',
    'RETURN',
)
tokens = reserved + (
    'ID', 'TYPEID', 'CONSTSTR', 'CONSTCHAR',                                    # 식별자
    'NNUM', 'FNUM',                                                             # 자연수, 양의 실수, 문자와 문자열이 필요할 수도?
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',                                  # +, - , *, /, %
    'OR', 'AND', 'XOR','NOT',                                                   # |, &, ^, ~
    'LOR', 'LAND', 'LNOT',                                                      # ||, &&, !
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',                                         # <, <=, >, >=, ==, !=
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE',             # (, ), [, ], {, }
    'COMMA', 'PERIOD', 'SEMI',                                                  # ',', '.', ';'
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

t_EQUALS = r'='
t_TIMESEQUAL = r'\*='
t_DIVEQUAL = r'/='
t_MODEQUAL = r'%='
t_PLUSEQUAL = r'\+='
t_MINUSEQUAL = r'-='
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'--'

t_CONSTSTR = r'\"[A-Za-z_\d\!=\+\-\*\/\%\:\\\(\)\.\,\ ]*\"'
t_CONSTCHAR = r'\'[A-Za-z_\d\!=\+\-\*\/\%\:\\\(\)\.\,\ ]\''

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

# #include
t_INCLUDE = r'[#][i][n][c][l][u][d][e]'

# 공백문자
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
    '''start : global_statement
             | start global_statement
    '''

# 전역 변수와 함수(시작부분)
def p_global_statement(t):
    '''global_statement : include_statement
                        | function_statement
                        | declaration_statement
    '''

# #Include 부분
def p_include_statement(t):
    '''include_statement : INCLUDE LT ID GT
                         | INCLUDE LT ID PERIOD ID GT
    '''
    global includeNum
    includeNum += 1
#    print("include 완료")

# 선언 부분
def p_declaration_statement(t):
    '''declaration_statement : function_call SEMI
                             | variable_statement SEMI
    '''

# 함수 호출
def p_function_call(t):
    '''function_call : ID LPAREN RPAREN
                     | ID LPAREN factor_list RPAREN
                     | ID LPAREN parameter_list RPAREN
    '''
    global calledFunctionNum
    calledFunctionNum += 1
#    print("함수 호출 완료")

# 변수 선언(semi declaration 으로 옮김)
def p_variable_statement(t):
    '''variable_statement : type_specifier variable_init
                          | type_specifier ID LBRACKET NNUM RBRACKET
    '''
    global declaredVariableNum
    declaredVariableNum += 1
#    print("변수 선언 완료")

# 초기화
def p_variable_init(t):
    '''variable_init : ID
                     | ID EQUALS init_statement
    '''
def p_init_statement(t):
    'init_statement : assign_expression'

# 매개변수(ex: int a, int b, ..., int z)
def p_empty(t):
    'empty : '
def p_parameter_list(t):
    '''parameter_list : type_specifier ID
                      | VOID
                      | type_specifier ID COMMA parameter_list
    '''
    # print("매개변수 완료")

# 인자(ex: (a, b, c))
def p_factor_list(t):
    '''factor_list : CONSTSTR
                   | CONSTCHAR
                   | arithmetic_expression
                   | factor_list COMMA factor_list
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
    '''expression_list : assign_expression
                       | expression_list COMMA assign_expression
    '''

# 변수에 값 할당하는 부분
def p_assign_expression(t):
    '''assign_expression : logic_expression
                         | prefix_expression assign_operator assign_expression
    '''
#    print("값 할당 완료")
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
                         | AND prefix_expression
                         | TIMES prefix_expression
                         | NOT prefix_expression
                         | LNOT prefix_expression
    '''
#    print("prefix 완료")
# 변수와 상수
def p_target_expression(t):
    '''target : ID
              | NNUM
              | FNUM
              | function_call
              | LPAREN expression_list RPAREN
    '''
# postfix
def p_postfix_expression(t):
    '''postfix_expression : target
                          | target LBRACKET expression_list RBRACKET
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
#    print("논리 표현 완료")

# 여러 문법들
def p_grammer_list(t):
    '''grammar_list : grammar_statement
                    | grammar_list grammar_statement
    '''
def p_grammer_statement(t):
    '''grammar_statement : expression_list SEMI
                         | body_statement
                         | iteration_statement
                         | if_statement
                         | branch_statement
                         | declaration_statement
    '''

# 중괄호 내부 구현
def p_body_statement(t):
    'body_statement : LBRACE grammar_list RBRACE'
#    print("중괄호 내부 구현")

# 함수 구현
def p_function_statement(t):
    '''function_statement : type_specifier ID LPAREN parameter_list RPAREN body_statement
                          | type_specifier ID LPAREN RPAREN body_statement
    '''
    global declaredFunctionNum
    declaredFunctionNum += 1
#    print("함수 완료")

# 반복문
def p_expression_for(t):
    '''expression_for : expression_list
                      | type_specifier expression_list
                      | empty
    '''
def p_iteration_statement(t):
    '''iteration_statement : WHILE LPAREN expression_list RPAREN grammar_statement
                           | FOR LPAREN expression_for SEMI expression_for SEMI expression_for RPAREN grammar_statement
    '''
    global loopNum
    loopNum += 1
#    print("반복문 완료")

# if문 else
def p_if_statement(t):
    'if_statement : IF LPAREN expression_list RPAREN grammar_statement else_statement'
    global conditionalNum
    conditionalNum += 1
#    print("if 문 완료")
def p_else_statement(t):
    '''else_statement : empty
                      | ELSE grammar_statement
    '''
#    print("else 문 완료")

# 분기문
def p_branch_statement(t):
    '''branch_statement : RETURN expression_list SEMI
                        | RETURN empty SEMI
                        | CONTINUE SEMI
                        | BREAK SEMI
    '''
#    print("분기 완료")

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

def printresult():
    print("#include: %d" % includeNum)
    print("Declared Functions: %d" % declaredFunctionNum)
    print("Declared Variables: %d" % declaredVariableNum)
    print("Conditional Statements: %d" % conditionalNum)
    print("Loop: %d" % loopNum)
    print("Called Function: %d" % calledFunctionNum)

while True:
    includeNum = 0
    declaredFunctionNum = 0
    declaredVariableNum = 0
    conditionalNum = 0
    loopNum = 0
    calledFunctionNum = 0

    filepath = input()

    # 파일 읽기
    try:
        f = open(filepath, 'r')
        s = f.read()
        lexer.input(s)
        parser.parse(s)
        printresult()

    except (FileNotFoundError, EOFError):
        print("Error")