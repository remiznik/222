INTEGER, PLUS, MINUS, DIV, LPAREN, RPAREN, EOF = ('INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF')

class Token(object):
    def __init__(self, type, value):
        self.type = type 
        self.value = value 

    def __str__(self):

        return 'Token({type}, {value})'.format(type=self.type, value=repr(self.value))

    def __reper__(self):

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
                return Token(DIV, '*')

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

class Num(AST):

    def __init__(self, token):
        
        self.token = token 
        self.value = token.value

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

        token = self.currnet_token 
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

        while self.current_token.type is (MUL, DIV):
            
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif:
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

    def parser(self):

        return self.expr()


class NodeVisitor(object):

    def visit(self, node):
        