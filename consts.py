INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, ID, ASSIGN,  SEMI, DOT, BEGIN, END, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'ID', 'ASSIGN', 'SEMI', 'DOT', 'BEGIN', 'END', 'EOF'
)

RESERVED_KEYWORDS = { 
    'BEGIN' : Token('BEGIN', 'BEGIN'),
    'PROGRAM' : Token('VAR', 'VAR'),
    'DIV': Token('INTEGER_DIV', 'DIV'),
    'INTEGER': Token('INTEGER', 'INTEGER'),
    'REAL': Token('REAL', 'REAL'),
    'BEGIN': Token('BEGIN', 'BEGIN'),
    'END': Token('END', 'END')}