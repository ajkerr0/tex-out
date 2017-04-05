
import os
import time

class Logger():
    """Basic object that outputs text to files."""
    
    def __init__(self, filename):
        self.filename = filename
        
    def write(self, msg):
        with open(self.filename, 'a') as f:
            self.write_n(msg)
    
    def write_n(self, msg):
        with open(self.filename, 'a') as f:
            self.write_n(msg)
            self.write_n('\n')
            
class TexLogger(Logger):
    """A logger that focuses on output to tex files."""
    
    def __init__(self, filename):
        super().__init__(filename)
        self.write_n(r'\documentclass[11pt,a4paper]{article}')
        self.write_n(r'\usepackage[utf8]{inputenc}')
        self.write_n(r'\usepackage{amsmath}')
        self.write_n(r'\usepackage{amsfonts}')
        self.write_n(r'\usepackage{amssymb}')
        self.write_n(r'\usepackage{graphicx}')
        self.write_n(r'\usepackage{float}')
        self.write_n(r'\usepackage[left=1.00in, right=1.00in, top=1.00in, bottom=1.00in]{geometry}')
        self.write_n(r'\begin{document}')
        
    
        
    def close(self):
        self.write(r'\end{document}')
