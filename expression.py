#/usr/bin/python3
'''Mathematical expressions are stored in a tree'''

import math

class Expression():
    '''Tree structure that represents expressions'''

    def __init__(self, value=0):
        self.set_value(value)
        self.children = []
        self.mode = 'radians'
    
    def __repr__(self):
        return '\n' + self.pretty()

    def __str__(self):
        return str(self.evaluate())
    
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
    
    def evaluate(self):
        '''Returns the value of the mathematical expression'''
        if self.expr_type == 'num':
            return self.value
        elif self.expr_type == '?:':
            if self.evaluate_child(0):
                return self.evaluate_child(1)
            else:
                return self.evaluate_child(2)
        elif self.expr_type == '&':
            return self.evaluate_child(0) and self.evaluate_child(1)                
        elif self.expr_type == '|':
            return self.evaluate_child(0) or self.evaluate_child(1)
        elif self.expr_type == '!':
            return not self.evaluate_child(0)
        elif self.expr_type == '+':
            return self.evaluate_child(0) + self.evaluate_child(1)
        elif self.expr_type == '-':
            return self.evaluate_child(0) - self.evaluate_child(1)
        elif self.expr_type == '*':            
            return self.evaluate_child(0) * self.evaluate_child(1)
        elif self.expr_type == '/':
            return self.evaluate_child(0) / self.evaluate_child(1)
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
            return math.degrees(value)
    
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