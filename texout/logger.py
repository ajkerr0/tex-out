
import csv
import os
import time

import numpy as np

class Logger():
    """Basic object that outputs text to files."""
    
    def __init__(self, directory, filename=None):
        
        self.mkdir(directory)
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
        
    def savefig(self, fig, figname):
        plotdir = self.directory + 'images/'
        self.mkdir(plotdir)
        fig.tight_layout()
        fig.savefig(plotdir+figname)
    
    @staticmethod
    def mkdir(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
            
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
        self.write_line(r'\graphicspath{ {images/} }')
        self.write_line(r'\usepackage[left=1.00in, right=1.00in, top=1.00in, bottom=1.00in]{geometry}')
        self.write_line(r'\setcounter{secnumdepth}{5}')
        self.write_line(r'\begin{document}')
        self.write_line('\\noindent')
        
    def texline(self, msg):
        """Write a tex line, that is a message followed by 
        double slashes followed by double a new line."""
        
        self.write_line(msg + " \\\\")
        
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
            
    def figure(self, fig, imagename, caption, width=3.):
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
        self.write_line(r'\includegraphics[width={0}in]{{{1}}}'.format(width, imagename))
        self.write_line(r'\caption{' + '{}'.format(caption) + '}')
        self.write_line(r'\end{figure}')
        
        self.savefig(fig, imagename)
        
class DataLogger:
    """A logger that focuses on output to csv files."""
    
    def __init__(self, filename, cat):
        self.filename = filename
        try:
            os.stat(filename).st_size
        except FileNotFoundError:
            self.write(cat)
#            self.write(dtypes)
   
    def write(self, data):
        with open(self.filename, 'a', newline='') as f:
            line_writer = csv.writer(f, delimiter=',')
            line_writer.writerow([datum for datum in data])
        
def data_read(filename, x, y, **constraints):
    
    # load entire data file
    data = np.genfromtxt(filename, 
                         dtype=None,
                         delimiter=',',
                         skip_header=0,
                         names=True)
    
    # keep only the data points that meet constraints
    indices = None
    for constrained_var, constraint in constraints.items():
        
        if constraint is None:
            # we ignore this constraint and go to the next one
#            continue
            pass
        
        step_indices = np.where(data[constrained_var] == constraint)[0]
        try:
            indices = np.intersect1d(indices, step_indices)
        except TypeError:
            # if indices is None, make it step_indices
            indices = step_indices
            
    if indices is None:
        pass
    else:
        try:
            data = data[indices]
        except IndexError:
            raise ValueError("No data meets the constraints")
    
    # group data points based on remaining degrees of freedom
    constraints[x] = ''
    constraints[y] = ''
    dofs = [x for x in data.dtype.names if x not in constraints]
    
    # determine shape of data
    shape = []
    dof_uniques = []
    for dof in dofs:
        uniques = np.unique(data[dof])
        shape.append(len(uniques))
        dof_uniques.append(uniques)
        
    # build nested lists with recursive algorithm
    # credit this step to Abhijit on StackOverflow    
    def build_list(shape):
        if not shape:
            return []
        return [build_list(shape[1:]) for i in range(shape[0])]
    xdata = build_list(shape)
    ydata = build_list(shape)
    
    # populate grouped data
    for datum in data:
        innerx, innery = xdata, ydata
        for dof, ulist in zip(dofs, dof_uniques):
            index = np.where(ulist==datum[dof])[0][0]
            innerx = innerx[index]
            innery = innery[index]
        innerx.append(datum[x])
        innery.append(datum[y])
    
    # fill numpy arrays with averages and stds
    xavgs, yavgs, xstds, ystds, vals = [],[],[],[],[]
    for indices in np.ndindex(*shape):
        innerx, innery = xdata, ydata
        val = []
        for count, index in enumerate(indices):
            innerx = innerx[index]
            innery = innery[index]
            val.append(dof_uniques[count][index])
        xavgs.append(np.average(innerx))
        yavgs.append(np.average(innery))
        xstds.append(np.std(innerx))
        ystds.append(np.std(innery))
        vals.append(val)
        
    return np.asarray(xavgs), np.asarray(yavgs), np.asarray(xstds), \
           np.asarray(ystds), vals, dofs
           
def data_read_individual(filename, x, y, **constraints):
    
    # load entire data file
    data = np.genfromtxt(filename, 
                         dtype=None,
                         delimiter=',',
                         skip_header=0,
                         names=True)
    
    # keep only the data points that meet constraints
    indices = None
    for constrained_var, constraint in constraints.items():
        step_indices = np.where(data[constrained_var] == constraint)[0]
        try:
            indices = np.intersect1d(indices, step_indices)
        except TypeError:
            # if indices is None, make it step_indices
            indices = step_indices
    data = data[indices]
    
    return data[x], data[y]
    
def texlog(filename):
    return TexLogger(filename)
