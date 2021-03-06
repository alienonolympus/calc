#/usr/bin/python3
'''Parses strings into a tree that can be evaluated to return the value'''

import math, sys, os

class Expression():
    '''Tree structure that represents mathematical expressions'''

    def __init__(self, value=0):
        self.set_value(value)
        self.children = []
        self.mode = 'radians'
    
    def __repr__(self):
        sys.stdout = open(os.devnull, "w") # Prevents output
        result = '\n' + self.pretty()
        sys.stdout = sys.__stdout__ # Prevents output
        return result

    def __str__(self):
        sys.stdout = open(os.devnull, "w") # Prevents output
        result = str(self.evaluate())
        sys.stdout = sys.__stdout__ # Prevents output
        return result
    
    def set_value(self, value):
        '''Sets the value of the expression'''
        if isinstance(value, float):
            self.expr_type = 'num'
            self.value = value
        else:
            self.expr_type = value
            self.value = 0
    
    def add_child(self, expr):
        '''Add a new expression as a child'''
        self.children.append(expr)
    
    def add_children(self, *exprs):
        '''Add several new expressions as children'''
        for expr in exprs:
            if isinstance(expr, Expression):
                self.add_child(expr)
            else:
                self.add_child(Expression(expr))
    
    def execute(self):
        '''Executes the expression without showing value'''
        self.evaluate()
    
    def evaluate(self):
        '''Returns the value of the expression'''
        if self.expr_type == 'num':
            return self.value
        elif self.expr_type == 'if':
            if self.evaluate_child(0):
                return self.evaluate_child(1)
            else:
                return self.evaluate_child(2)
        elif self.expr_type == '=':
            return self.evaluate_child(0) == self.evaluate_child(1)    
        elif self.expr_type == '>':
            return self.evaluate_child(0) > self.evaluate_child(1)                
        elif self.expr_type == '<':
            return self.evaluate_child(0) < self.evaluate_child(1)
        elif self.expr_type == '≥':
            return self.evaluate_child(0) >= self.evaluate_child(1)                
        elif self.expr_type == '≤':
            return self.evaluate_child(0) <= self.evaluate_child(1)
        elif self.expr_type == '&':
            return self.evaluate_child(0) and self.evaluate_child(1)                
        elif self.expr_type == '|':
            return self.evaluate_child(0) or self.evaluate_child(1)
        elif self.expr_type == '!':
            return not self.evaluate_child(0)
        elif self.expr_type == 'o':
            result = self.evaluate_child(0)
            print(chr(int(result)), end = '')
            return result
        elif self.expr_type == '+':
            return self.evaluate_child(0) + self.evaluate_child(1)
        elif self.expr_type == '-':
            return self.evaluate_child(0) - self.evaluate_child(1)
        elif self.expr_type == '*':            
            return self.evaluate_child(0) * self.evaluate_child(1)
        elif self.expr_type == '/':
            return self.evaluate_child(0) / self.evaluate_child(1)
        elif self.expr_type == '%':
            return self.evaluate_child(0) % self.evaluate_child(1)
        elif self.expr_type == '^':
            return math.pow(self.evaluate_child(0), self.evaluate_child(1))
        elif self.expr_type == 'v':
            return math.pow(self.evaluate_child(1), (1 / self.evaluate_child(0)))
        elif self.expr_type == 'l':
            return math.log(self.evaluate_child(1), self.evaluate_child(0))
        elif self.expr_type == 'L':
            return math.log10(self.evaluate_child(0))
        elif self.expr_type == 'n':
            return - self.evaluate_child(0)
        elif self.expr_type == 's':
            return math.sin(self.evaluate_trig_child(0))
        elif self.expr_type == 'c':
            return math.cos(self.evaluate_trig_child(0))
        elif self.expr_type == 't':
            return math.tan(self.evaluate_trig_child(0))
        elif self.expr_type == 'S':
            return self.degrees_or_radians(math.asin(self.evaluate_child(0)))
        elif self.expr_type == 'C':
            return self.degrees_or_radians(math.acos(self.evaluate_child(0)))
        elif self.expr_type == 'T':
            return self.degrees_or_radians(math.atan(self.evaluate_child(0)))
        elif self.expr_type == 'ś':
            return math.sinh(self.evaluate_trig_child(0))
        elif self.expr_type == 'ć':
            return math.cosh(self.evaluate_trig_child(0))
        elif self.expr_type == 't́':
            return math.tanh(self.evaluate_trig_child(0))
        elif self.expr_type == 'Ś':
            return self.degrees_or_radians(math.asinh(self.evaluate_child(0)))
        elif self.expr_type == 'Ć':
            return self.degrees_or_radians(math.acosh(self.evaluate_child(0)))
        elif self.expr_type == 'T́':
            return self.degrees_or_radians(math.atanh(self.evaluate_child(0)))
    
    def evaluate_child(self, index):
        '''Evaluate an indexed child'''
        return self.children[index].evaluate()

    def degrees_or_radians(self, value):
        '''Check current mode and see if degrees or radians should be used for trigonometric functions'''
        if self.mode == 'radians':
            return value
        elif self.mode == 'degrees':
            return math.radians(value)
    
    def evaluate_trig_child(self, index):
        '''Evaluate an indexed child for trigonometric functions'''
        return self.degrees_or_radians(self.evaluate_child(index))
    
    def pretty(self, indent=0):
        '''Generates a string showing the structure of the expression tree'''
        pretty_output = 'Value: ' + str(self.evaluate()) + ', Type: ' + self.expr_type + '\n'
        if self.children:
            for child in self.children:
                pretty_output += '    ' * indent + '|-- ' + child.pretty(indent + 1)
        return pretty_output

    def pretty_print(self):
        '''Prints the structure of the expression tree'''
        print(self.pretty())


