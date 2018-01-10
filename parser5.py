import ply.yacc as yacc

import AST

from lex5 import tokens

precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),
)

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
}

vars = {}


def p_programme(p):
    ''' programme : statement
    | statement programme'''
    try:
        p[0] = AST.ProgramNode([p[1]] + p[2].children)
    except Exception as e:
        p[0] = AST.ProgramNode(p[1])


def p_programme_recursive(p):
    ''' programme : statement ';' programme '''
    p[0] = AST.ProgramNode([p[1]] + p[3].children)


def p_statement(p):
    ''' statement : assignation
        | structure '''
    p[0] = p[1]


def p_statement_print(p):
    ''' statement : PRINT expression '''
    p[0] = AST.PrintNode(p[2])


def p_structure(p):
    ''' structure : WHILE expression '{' programme '}' '''
    p[0] = AST.WhileNode([p[2], p[4]])


def p_structure_if(p):
    ''' structure : IF condition '{' programme '}' '''
    p[0] = AST.IfNode([p[2], p[4]])


def p_structure_switch(p):
    ''' structure : SWITCH condition '{' programme '}' '''
    p[0] = AST.IfNode([p[2], p[4]])


def p_structure_case(p):
    ''' structure : CASE DIGIT '{' programme '}' '''
    p[0] = AST.CaseNode([p[2], p[4]])


def p_expression_op(p):
    ''' expression : expression ADD_OP expression
            | expression MUL_OP expression '''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])


def p_expression_var(p):
    ''' expression : IDENTIFIER '''
    p[0] = AST.TokenNode(p[1])


def p_expression_num(p):
    ''' expression : DIGIT '''
    p[0] = AST.TokenNode(p[1])


def p_expression_bool(p):
    ''' expression : TRUE
    | FALSE'''
    p[0] = AST.TokenNode(p[1])


def p_expression_paren(p):
    ''' expression : '(' expression ')' '''
    p[0] = p[2]


def p_minus(p):
    ''' expression : ADD_OP expression %prec UMINUS '''
    p[0] = AST.OpNode(p[1], [p[2]])


# def p_assign(p):
#     ''' assignation : IDENTIFIER '=' expression '''
#     vars[p[1]] = (vars[p[1]][0], p[3])
#     p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


def p_assign_bool(p):
    ''' assignation : BOOL IDENTIFIER '=' BOOLEAN '''
    vars[p[2]] = ('BOOL', p[4])
    p[0] = AST.AssignDeclareNode(p[1], [AST.TokenNode(p[2]), AST.TokenNode(p[4])])


def p_assign_number(p):
    ''' assignation : NUMBER IDENTIFIER '=' DIGIT '''
    vars[p[2]] = ('NUMBER', p[4])
    p[0] = AST.AssignDeclareNode(p[1], [AST.TokenNode(p[2]), AST.TokenNode(p[4])])


def p_assign_text(p):
    ''' assignation : TEXT IDENTIFIER '=' CHARACTERS '''
    vars[p[2]] = ('TEXT', p[4])
    p[0] = AST.AssignDeclareNode(p[1], [AST.TokenNode(p[2]), AST.TokenNode(p[4])])


def p_condition(p):
    ''' condition : expression EQUAL expression
    | expression NOTEQUAL expression
    | expression '>' expression
    | expression '<' expression '''
    p[0] = AST.ConditionNode(p[2], [p[1], p[3]])


def p_error(p):
    print("Syntax error in line %d" % p.lineno)


def parse(program):
    return yacc.parse(program)


yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys, time

    prog = open(sys.argv[0]).read()
    result = yacc.parse(prog)

    time.sleep(1)

    if result:
        print(result)

        import os

        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0] + '-ast.pdf'
        graph.write_pdf(name)
        print("wrote ast to", name)
    else:
        print("Parsing returned no result!")
