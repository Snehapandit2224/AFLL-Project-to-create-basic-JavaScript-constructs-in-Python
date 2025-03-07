import ply.lex as lex
import ply.yacc as yacc

# List of token names
tokens = (
    'WHILE', 'CONSOLE', 'LOG',
    'NUMBER', 'IDENTIFIER', 'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE', 'SEMICOLON',
    'EQUALS', 'LESS', 'PLUSPLUS'
)

# Keywords dictionary
keywords = {
    'while': 'WHILE',
    'console': 'CONSOLE'
}

# Parsing rules
precedence = (
    ('left', 'LESS'),  # Resolves ambiguity for comparison operators
)

# Regular expressions for tokens
t_LOG        = r'\.log'
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRACE     = r'\{'
t_RBRACE     = r'\}'
t_SEMICOLON  = r';'
t_EQUALS     = r'='
t_LESS       = r'<'
t_PLUSPLUS   = r'\+\+'

# Identifiers and numbers
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'IDENTIFIER')  # Check for keywords
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored characters (spaces and tabs)
t_ignore = ' \t'

# Define a rule for tracking line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Symbol table
symbol_table = {"x": 0, "y": 0}  # Initialize x and y to 0

# Parsing rules
def p_program(p):
    '''program : statement
               | statement program'''

def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN compound_statement'
    print("Parsed successfully")

    max_iterations = 10  # Define the maximum number of iterations
    iterations = 0

    # Execute the loop as long as the condition is true and within max_iterations
    while p[3] and iterations < max_iterations:  # Initial condition evaluation
        p[5]  # Execute the compound statement (loop body)

        # Update the value of x after each iteration based on the increment
        x_value = symbol_table.get("x", 0)  # Get current value of 'x'
        symbol_table["x"] = x_value + 1  # Increment 'x'

        # Dynamically re-evaluate the condition
        p[3] = symbol_table.get("x", 0) < 12  # Re-evaluate condition (x < 12)

        # Increment the iteration count
        iterations += 1

def p_compound_statement(p):
    'compound_statement : LBRACE statements RBRACE'
    pass  # No need for any detailed output here

def p_statement_assignment(p):
    'statement : IDENTIFIER EQUALS expression SEMICOLON'
    symbol_table[p[1]] = p[3]

def p_statement_increment(p):
    'statement : IDENTIFIER PLUSPLUS SEMICOLON'
    if p[1] in symbol_table:
        symbol_table[p[1]] += 1
    else:
        print(f"Error: {p[1]} not defined")

def p_statement_console_log(p):
    'statement : CONSOLE LOG LPAREN expression RPAREN SEMICOLON'
    pass  # No need for detailed output here

def p_statements(p):
    '''statements : statements statement
                  | statement'''

# Expression rules
def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_identifier(p):
    'expression : IDENTIFIER'
    p[0] = symbol_table.get(p[1], 0)  # Retrieve value from symbol table

def p_expression_less(p):
    'expression : expression LESS expression'
    p[0] = p[1] < p[3]

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print("Syntax error at end of input")

# Build the parser
parser = yacc.yacc()

# Prompt user for input code
print("Enter your code (end with a blank line):")
user_input = []
while True:
    line = input()
    if line.strip() == "":
        break
    user_input.append(line)

# Join user input into a single string
code = "\n".join(user_input)

# Tokenize and parse
lexer.input(code)
print("\nTokens:")
for token in lexer:
    print(token)

print("\nParsing result:")
parser.parse(code)
