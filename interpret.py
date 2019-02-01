from consts import *
class NodeVisitor(object):

    def visit(self, node):
        
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):

        raise Exception('No visist_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_NoOp(self, node):
        pass
    
    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)
    
    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            return NameError(repr(var_name))
        return val

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_UnaryOp(self, node):
        op = node.op.type 
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def printNode(self, node):
        
        method_name = 'printNode_' + type(node).__name__
        printVisit = getattr(self, method_name, self.generic_visit)
        return printVisit(node)

    def printNode_BinOp(self, node):        
        return  self.printNode(node.left) + self.printNode(node.right) + node.op.value


    def printNode_Num(self, node):
        return str(node.value)

    
    def lispNode(self, node):
        
        method_name = 'lispNode_' + type(node).__name__
        printVisit = getattr(self, method_name, self.generic_visit)
        return printVisit(node)

    def lispNode_BinOp(self, node):        
        return  "(" + node.op.value +  self.lispNode(node.left) + self.lispNode(node.right) + ")"


    def lispNode_Num(self, node):
        return str(node.value)


    def interpret(self):
        tree = self.parser.parse()
        # rj = self.printNode(tree)
        # print(rj)
        # lst = self.lispNode(tree)
        # print(lst)
        return self.visit(tree)

