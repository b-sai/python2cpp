from collections import deque
from lark import Lark
import sys
my_grammar = """
?start: statement_list

tab: "<IN>"

?statement_list: command+

command : tab* (assignment
            | if_statement
            | function
            | while_statement)

assignment:   var "="  (string|number|addition|subtraction|multiplication|division)
if_statement:  "if" expression":"statement_list
while_statement: "while" expression":"statement_list
addition: _token "+"  _token -> add
subtraction: _token "-"  _token -> sub
multiplication: _token "*"  _token -> mul
division: _token "/"  _token -> div

_token: var | number


?expression: var
            | number
            | expression ">" expression -> gt
            | expression "<"  expression -> lt
            | expression ">=" expression -> ge
            | expression "<="  expression -> le
            | expression "==" expression -> eq
            | expression "!="  expression -> ne
            | if_statement

function : var "(" arg ")" 
arg : string|number|var



var:NAME
string:ESCAPED_STRING
number:NUMBER

%import common.ESCAPED_STRING
%import common.CNAME -> NAME
%import common.WS
%import common.INT -> NUMBER
%ignore WS
"""
dep = [0]


def get_num_tabs(t):
    count = 0
    for cmd in t.children:
        if cmd.data == 'tab':
            count += 1
    return count


stack = deque()


def translate(t):
    if t.data == 'statement_list':
        ret_str = []
        for cmd in t.children:
            ret_str.append(translate(cmd))
        while len(stack) > 0 and (stack[-1] > get_num_tabs(t)):
            ret_str.append("}")
            stack.pop()
        return "\n".join(ret_str)

    elif t.data == 'var':
        return t.children[0]

    elif t.data == 'tab':
        return "<IN>"

    elif t.data == 'command':
        ret_str = []

        if len(stack) == 0:
            if get_num_tabs(t) == 1:
                ret_str.append("{")
                stack.append(get_num_tabs(t))
        elif len(stack) > 0:

            if get_num_tabs(t) > stack[-1]:
                ret_str.append("{")
                stack.append(get_num_tabs(t))
        while len(stack) > 0 and (stack[-1] > get_num_tabs(t)):
            ret_str.append("}")
            stack.pop()
        for cmd in t.children:
            ret_str.append(translate(cmd))

        ret_str = [x for x in ret_str if x != "<IN>"]

        return "\n".join(ret_str)

    elif t.data == 'string':
        return t.children[0]

    elif t.data == 'assignment':
        lhs, rhs = t.children
        if rhs.data == 'number':
            dtype = 'int '
        elif rhs.data == 'string ':
            dtype = 'string'
        else:
            dtype = ""
        return dtype + translate(lhs) + '=' + translate(rhs)+';'

    elif t.data == 'if_statement':
        case, block = t.children
        return 'if (' + translate(case) + translate(block)

    elif t.data == 'while_statement':
        case, block = t.children
        return 'while (' + translate(case) + translate(block)

    elif t.data == 'lt':
        return translate(t.children[0]) + "<" + translate(t.children[1]) + ")"
    elif t.data == 'gt':
        return translate(t.children[0]) + ">" + translate(t.children[1]) + ")"
    elif t.data == 'le':
        return translate(t.children[0]) + "<=" + translate(t.children[1]) + ")"
    elif t.data == 'ge':
        return translate(t.children[0]) + ">=" + translate(t.children[1]) + ")"
    elif t.data == 'eq':
        return translate(t.children[0]) + "==" + translate(t.children[1]) + ")"
    elif t.data == 'ne':
        return translate(t.children[0]) + "!=" + translate(t.children[1]) + ")"

    elif t.data == 'number':
        return t.children[0]

    elif t.data == 'arg':
        return t.children[0]

    elif t.data == 'add':
        return translate(t.children[0]) + "+" + translate(t.children[1])
    elif t.data == 'sub':
        return translate(t.children[0]) + "-" + translate(t.children[1])
    elif t.data == 'div':
        return translate(t.children[0]) + "/" + translate(t.children[1])
    elif t.data == 'mul':
        return translate(t.children[0]) + "*" + translate(t.children[1])

    elif t.data == 'token':
        return t.children[0]

    else:
        print(t.children)
        raise SyntaxError("bad tree")


if __name__ == '__main__':

    args = sys.argv

    if len(args) > 1:
        inp_file = open(args[1])
        program = inp_file.readlines()
        program = "".join(program)
    else:
        program = """
        if 1>2:
        <IN>a=1
        <IN>if 2>3:
        <IN><IN>b=2
        c=3
        if 4 < 5:
        <IN>k=0
        while 1>2:
        <IN>d=4
        """
    parser = Lark(my_grammar)

    parse_tree = parser.parse(program)
    print(translate(parse_tree))
