import AST
from AST import addToClass

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
}


@addToClass(AST.ProgramNode)
def compile(self):
    pycode = ""
    for c in self.children:
        pycode += c.compile()
    return pycode


@addToClass(AST.TokenNode)
def compile(self):
    pycode = ""
    pycode += "%s" % self.tok
    return pycode


@addToClass(AST.OpNode)
def compile(self):
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
    pycode = "%s = " % self.children[0].tok
    pycode += "%s\n" % self.children[1].compile()
    return pycode


@addToClass(AST.AssignDeclareNode)
def compile(self):
    pycode = "%s" % self.children[0].tok
    pycode += " = %s\n" % self.children[1].tok
    return pycode


@addToClass(AST.PrintNode)
def compile(self):
    pycode = "print("
    pycode += "%s)\n" % self.children[0].compile()
    return pycode


@addToClass(AST.WhileNode)
def compile(self):
    while self.children[0].compile():
        self.children[1].compile()


if __name__ == '__main__':
    from parser5 import parse
    import sys
    import os

    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0] + '.py'
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()

    print("Wrote output to", name)
