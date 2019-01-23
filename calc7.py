INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF'
)


class Token(object):
    def __init__(self, type, value):
        self.type = type 
        self.value = value 

    def __str__(self):

        return 'Token({type}, {value})'.format(type=self.type, value=repr(self.value))

    def __repr__(self):

        return self.__str__()
    
class Lexer(object):

    def __init__(self, text):

        self.text = text 
        self.pos = 0
        self.current_char = self.text[self.pos]
    
    def error(self):

        raise Exception("Invalid character")
    
    def advance(self):

        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):

        while self.current_char is not None and self.current_char.isspace():
            self.advance()


    def integer(self):

        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return int(result)

    def get_next_token(self):

        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            
            self.error()
        
        return Token(EOF, None)



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

class Parser(object):

    def __init__(self, lexer):

        self.lexer = lexer 
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Invalid sysntax")
    
    def eat(self, token_type):

        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def factor(self):

        token = self.current_token 
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node

    def term(self):

        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node, op=token, right=self.factor())
        
        return node
    
    def expr(self):

        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            
            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self):

        return self.expr()


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
        rj = self.printNode(tree)
        print(rj)
        lst = self.lispNode(tree)
        print(lst)
        return self.visit(tree)


def main():
    while True:
        try:
            try:
                text = raw_input('spi> ')
            except NameError:  # Python3
                text = input('spi> ')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)


if __name__ == '__main__':
    main()