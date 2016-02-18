# asdl-to-sexp
A python program that converts Abtract Syntax Tree (AST) files represented in the ASDL format into S-expressions

====================================================================================================
###Overview:
This program converts an Abstract Syntax Tree (AST) represented in the ASDL format
into a corresponding S-Expression. The S-Expression is then saved to a file and optionally
displayed in a GUI window.

###Requirements:
    Python 3.x,
    Tcl/tk (wish), and the file "viewtree.tk" in the current directory.

###How to execute the program:

    $ python asdl2sexp.py
        Displays this introduction.

    $ python asdl2sexp.py <input_filename>
        process the file given by <input_filename>. This should be the file containing the AST data

    Example:
        $ python asdl2sexp.py myast.ast

###The output of the program:   
    The program will produce the output file <input_filename>.sexpr, containing the s-expression
    corresponding to your supplied AST. If you have Tcl/tk installed and the file viewtree.tk in
    your current working directory, the graphical tree for the AST will also be displayed.

    Example:
        $ python asdl2exp.py myast.abc
    will produce the file
        myast.sexpr
----------------------------------------------------------------------------------------------------

Author: Uzziah Eyee (2016)
Licence: Potato License--Bake it, fry it, toast it, ...just don't waste it.

----------------------------------------------------------------------------------------------------
####Credits:   
    GUI Graphing Program "viewtree.tk" written by:   
    Adwait Ratnaparkhi   
    Dept. of Computer and Information Science   
    University of Pennsylvania, 1996   
    adwait@unagi.cis.upenn.edu   
    
====================================================================================================
