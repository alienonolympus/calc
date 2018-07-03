#/usr/bin/python3

import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.label import Label

class CalcGUI(App):
    def build(self):
        return Label(text='Hello world')

def gui():
    CalcGUI().run()
    