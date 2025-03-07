import ply.lex as lex
import ply.yacc as yacc

# Lexer
tokens = (
    'SWITCH', 'CASE', 'DEFAULT', 'NUMBER', 'IDENTIFIER', 'CHAR_LITERAL', 'COLON', 'LBRACE', 'RBRACE',
)

# Token definitions
def t_SWITCH(t):
    r'switch'
    return t

def t_CASE(t):
    r'case'
    return t

def t_DEFAULT(t):
    r'default'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CHAR_LITERAL(t):
    r"\'[a-zA-Z]\'"
    t.value = t.value.strip("'")  # Strip the quotes to extract the character
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

t_COLON = r':'
t_LBRACE = r'{'
t_RBRACE = r'}'

# Ignoring spaces and tabs
t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Parser
def p_switch_statement(p):
    '''switch_statement : SWITCH IDENTIFIER LBRACE case_list RBRACE'''
    p[0] = ('switch', p[2], p[4])

def p_case_list(p):
    '''case_list : case_list case
                 | case_list default_case
                 | case
                 | default_case'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_case(p):
    '''case : CASE NUMBER COLON IDENTIFIER
            | CASE CHAR_LITERAL COLON IDENTIFIER'''
    p[0] = ('case', p[2], p[4])

def p_default_case(p):
    '''default_case : DEFAULT COLON IDENTIFIER'''
    p[0] = ('default', p[3])

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

# Interpreter
def interpret_switch(statement, value):
    if not statement:
        return "Invalid switch statement"

    switch_type, var_name, case_list = statement
    for case in case_list:
        if case[0] == 'case' and case[1] == value:
            return f"Matched case {case[1]}: {case[2]}"
        elif case[0] == 'default':
            return f"Default case: {case[1]}"
    return "No match"

# Prompt user for input code
print("Enter your switch statement (end with a blank line):")
user_input = []
while True:
    line = input()
    if line.strip() == "":
        break
    user_input.append(line)

# Join user input into a single string
code = "\n".join(user_input)

# Lexical analysis (tokenization)
lexer.input(code)

# Print the tokens for debugging
print("\nTokens:")
tokens = list(lexer)
for token in tokens:
    print(token)

# Now, parse the tokenized input
parsed = parser.parse(code)

# Check if parsing was successful
if parsed:
    print("Parsed result:", parsed)
    
    # Simulate the switch execution
    switch_value = input("Enter a value to switch on (for matching cases): ")
    # Convert input to int or keep as a single character
    try:
        switch_value = int(switch_value)
    except ValueError:
        switch_value = switch_value  # Keep as character
    
    result = interpret_switch(parsed, switch_value)
    print(result)
else:
    print("Parsing failed.")
