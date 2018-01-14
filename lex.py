import ply.lex as lex

reserved_words = (
    'step',
    'for',
    'to',
    'while',
    'if',
    'else',
    'switch',
    'case',
    'default',
    'print',
    'PI',
    'true',
    'false',
    'number',
    'list',
    'text',
    'bool',
    'break',
    'loop'
)

tokens = (
             'DIGIT',  # Represent a number
             'CHARACTERS',  # Represent a string
             'BOOLEAN',  # true or false
             'CONTEXT_OP',  # not used
             'ADD_OP',
             'MUL_OP',
             'COMP_OP',
             'IDENTIFIER',
             'EQUAL',
             'NOTEQUAL'
         ) + tuple(map(lambda s: s.upper(), reserved_words))

literals = '();={}><,."'


def t_DIGIT(t):
    r'\d+(\.\d+)?'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Line %d: Problem while parsing %s, number expected" % (t.lineno, t.value))
        t.value = 0
    return t


def t_CHARACTERS(t):
    r'".*"'
    return t


def t_BOOLEAN(t):
    r'true|false'
    try:
        t.value = bool(t.value)
    except ValueError:
        print("Line %d: Problem while parsing %s, boolean expected" % (t.lineno, t.value))
        t.value = 0
    return t


def t_CONTEXT_OP(t):
    r'\.'
    return t


def t_ADD_OP(t):
    r'[+-]'
    return t


def t_MUL_OP(t):
    r'[*/]'
    return t


def t_EQUAL(t):
    r'=='
    return t


def t_NOTEQUAL(t):
    r'!='
    return t


def t_COMP_OP(t):
    r'==|!=|=!|<|>'
    return t


def t_IDENTIFIER(t):
    r'[A-Za-z_]\w*'
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print("Illegal character '%s' line : %i" % (repr(t.value[0]), t.lineno))
    t.lexer.skip(1)


lex.lex()

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()

    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok:
            break
        print("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
