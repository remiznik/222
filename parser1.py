from ast1 import *
from consts import *


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

    def program(self):

        node = self.compound_statement()
        self.eat(DOT)
        return node
    
    def compound_statement(self):

        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)

        root = Compound()
        for node in nodes:
            root.children.append(node)
        
        return root

    def statement_list(self):

        node = self.statement()
        results = [node]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())

        if self.current_token.type == ID:
            self.error()

        return results
    
    def statement(self):

        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        
        return node
    
    def assignment_statement(self):

        left = self.variable()
        token = self.current_token

        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node
    
    def variable(self):

        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        return NoOp()


    def factor(self):

        token = self.current_token 
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            node = self.variable()
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

    def block(self):

        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node )
        return node 
    
    def declarations(self):

        declarations = []
        if self.current_token.type = VAR:
            self.eat(VAR)
            while self.current_token.type == ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(SEMI)
        return declarations

    def variable_declaration(self):

        var_nodes = [Var(self.current_token)]
        self.eat(ID)

        while self.current_token == COMMA:
            self.eat(COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(ID)

        self.eat(COLOM)

        type_node = self.type_spec()
        var_declarations = [
            VarDec(var_node, type_node)
            for var_node in var_nodes
        ]
        return var_declarations
    def parse(self):

        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        return node
