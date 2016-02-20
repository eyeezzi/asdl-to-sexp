import sys
import os
import subprocess

def cls():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def sexpr_to_json(src):

    if src.loc < len(src.sexp) and src.sexp[src.loc] == '(':
        src.lp += 1
        src.json += "{\"name\": \""
        src.loc += 1
        while src.loc < len(src.sexp):
            if src.sexp[src.loc] == " ":
                # we are going to add children
                if src.lp - src.rp == src.depth:
                    # don't create a new children node.
                    src.json += "\",\"children\": ["
                    break
                else:
                    # create a new children node.
                    src.depth += 1
                    src.json += "\",\"children\": ["
                    src.loc += 1
                    sexpr_to_json(src)
            elif src.sexp[src.loc] == ")":
                src.depth -= 1
                src.json += "\""
                src.loc += 1
                src.rp += 1
                break
            else:
                src.json += src.sexp[src.loc]
                src.loc += 1
        src.json += "]}"

def recursive_conv(src):

    if src.loc >= len(src.asdl):
        return

    if src.asdl[src.loc] != "(":
        src.sexp += "("
        while src.loc < len(src.asdl) and src.asdl[src.loc] != ")":
            if src.asdl[src.loc] == "(":
                src.sexp += " "
                src.loc += 1
                recursive_conv(src)
            elif src.asdl[src.loc] == ",":
                src.sexp += ") ("
                src.loc += 1
            else:
                src.sexp += src.asdl[src.loc]
                src.loc += 1
        src.sexp += ")"
        src.loc += 1
        return

    return

class data:
    def __init__(self, asdl):
        self.asdl = asdl
        self.loc = 0
        self.sexp = ""
        self.json = ""
        self.lp = 0
        self.rp = 0
        self.close = False
        self.depth = 0

def is_matching_paren(src):
    """ recursively parses a string representing an AST in ASDL format
        into a Lisp-style s-expression
    """
    num_of_lparen = 0
    num_of_rparen = 0

    for i in range(0, len(src), 1):
        if src[i] == "(":
            num_of_lparen += 1
        elif src[i] == ")":
            num_of_rparen += 1
        else:
            pass

    if num_of_lparen == num_of_rparen:
        return True
    else:
        return False

def asdl_to_sexpr(src):
    """ iteratively parses a string representing an AST in ASDL format
        into a Lisp-style s-expression
    """
    asdl = list(src)
    output = list("")
    store = ""

    for i in range(len(asdl)-1, -1, -1):
        curr = asdl[i]

        if curr == "(" and store == "(":
            output.append(curr)
            output.append(" ")
            continue

        if i == 0 and store == "(":
            output.append(curr)
            output.append(store)
            store = ""
            break

        if curr == "(" and store != "(":
            store = "("
            output.append(" ")
            i -= 1
            continue

        if curr == "," and store == "(":
            output.append(store)
            store = ""
            output.append(" ")
            i -= 1
            continue

        output.append(curr)

    output = output[::-1]  # reverse list
    sexpr = "".join(output)
    return sexpr

if len(sys.argv) == 1:
    cls()
    print("""\
====================================================================================================
This program converts an Abstract Syntax Tree (AST) represented in the ASDL format
into a corresponding S-Expression. The S-Expression is then saved to a file and optionally
displayed in a GUI window.

Requirements:
    Python 3.x,
    Tcl/tk (wish), and the file "viewtree.tk" in the current directory.

How to execute the program:
    $ python asdl2sexp.py
        Displays this introduction.

    $ python asdl2sexp.py <input_filename>
        process the file given by <input_filename>. This should be the file containing the AST data

    Example:
        $ python asdl2sexp.py myast.ast

The output of the program:
    The program will produce the output file <input_filename>.sexpr, containing the s-expression
    corresponding to your supplied AST. If you have Tcl/tk installed and the file viewtree.tk in
    your current working directory, the graphical tree for the AST will also be displayed.

    Example:
        $ python asdl2exp.py myast.abc
    will produce the file
        myast.sexpr
----------------------------------------------------------------------------------------------------
Author: Uzziah Eyee (2016), ueyee@sfu.ca
Licence: GNU GPL v.2.0
----------------------------------------------------------------------------------------------------
Credits:
    GUI Graphing Program "viewtree.tk" written by:
    Adwait Ratnaparkhi
    Dept. of Computer and Information Science
    University of Pennsylvania, 1996
    adwait@unagi.cis.upenn.edu
====================================================================================================
    """)

elif len(sys.argv) >= 2:

    # if the input file does not exist
    if not os.path.isfile(sys.argv[1]):
        print("Error: The file you specified does not exist, please double check.")
        exit()
    else:
        input_filename, file_extension = os.path.splitext(sys.argv[1])

        asdl_string = ""
        with open(sys.argv[1], 'r') as myfile:
            asdl_string = myfile.read().replace('\n', '')

        if not is_matching_paren(asdl_string):
            print("Warning: You have unmatching parenthesis in your ASDL AST")
        ## uncomment the line below to use the iterative version.
        # sexpr_string = asdl_to_sexpr(asdl_string)

        # comment the 3 lines below to use the iterative version.
        mydata = data(asdl_string)
        recursive_conv(mydata)
        sexpr_string = mydata.sexp

        mydata.loc = 0
        sexpr_to_json(mydata)
        print(mydata.sexp)
        print(mydata.json)
        exit()

        # the output file is named <input-file>.sexpr
        output_filename = "{}.sexpr".format(input_filename)
        with open(output_filename, "w") as text_file:
            print(sexpr_string, file=text_file)
            print("Log: Conversion done. Output file: {}".format(output_filename))

        # now try to display the s-exp in viewtree.tk
        cwd = os.getcwd()
        dir_content = os.listdir(cwd)

        # if the required tk program exists in the current directory
        if "viewtree.tk" in dir_content:
            command = "wish viewtree.tk {}".format(output_filename)
            subprocess.call(command)
        else:
            print("Log: Please add the file \"viewtree.tk\" to your current directory to enable pretty printing.")
            exit()
else:
    print("Error: Incorrect invocation.")
    exit()