def isunary(op):
    '''Checks if an operation is an unary operation'''
    return op in [
        'o',
        '!',
        'n',
        's',
        'c',
        't',
        'S',
        'C',
        'T',
        'L',
        'ś',
        'ć',
        't́',
        'Ś',
        'Ć',
        'T́'
    ]

def operation_level(op):
    '''Assigns a numerical value to operations for easier comparison'''
    if op == '?' or op == ':':
        return -99
    elif op == '&' or op == '|':
        return -1
    elif op == '>' or op == '<' or op == '≥' or op == '≤' or op == '=':
        return 0
    elif op == '+' or op == '-':
        return 1
    elif op == '*' or op == '/' or op == '%':
        return 2
    elif op == '^' or op == 'v' or op == 'l':
        return 3
    elif isunary(op):
        return 4
    elif op == '(' or op == ')':
        return 98
    elif op == 'I':
        return 100
    else:
        return 99

def outer_brackets(expr):
    '''Returns an array containing the indices of the outermost pairs of brackets'''
    indices = []
    bracket_count = 0
    closed_outer_bracket_count = 0
    for i in range(len(expr)):
        if expr[i] == '(':
            bracket_count += 1
            if bracket_count == 1:
                indices.append([0, 0])
                indices[closed_outer_bracket_count][0] = i
        elif expr[i] == ')':
            bracket_count -= 1
            if bracket_count == 0:
                indices[closed_outer_bracket_count][1] = i
                closed_outer_bracket_count += 1
    return indices

def ternary(expr, first_op, second_op):
    '''Provides the indices of the ternary operations (accepted as 2nd and 3rd arguments)'''
    op_count = 0
    if_index = 0
    else_index = 0
    if first_op in expr and second_op in expr:
        for i in range(len(expr)):
            if expr[i] == first_op:
                if_index = i
                op_count += 1
            if expr[len(expr) - 1 - i] == second_op:
                else_index = len(expr) - 1 - i
                op_count += 1
            if op_count == 2:
                return (if_index, else_index)
            if i * 2 > len(expr):
                return False
    return False

def isfloat(string):
    '''Checks if a string is a float or not.
    Returns 0 for non-floats, 1 for regular floats and 2 for mathematical constants.'''
    if string == 'e' or string == 'π':
        return 2
    for ch in string:
        if not ch.isdecimal() and ch != '.':
            return 0
    return 1

def translate(string):
    '''Turns a string using proper mathematical notation into easier to parse language'''
    expr_string = ''.join(string)
    expr_string = expr_string.replace('sqrt', '2v')
    expr_string = expr_string.replace('pi', 'π')
    expr_string = expr_string.replace('<=', '≤')
    expr_string = expr_string.replace('>=', '≥')
    expr_string = expr_string.replace('and', '&')
    expr_string = expr_string.replace('or', '|')
    expr_string = expr_string.replace('not', '!')
    expr_string = expr_string.replace('mod', '%')
    expr_string = expr_string.replace('log', 'L')
    expr_string = expr_string.replace('ln', 'el')
    expr_string = expr_string.replace('arcsin', 'S')
    expr_string = expr_string.replace('arccos', 'C')
    expr_string = expr_string.replace('arctan', 'T')
    expr_string = expr_string.replace('sin', 's')
    expr_string = expr_string.replace('cos', 'c')
    expr_string = expr_string.replace('tan', 't')
    expr_string = expr_string.replace('arcsinh', 'Ś')
    expr_string = expr_string.replace('arccosh', 'Ć')
    expr_string = expr_string.replace('arctanh', 'T́')
    expr_string = expr_string.replace('sinh', 'ś')
    expr_string = expr_string.replace('cosh', 'ć')
    expr_string = expr_string.replace('tanh', 't́')
    return expr_string

