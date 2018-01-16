import AST
import sys
import os
from parser_bracket import parse
from AST import addToClass

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
}


@addToClass(AST.ProgramNode)
def compile(self):
    """Compile each children of a program node"""
    pycode = ""
    for c in self.children:
        pycode += c.compile()
    return pycode


@addToClass(AST.TokenNode)
def compile(self):
    """Compile a token"""
    pycode = "%s" % self.tok
    if self.tok == "break":
        pycode += "\n"
    return pycode


@addToClass(AST.OpNode)
def compile(self):
    """Compile an operator +,-,/,*"""
    pycode = ""

    if len(self.children) == 1:
        pycode += "-"
        pycode += self.children[0].compile()
    elif len(self.children) == 2:
        pycode += self.children[0].compile()
        pycode += " " + self.op + " "
        pycode += self.children[1].compile()
    else:
        for c in self.children:
            pycode += c.compile()
        pycode += self.op + "\n"

    return pycode


@addToClass(AST.AssignNode)
def compile(self):
    """Compile an assignation"""
    pycode = "%s = " % self.children[0].tok
    pycode += "%s\n" % self.children[1].compile()
    return pycode


@addToClass(AST.AssignDeclareNode)
def compile(self):
    """Compile a node that declare and assign a variable"""
    pycode = "%s" % self.children[0].tok
    pycode += " = %s\n" % self.children[1].tok
    return pycode


@addToClass(AST.PrintNode)
def compile(self):
    """Compile the print function"""
    pycode = "print("
    pycode += "%s)\n" % self.children[0].compile()
    return pycode


@addToClass(AST.WhileNode)
def compile(self):
    """Compile a while structure"""
    pycode = "while "
    pycode += self.children[0].compile()
    pycode += ":\n"
    pycode += add_indentation(self.children[1].compile())
    return pycode


@addToClass(AST.LoopNode)
def compile(self):
    """Compile a loop structure"""
    pycode = "while True :\n"
    pycode += add_indentation(self.children[0].compile())
    return pycode


@addToClass(AST.ForNode)
def compile(self):
    """Compile a for num to num step num loop"""
    pycode = "for _ in range("
    pycode += number_to_int(self.children[0].compile())
    pycode += ", "
    pycode += number_to_int(self.children[1].compile())
    pycode += ", "
    pycode += number_to_int(self.children[2].compile())
    pycode += "):\n"
    pycode += add_indentation(self.children[3].compile())
    return pycode


@addToClass(AST.IfNode)
def compile(self):
    """Compile a if structure"""
    pycode = "if "
    pycode += self.children[0].compile()
    pycode += ":\n"
    pycode += add_indentation(self.children[1].compile())
    return pycode


@addToClass(AST.SwitchNode)
def compile(self):
    """Compile a switch structure"""
    pycode = "switch_var = "
    pycode += self.children[0].compile()
    pycode += "\n"
    for c in self.children[1:]:
        pycode += c.compile()
    return pycode


@addToClass(AST.CaseNode)
def compile(self):
    """Compile a case statement inside a switch"""
    pycode = "if switch_var"
    pycode += " == "
    pycode += self.children[0].compile()
    pycode += ":\n"
    pycode += add_indentation(remove_break_line(self.children[1].compile()))
    return pycode


@addToClass(AST.ConditionNode)
def compile(self):
    """Compile a condition node"""
    pycode = ""
    pycode += self.children[0].compile()
    pycode += " " + self.comparator + " "
    pycode += self.children[1].compile()
    return pycode


def number_to_int(string_number):
    """Remove the floating value of a string"""
    return str(int(float(string_number)))


def add_indentation(text):
    """"In a given string, add indentation of 4 spaces to each newline"""
    lines = text.split('\n')
    lines.pop()
    result = ""
    for line in lines:
        result += "    " + line + "\n"
    return result


def remove_break_line(text):
    """In a given string, remove instruction lines containing break"""
    return text[:text.rfind('break')]


if __name__ == '__main__':
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0] + '.py'
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()

    print("Wrote output to", name)
