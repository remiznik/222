INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

class Token(object):

    def __init__(self, type, value):

        self.type = type 
        self.value = value

    def __str__(self):

        return 'Token({type}, {value}'.format(type=self.type, value=repr(self.value))
    
    def __repr__(self):
        return self.__str__()

class Interpreter(object):

    def __init__(self, text):

        self.text = text
        self.pos = 0
        self.current_token = None 