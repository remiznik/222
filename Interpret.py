from Consts import *
import symbol_table

class NodeVisitor(object):

    def visit(self, node):
        
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):

        raise Exception('No visist_{} method'.format(type(node).__name__))

class SymbolTableBuilder(NodeVisitor):
    def __init__(self):
        self.symtab = symbol_table.SymbolTable()
    
    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        
        self.visit(node.compound_statement)

    def visit_Program(self, node):
        self.visit(node.block)
    
    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Num(self, node):
        pass

    def visit_UnaryOp(self, node):
        self.visit(node.expr)
    
    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass
    
    def vistit_VarDecl(self, node):
        type_name = node.type_node.value
        type_symbol = self.symtab.lookup(type_name)
        var_name = node.var_node.value
        var_symbol = symbol_table.VarSymbol(var_name, type_symbol)
        self.symtab.define(var_symbol)
    
    def visit_Assign(self, node):
        var_name = node.left.value
        var_symbol = self.symtab.lookup(var_name)
        if var_symbol is None:
            raise NameError(repr(var_name))
        
        self.visit(node.right)
    
    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.symtab.lookup(var_name)
        if var_symbol is None:
            raise NameError(repr(var_name))

    def visit_ProcedureDecl(self, node):
        pass


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
        elif node.op.type == INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == FLOAT_DIV:
            return float(self.visit(node.left)) / float(self.visit(node.right))
         

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
    
    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        
        self.visit(node.compound_statement)
    
    def visit_ProcedureDecl(self, node):
        pass

    def visit_VarDecl(self, node):
        pass
    
    def visit_Type(self, node):
        pass

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

