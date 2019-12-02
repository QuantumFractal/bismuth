from lark import Lark, Transformer, Token, Visitor, v_args
import logging
logging.basicConfig(level=logging.DEBUG)

import sys
from pathlib import Path

top_dir = Path(sys.path[0]).parents[0]
grammar_dir = top_dir / "grammar"
svg_dir = top_dir / "svg"

def parse_number(value):
    attr_val = None
    try:
        attr_val = float(value)
    except ValueError:
        try:
            attr_val = int(value)
        except ValueError:
            pass
    return attr_val


class T(Transformer):
    def start(self, *args):
        return args[0]

    def command(self, *args):
        tree = args[0][0]
        command = tree.data
        points = [t for t in tree.children if type(t) != Token]
        data = {'command': command, 'points': points}
        return data

    def pair(self, *args):
        first = parse_number(args[0][0].value)
        second = parse_number(args[0][1].value)
        return (first, second)


svg_parser = None
with open(grammar_dir / "path.lark", 'r') as f:
    svg_parser = Lark(f.read(), parser='lalr', debug=True)


path_string = "M20,230 Q40,205 50,230 T90,230"
#path_string = "M 10 10 C 20 20, 40 20, 50 10"

tree = svg_parser.parse(path_string)
print(tree.pretty())

print("-"*30)
t = T().transform(tree)
print("-"*30)
print(t)
import code; code.interact(local=locals()) 