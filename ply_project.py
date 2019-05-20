reserved = (
    'VOID', 'CHAR', 'SHORT', 'INT', 'LONG', 'FLOAT', 'DOUBLE',
    'IF', 'ELSE', 'WHILE', 'SWITCH', 'CASE', 'FOR', 'CONTINUE', 'BREAK',
    'DEFAULT', 'RETURN',
)
tokens = reserved + (
    'ID', 'TYPEID',     # 식별자
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',                                  # +, - , *, /, %
    'OR', 'AND', 'NOT',                                                         # |, &, ~
    'LOR', 'LAND', 'LNOT',                                                      # ||, &&, !
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',                                         # <, <=, >, >=, ==, !=
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE',             # (, ), [, ], {, }
    'COMMA', 'PERIOD', 'SEMI', 'COLON',                                         # ',', '.', ';', ':'
    'EQUALS', 'PLUSEQUAL', 'MINUSEQUAL', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL',  # =, +=, -=, *=, /=, %=
    'PLUSPLUS', 'MINUSMINUS',                                                   # ++, --
    'INCLUDE',                                                                  # 'LIBRARY'
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


# #include 부분(라이브러리)
def p_include_statement(t):
    'start : INCLUDE LT ID PERIOD ID GT'
    print("include 완료")
def p_declaration_start(t):
    'start : declaration'
    print("완료")

#선언
def p_declaration(t):
    'declaration : declaration_specifiers ID SEMI'
    print("선언 완료")
# def p_declaration_list(t):
#   'declaration : declaration_specifiers init_declarator_list SEMI'

def p_declaration_specifier(t):
    'declaration_specifiers : type_specifier'
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
    print("자료형")


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