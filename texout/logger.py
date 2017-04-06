

class Logger():
    """Basic object that outputs text to files."""
    
    def __init__(self, filename):
        self.filename = filename
        
    def write(self, msg, mode='a'):
        with open(self.filename, mode) as f:
            f.write(msg)
    
    def write_line(self, msg):
        self.write(msg)
        self.write('\n')
            
class TexLogger(Logger):
    """A logger that focuses on output to tex files."""
    
    def __init__(self, filename):
        super().__init__(filename)
        self.write(r'\documentclass[11pt,a4paper]{article}', 'w')
        self.write('\n')
        self.write_line(r'\usepackage[utf8]{inputenc}')
        self.write_line(r'\usepackage{amsmath}')
        self.write_line(r'\usepackage{amsfonts}')
        self.write_line(r'\usepackage{amssymb}')
        self.write_line(r'\usepackage{graphicx}')
        self.write_line(r'\usepackage{float}')
        self.write_line(r'\usepackage[left=1.00in, right=1.00in, top=1.00in, bottom=1.00in]{geometry}')
        self.write_line(r'\begin{document}')
        
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
        
        self.write('\\')
        print('{0}section{{{1}}}'.format('sub'*sub, title))
        self.write('{0}section{{{1}}}'.format('sub'*sub, title))
#        self.write_line('\{{0}}section{{1}}'.format('sub'*sub, title))
        self.write('\n\n')
        
    def figure(self, image, caption):
        """Add figure to the tex file.
        
        Parameters:
        
            image (str):
                Location of file to be included in tex.
            caption (str):
                Figure caption."""
        
        self.write('\n')
        self.write_line(r'\begin{figure}[H]')
        self.write_line(r'\centering')
        self.write_line(r'\includegraphics[width=3.in]{' + '{}'.format(image) + '}')
        self.write_line(r'\caption{' + '{}'.format(caption) + '}')
        self.write_line(r'\end{figure}')
        
def texlog(filename):
    return TexLogger(filename)
