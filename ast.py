class AST(object):

    pass

class BinOp(AST):

    def __init__(self, left, op, right):

        self.left = left 
        self.token = self.op = op
        self.right = right

    def __str__(self):

        return '{type}'.format(type=self.op.value)

class Num(AST):

    def __init__(self, token):
        
        self.left = None
        self.right = None
        self.token = token 
        self.value = token.value
    
    def __str__(self):

        return '{type}'.format(type=self.value)  

class UnaryOp(AST):

    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class Compound(AST):

    def __init__(self):
        self.children = []
    
class Var(AST):

    def __init__(self, token):
        self.token = token 
        self.value = token.value

class NoOp(AST):

    pass

class Assign(AST):

    def __init__(self, left, op, right):
        self.left = left 
        self.right = right 
        self.token = self.op = op



