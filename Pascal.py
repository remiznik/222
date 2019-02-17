import Lexer    
import Parser
import Interpret

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
    text = """PROGRAM Part10;
        VAR
        number     : INTEGER;
        a, b, c, x : INTEGER;
        y          : REAL;
    BEGIN
    BEGIN
        number := 2;
        a := number;
        b := 10 * a + 10 * number DIV 4;
        c := a - - b
    END;
        x := 11;
        y := 20 / 7 + 3.14;
    END."""
    lexer = Lexer.Lexer(text)
    parser = Parser.Parser(lexer)
    interpreter = Interpret.Interpreter(parser)
    interpreter.interpret()
    print(interpreter.GLOBAL_SCOPE)
