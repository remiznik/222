import lexer
import parser1
import interpret

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
    # main()
    # lexer = Lexer('BEGIN a := 2; END.')
    # token = lexer.get_next_token()
    # while token.type is not EOF:
    #     print(token)
    #     token = lexer.get_next_token()
    text = """
    BEGIN
        BEGIN
            number := 2;
            a := number;
            b := 10 * a + 10 * number / 4;
            c := a - - b
        END;
        x := 11;
    END.
    """
    lexer = lexer.Lexer(text)
    parser = parser1.Parser(lexer)
    interpreter = interpret.Interpreter(parser)
    interpreter.interpret()
    print(interpreter.GLOBAL_SCOPE)
