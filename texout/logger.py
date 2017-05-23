
import os
import time

class Logger():
    """Basic object that outputs text to files."""
    
    def __init__(self, directory, filename=None):
        if not os.path.exists(directory):
            os.makedirs(directory)
        if filename is None:
            filename = time.strftime('%m-%d--%H-%M-%S', time.localtime()) + '.tex'
        if directory.endswith('/'):
            buffer = ""
        else:
            buffer = "/"
        self.filename = filename
        self.directory = directory + buffer
        self.textfilename = self.directory + filename
        
    def write(self, msg, mode='a'):
        with open(self.textfilename, mode) as f:
            f.write(msg)
    
    def write_line(self, msg):
        self.write(msg)
        self.write('\n')
            
class TexLogger(Logger):
    """A logger that focuses on output to tex files."""
    
    def __init__(self, directory, filename=None):
        super().__init__(directory, filename)
        self.write(r'\documentclass[11pt,a4paper]{article}', 'w')
        self.write('\n')
        self.write_line(r'\usepackage[utf8]{inputenc}')
        self.write_line(r'\usepackage{amsmath}')
        self.write_line(r'\usepackage{amsfonts}')
        self.write_line(r'\usepackage{amssymb}')
        self.write_line(r'\usepackage{graphicx}')
        self.write_line(r'\usepackage{float}')
        self.write_line(r'\usepackage[left=1.00in, right=1.00in, top=1.00in, bottom=1.00in]{geometry}')
        self.write_line(r'\setcounter{secnumdepth}{5}')
        self.write_line(r'\begin{document}')
        self.write_line('\\noindent')
        
    def texline(self, msg):
        """Write a tex line, that is a message followed by 
        double slashes followed by double a new line."""
        
        self.write_line(msg + "\\\\")
        
    def close(self):
        """End the tex document."""
        
        self.write(r'\end{document}')
        
    def section(self, title, sub=0):
        """Add section to tex file.
        
        Parameters:
        
            title (str):
                Name of the section
                
        Keywords:
        
            sub (int):
                The depth of the section.  Defaults to 0."""
                
        if sub < 3:
            self.write_line('\{0}section{{{1}}}\n'.format('sub'*sub, title))
        elif sub == 3:
            self.write_line('\paragraph{{{0}}} \mbox{{}} \n'.format(title))
            self.write_line('\\noindent')
        elif sub == 4:
            self.write_line('\subparagraph{{{0}}} \mbox{{}} \n'.format(title))
            self.write_line('\\noindent')
        else:
            raise ValueError("TeX file cannot handle section levels greater than 5.")
            
    def figure(self, image, caption, width=3.):
        """Add figure to the tex file.
        
        Parameters:
        
            image (str):
                Location of file to be included in tex.
            caption (str):
                Figure caption.
                
        Keywords:
        
            width (float):
                Width in inches of the figure."""
        
        self.write('\n')
        self.write_line(r'\begin{figure}[H]')
        self.write_line(r'\centering')
        self.write_line(r'\includegraphics[width={0}in]{{{1}}}'.format(width, image))
        self.write_line(r'\caption{' + '{}'.format(caption) + '}')
        self.write_line(r'\end{figure}')
        
def texlog(filename):
    return TexLogger(filename)
