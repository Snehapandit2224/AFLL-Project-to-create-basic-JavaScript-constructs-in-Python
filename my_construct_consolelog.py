import ply.lex as lex
import ply.yacc as yacc

# Lexer (Tokenizer) for identifying `console.log()` syntax, numbers, strings, operators, and booleans
tokens = (
    'CONSOLE_LOG', 'LPAREN', 'RPAREN', 'STRING', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 
    'TRUE', 'FALSE', 'GT', 'LT', 'EQ', 'NEQ', 'AND', 'OR', 'COMMA', 'SEMICOLON'
)

# Token definitions
t_CONSOLE_LOG = r'console\.log'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'  # New token for semicolon
t_STRING = r'(\".*?\"|\'.*?\')'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_GT = r'>'
t_LT = r'<'
t_EQ = r'=='
t_NEQ = r'!='
t_AND = r'&&'
t_OR = r'\|\|'

t_ignore = ' \t\n'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # Convert to integer
    return t

def t_TRUE(t):
    r'true'
    t.value = True  # Convert to boolean True
    return t

def t_FALSE(t):
    r'false'
    t.value = False  # Convert to boolean False
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Precedence and associativity rules for operators
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'GT', 'LT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Parser for handling the `console.log()` statement
def p_statement_log(p):
    '''statement : CONSOLE_LOG LPAREN expression RPAREN SEMICOLON
                 | CONSOLE_LOG LPAREN expression RPAREN'''
    print(p[3])

# Expression rules to handle numbers, booleans, strings, and binary operations
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression GT expression
                  | expression LT expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression AND expression
                  | expression OR expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        if p[3] == 0:
            print("Error: Division by zero")
            p[0] = None
        else:
            p[0] = p[1] / p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '!=':
        p[0] = p[1] != p[3]
    elif p[2] == '&&':
        p[0] = p[1] and p[3]
    elif p[2] == '||':
        p[0] = p[1] or p[3]

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = p[1]  # Already converted to integer

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = p[1][1:-1]  # Remove the surrounding quotes

def p_expression_boolean(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = p[1]  # Already converted to boolean

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ({p.value})")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

# Function to tokenize input and print tokens
def print_tokens(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:  # No more tokens
            break
        print(tok)

# Modify the handle_user_input function to use print_tokens
def handle_user_input():
    while True:
        try:
            user_input = input("Enter a console.log statement (or 'exit' to quit): ").strip()
            if user_input.lower() == 'exit':
                print("Exiting...")
                break
            print("Tokens:")
            print_tokens(user_input)  # Print the tokens
            print("Parsing Result:")
            parser.parse(user_input)  # Parse the input
        except Exception as e:
            print(f"Error: {e}")

# Run the user input handler
if __name__ == "__main__":
    handle_user_input()