def lexer(expression_string):
    '''Turns a string into a list of mathematical expressions'''
    expr_string = expression_string
    i = 0
    expr_list = []
    operations = [
        '?', # if
        ':', # else
        '=', # equal to
        '>', # greater than
        '<', # less than
        '≥', # greater than or equal to
        '≤', # less than or equal to
        '&', # and
        '|', # or
        '!', # not
        'o', # output
        'I', # input
        '+', # addition
        '-', # subtraction
        '*', # multiplication
        '/', # division
        '%', # modulo
        '(', # lparenthesis
        ')', # rparenthesis
        '^', # exponent
        'v', # root
        'l', # logarithm
        'L', # base-10 logarithm
        'n', # negate
        's', # sine
        'c', # cosine
        't', # tangent
        'S', # arcsine
        'C', # arccosine
        'T', # arctangent
        'ś', # hyperbolic sine
        'ć', # hyperbolic cosine
        't́', # hyperbolic tangent
        'Ś', # hyperbolic arcsine
        'Ć', # hyperbolic arccosine
        'T́' # hyperbolic arctangent
    ]

    # Remove redundant brackets on the outside that will stop the root node from being determined
    if expr_string:
        if expr_string[0] == '(' and expr_string[len(expr_string) - 1] == ')':
            expr_string = expr_string[1 : len(expr_string ) - 1]

    previous_is_number = False

    while i < len(expr_string):
        if expr_string[i] in operations:
            if expr_string[i] == '-' and not previous_is_number:
                expr_list.append('n')
            elif isunary(expr_string[i]) and previous_is_number:
                expr_list.append('*')
                expr_list.append(expr_string[i])
            else:
                expr_list.append(expr_string[i])
            previous_is_number = False
        elif expr_string[i] == 'e' or expr_string [i] == 'π':
            if previous_is_number:
                expr_list.append('*')
            expr_list.append(expr_string[i])
            previous_is_number = True
        else:
            num_string = ''
            decimal = False
            while i < len(expr_string) and isfloat(expr_string[i]) == 1:
                if expr_string[i] == '.':
                    if not decimal:
                        decimal = True
                    else:
                        i += 1
                        continue
                num_string += expr_string[i]
                i += 1
            if previous_is_number:
                expr_list.append('*')
            expr_list.append(num_string)
            previous_is_number = True
            i -= 1
        i += 1
    
    return expr_list

def parse(expression_string):
    '''Parses a string and returns an Expression object'''
    expr_list = lexer(translate(expression_string))
    expr = Expression()

    #Determine the root node
    current_index = 0
    brackets = outer_brackets(expr_list)

    for i in range(len(expr_list)):
        if operation_level(expr_list[i]) <= operation_level(expr_list[current_index]):
            if not brackets:
                current_index = i
            else:
                valid_index = True
                for bracket_set in brackets:
                    if bracket_set[0] < i < bracket_set[1]:
                        valid_index = False
                if valid_index:
                    current_index = i
    
    try:
        current_op = operation_level(expr_list[current_index])
    except IndexError:
        current_op = 99

    if current_op == 100:
        expr = parse(input())
    elif current_op == 99: # Check if root node is a number
        if isfloat(expr_list[current_index]) == 2:
            if expr_list[current_index] == 'e':
                expr.set_value(math.e)
            elif expr_list[current_index] == 'π':
                expr.set_value(math.pi)
        else:
            expr.set_value(float(expr_list[current_index]))
    elif current_op == 98:
        last_brackets = brackets.pop()
        expr = parse(expr_list[last_brackets[0] + 1 : last_brackets[1]])
    elif current_op == 4:
        # For unary operations, a check to see if there is are preceding unary operations is required
        while isunary(expr_list[current_index - 1]):
            current_index -= 1
        expr.set_value(expr_list[current_index])
        expr.add_children(parse(expr_list[current_index + 1 : ]))
    elif -1 <= current_op <= 3:
        expr.set_value(expr_list[current_index])
        expr.add_children(
            parse(expr_list[0 : current_index]),
            parse(expr_list[current_index + 1 : ])
        )
    elif current_op == -99:
        indices = ternary(expr_list, '?', ':')
        expr.set_value('if')
        expr.add_children(
            parse(expr_list[0 : indices[0]]),
            parse(expr_list[indices[0] + 1 : indices[1]]),
            parse(expr_list[indices[1] + 1 : ])
        )
    return expr