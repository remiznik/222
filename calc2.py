INTEGER, PLUS, MINUS, MUL, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MUL', 'EOF'

class Token(object):
    def __init__(self, type, value):

        self.type = type

        self.value = value

    def __str__(self):

        return 'Token({type}, {value})'.format(type=self.type, value=repr(self.vlaue))

    def __repr__(self):
        
        return self.__str__()

class Interpreter(object):

    def __init__(self, text):

        self.text = text
        self.pos = 0

        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):

        raise Exception('Error parsing input')
    
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
            
            self.error()

        return Token(EOF, None)

    def eat(self, token_type):

        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
    
    def expr(self):

        self.current_token = self.get_next_token()
        result = 0
        while self.current_token.type is not EOF:
            left = self.current_token
            self.eat(INTEGER)

            if self.current_token.type is not EOF:
                op = self.current_token

                if op.type == PLUS:
                    self.eat(PLUS)
                elif op.type == MUL:
                    self.eat(MUL)
                else:
                    self.eat(MINUS)

            if op.type == PLUS:
                result += left.value
            else:
                result -= left.value
            
        return result

def main():
    while True:
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()