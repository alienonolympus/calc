#/usr/bin/python3

from parse import parse
from gui import gui

def cli():
    mode = 'radians'
    while True:
        input_string = input('>>')
        if input_string == 'exit':
            return
        elif input_string == 'degrees':
            mode = 'degrees'
        elif input_string == 'radians':
            mode = 'radians'
        else:
            expr = parse(input_string)
            expr.mode = mode
            print(round(expr.evaluate(), 5))
mode = input('Mode: ')

if mode == 'cli':
    cli()
elif mode == 'gui':
    gui()