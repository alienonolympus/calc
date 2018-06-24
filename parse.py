#/usr/bin/python3
'''Parses strings and returns an Expression object'''

from expression import Expression

def operation_level(op):
    if op == '+' or op == '-':
        return 1
    elif op == '*' or op == '/':
        return 2
    else:
        return 99

def lexer(expression_string):
    '''Turns a string into a list of mathematical expressions'''
    expr_string = expression_string
    i = 0
    expr_list = []
    operations = [
        '+',
        '-',
        '*',
        '/',
        '(',
        ')'
    ]

    while i < len(expression_string):
        if expr_string[i] in operations:
            expr_list.append(expr_string[i])
        else:
            num_string = ''
            decimal = False
            while i < len(expression_string) and (expr_string[i].isdigit() or expr_string[i] == '.'):
                if expr_string[i] == '.':
                    if not decimal:
                        decimal = True
                    else:
                        i += 1
                        continue
                num_string += expr_string[i]
                i += 1
            expr_list.append(num_string)
            i -= 1
        i += 1
    
    return expr_list

def parse(expression_string):
    '''Parses a string and returns an Expression object'''
    expr_list = lexer(expression_string)
    expr = Expression()

    #Determine the root node
    current_index = 0

    for i in range(len(expr_list)):
        if operation_level(expr_list[i]) <= operation_level(expr_list[current_index]):
            current_index = i
    
    if operation_level(expr_list[current_index]) == 99: #Check if root node is a number
        expr.set_value(float(expr_list[current_index]))
    else:
        expr.set_value(expr_list[current_index])
        expr.add_children(parse(expr_list[0:current_index]), parse(expr_list[current_index + 1:]))
    
    return expr