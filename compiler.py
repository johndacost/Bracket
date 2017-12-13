from TP.TP4 import AST
from TP.TP4.AST import addToClass

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
}


@addToClass(AST.TokenNode)
def compile(self):
    bytecode = ""
    if isinstance(self.tok, str):
        bytecode += "PUSHV %s\n" % self.tok
    else:
        bytecode += "PUSHC %s\n" % self.tok
    return bytecode


@addToClass(AST.OpNode)
def compile(self):
    bytecode = ""

    if len(self.children) == 1:
        bytecode += self.children[0].compile()
        bytecode += "USUB\n"
    else:
        for c in self.children:
            bytecode += c.compile
        bytecode += operations[self.op] + "\n"

    return bytecode


@addToClass(AST.AssignNode)
def compile(self):
    bytecode = self.children[0].compile()
    bytecode += "PUSHV %s\n" % self.children[0].tok
    bytecode += "PUSHC %s\n" % self.children[1].tok
    return bytecode


@addToClass(AST.PrintNode)
def compile(self):
    bytecode = self.children[0].compile()
    bytecode += "PRINT\n"
    return bytecode


@addToClass(AST.WhileNode)
def compile(self):
    while self.children[0].compile():
        self.children[1].compile()


if __name__ == '__main__':
    from TP.TP3.parser5 import parse
    import sys
    import os

    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0] + '.vm'
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()

    print("Wrote output to", name)
