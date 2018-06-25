#/usr/bin/python3
'''Mathematical expressions are stored in a tree'''

class Expression():
    '''Tree structure that represents expressions'''

    def __init__(self, value=0):
        self.set_value(value)
        self.children = []
    
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
        else:
            if self.expr_type == '+':
                return self.children[0].evaluate() + self.children[1].evaluate()
            elif self.expr_type == '-':
                return self.children[0].evaluate() - self.children[1].evaluate()
            elif self.expr_type == '*':            
                return self.children[0].evaluate() * self.children[1].evaluate()
            elif self.expr_type == '/':
                return self.children[0].evaluate() / self.children[1].evaluate()