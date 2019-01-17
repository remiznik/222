INT, PLUS, MINUS, MUL, DIV, EOF = "INT", "PLUS", "MUNUS", "MUL", "DIV", "EOF"

class Token(object):

    def __init__(self, type, value):

        self.type = type
        self.value = value

class Lexer(object):

    def __init__(self, text):

        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
    
    def error(self):
        raise Exception("Lexer error")
    
    def advance(self):
        self.pos += 1

        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def integer(self):

        reslt = ""
        while self.pos < len(self.text) and self.current_char.isdigit():
            reslt += self.current_char
            self.advance()
        
        return int(reslt)

    def skip_whitespace(self):

        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def get_next_token(self):

        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                return Token(INT, self.integer())

            if self.current_char == "*":
                self.advance()
                return Token(MUL, "*")
            
            if self.current_char == "/":
                self.advance()
                return Token(DIV, '/')

            if self.current_char == "+":
                self.advance()
                return Token(PLUS, "+")

            if self.current_char == "-":
                self.advance()
                return Token(MINUS, "-")

            self.error()
        return Token(EOF, None)


class Inter(object):

    def __init__(self, lexer):

        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def error(self):
        raise Exception("Interper error")

    def eat(self, type):

        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        self.eat(INT)
        return token.value

    def term(self):

        result = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.factor()
            if token.type == DIV:
                self.eat(DIV)
                result = result / self.factor()
        
        return result
    
    def expr(self):

        result = self.term()

        while self.current_token.type in (MINUS, PLUS):
            token = self.current_token
            if token.type == MINUS:
                self.eat(MUL)
                result = result - self.term()
            
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()

        return result
            




def main():

    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break

        if not text:
            continue

        lexer = Lexer(text)
        interpreter = Inter(lexer)
        result = interpreter.expr()

        print(result)

if __name__ == '__main__':
    main()