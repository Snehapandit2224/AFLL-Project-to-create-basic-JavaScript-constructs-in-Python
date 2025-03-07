import ply.lex as lex
import ply.yacc as yacc

# List of token names
tokens = (
    'ID', 'NUMBER', 'QUESTION', 'COLON', 'EQ', 'GT', 'LT',
)

# Regular expression rules for simple tokens
t_QUESTION = r'\?'
t_COLON = r':'
t_EQ = r'=='
t_GT = r'>'
t_LT = r'<'

# Regular expression for identifiers (e.g., variable names)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Regular expression for numbers (integers)
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Dictionary to simulate variable values
variables = {
    'x': 6  # Assign a value to x for testing
}

# Parsing rules

# Starting rule
def p_expression(p):
    '''expression : ternary_expression
                  | simple_expression'''
    p[0] = p[1]

# Simple expression (numbers or identifiers)
def p_simple_expression(p):
    '''simple_expression : NUMBER
                         | ID'''
    # Retrieve the value of the identifier from the variables dictionary
    if isinstance(p[1], str) and p[1] in variables:
        p[0] = variables[p[1]]
    else:
        p[0] = p[1]

# Ternary expression (condition ? expr_true : expr_false)
def p_ternary_expression(p):
    '''ternary_expression : condition QUESTION expression COLON expression'''
    # Print the ternary expression structure
    print(f"Ternary expression structure: {p[1]} ? {p[3]} : {p[5]}")

    # Evaluate the condition
    condition_result = p[1]
    if condition_result:
        p[0] = p[3]
    else:
        p[0] = p[5]

    # Print the evaluated result of the ternary expression
    print(f"Ternary expression result: {p[0]}")

# Condition (simple comparison)
def p_condition(p):
    '''condition : expression GT expression
                 | expression LT expression
                 | expression EQ expression'''
    # Evaluate the condition based on the operator
    if p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
print("Generating LALR tables")
parser = yacc.yacc()

# Take JavaScript ternary operator code as user input
js_code = input("Enter JavaScript ternary operator code: ")

# Tokenize and print each token
lexer.input(js_code)
for token in lexer:
    print(token)

# Parse the input using the parser and evaluate
result = parser.parse(js_code)

# Display final evaluated result
print("Final Evaluated Result:", result)
